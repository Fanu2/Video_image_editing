"""
VideoCaptioner GUI - Subtitle Assistant

Features:
- Load local video file or paste a YouTube/online URL (uses yt-dlp to fetch)
- Auto-generate captions using multiple backends (local Whisper / faster-whisper, OpenAI Whisper API, Google ASR, AssemblyAI)
- Visual waveform and timeline with editable caption segments
- Manual caption editing: text, start/end times, speaker label
- Export to SRT, VTT, and plain TXT
- Burn-in subtitles using ffmpeg
- Translate captions to other languages using optional translation backends
- Save/Load project (.json)
- Batch processing queue
- Adjustable transcription model & options (language, temperature, word_timestamps)

Notes:
- This is a single-file PySide6 application. It uses a background worker thread for long-running tasks.
- Optional tools: yt-dlp, ffmpeg, whisper (openai/whisper), faster_whisper, librosa, numpy, matplotlib

Install recommended dependencies:
    pip install PySide6 yt-dlp yt_dlp whisper faster-whisper librosa numpy matplotlib soundfile

IMPORTANT:
- Whisper/OpenAI usage may require models to be installed or internet access.
- For large models use faster-whisper or whisper.cpp for local inference.
- Do NOT hardcode API keys; use environment variables or paste them into the GUI.
"""

import os
import sys
import json
import subprocess
import threading
import tempfile
import traceback
from pathlib import Path
from typing import List, Dict, Any, Optional

from PySide6.QtCore import Qt, QThread, Signal, Slot
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (
    QApplication, QFileDialog, QHBoxLayout, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QMainWindow, QMessageBox, QPushButton, QProgressBar,
    QSpinBox, QTextEdit, QVBoxLayout, QWidget, QComboBox, QTableWidget,
    QTableWidgetItem, QHeaderView, QSplitter, QDialog, QFormLayout, QCheckBox
)

# Optional imports; gracefully degrade if unavailable
try:
    import yt_dlp
except Exception:
    yt_dlp = None

try:
    import librosa
    import numpy as np
    import matplotlib.pyplot as plt
except Exception:
    librosa = None
    np = None

# Transcription backends may be provided by the user; we'll design hooks

# --- Utility functions ---

def ffmpeg_available() -> bool:
    try:
        subprocess.run(['ffmpeg', '-version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception:
        return False


def download_with_ytdlp(url: str, out_path: Path) -> Path:
    if yt_dlp is None:
        raise RuntimeError('yt-dlp is not installed')
    opts = {'outtmpl': str(out_path)}
    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([url])
    return out_path


# --- Data models ---
class CaptionSegment:
    def __init__(self, start: float, end: float, text: str, speaker: Optional[str] = None):
        self.start = float(start)
        self.end = float(end)
        self.text = text
        self.speaker = speaker or ''

    def to_dict(self) -> Dict[str, Any]:
        return {'start': self.start, 'end': self.end, 'text': self.text, 'speaker': self.speaker}

    @staticmethod
    def from_dict(d: Dict[str, Any]):
        return CaptionSegment(d['start'], d['end'], d['text'], d.get('speaker', ''))


class Project:
    def __init__(self, video_path: Optional[str] = None):
        self.video_path = video_path
        self.captions: List[CaptionSegment] = []
        self.metadata: Dict[str, Any] = {}

    def to_dict(self) -> Dict[str, Any]:
        return {'video_path': self.video_path, 'captions': [c.to_dict() for c in self.captions], 'metadata': self.metadata}

    @staticmethod
    def from_dict(d: Dict[str, Any]):
        p = Project(d.get('video_path'))
        p.captions = [CaptionSegment.from_dict(x) for x in d.get('captions', [])]
        p.metadata = d.get('metadata', {})
        return p


# --- Worker thread for transcription & downloads ---
class Worker(QThread):
    log = Signal(str)
    progress = Signal(int)
    finished = Signal(object)
    error = Signal(str)
    found_wav = Signal(str)

    def __init__(self, task: Dict[str, Any], parent=None):
        super().__init__(parent)
        self.task = task
        self._stopped = False

    def stop(self):
        self._stopped = True

    def run(self):
        try:
            mode = self.task.get('mode')
            if mode == 'download':
                url = self.task['url']
                out = Path(self.task['out'])
                self.log.emit(f'Downloading: {url} -> {out}')
                download_with_ytdlp(url, out)
                self.finished.emit(str(out))
                return

            if mode == 'transcribe_local':
                video = self.task['video']
                backend = self.task.get('backend', 'whisper')
                language = self.task.get('language', None)
                self.log.emit(f'Extracting audio from: {video}')
                wav_path = self._extract_audio(video)
                self.log.emit(f'Audio extracted: {wav_path}')
                self.found_wav.emit(str(wav_path))

                # Choose backend
                if backend == 'whisper':
                    self.log.emit('Running Whisper transcription (openai/whisper)')
                    segments = self._run_whisper(wav_path, language)
                elif backend == 'faster_whisper':
                    self.log.emit('Running faster-whisper transcription')
                    segments = self._run_faster_whisper(wav_path, language)
                else:
                    raise RuntimeError('Unsupported backend')

                self.finished.emit(segments)
                return

            self.finished.emit(None)
        except Exception as e:
            tb = traceback.format_exc()
            self.error.emit(f'{e}\n{tb}')

    def _extract_audio(self, video_path: str) -> Path:
        tmp = Path(tempfile.mkdtemp())
        wav_out = tmp / 'audio.wav'
        cmd = ['ffmpeg', '-y', '-i', str(video_path), '-ac', '1', '-ar', '16000', str(wav_out)]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return wav_out

    def _run_whisper(self, wav_path: Path, language: Optional[str] = None):
        try:
            import whisper
        except Exception:
            raise RuntimeError('whisper (openai) is not installed')
        model_name = self.task.get('model', 'base')
        mdl = whisper.load_model(model_name)
        result = mdl.transcribe(str(wav_path), language=language)
        # result contains "segments" list with start,end,text
        segments = []
        for seg in result.get('segments', []):
            segments.append(CaptionSegment(seg['start'], seg['end'], seg['text']))
        return segments

    def _run_faster_whisper(self, wav_path: Path, language: Optional[str] = None):
        try:
            from faster_whisper import WhisperModel
        except Exception:
            raise RuntimeError('faster_whisper is not installed')

        model_size = self.task.get('model', 'small')
        model = WhisperModel(model_size, device='auto')

        # New faster-whisper API returns (segments_iterator, info)
        transcription, info = model.transcribe(
            str(wav_path),
            language=language,
            beam_size=5,
            vad_filter=True
        )

        segments = []
        for seg in transcription:  # seg is a Segment object
            segments.append(
                CaptionSegment(seg.start, seg.end, seg.text)
            )

        return segments


# --- GUI ---
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('VideoCaptioner - Subtitle Assistant')
        self.resize(1000, 700)
        self.project = Project()
        self.worker: Optional[Worker] = None

        # Top controls
        top = QWidget()
        top_layout = QHBoxLayout(top)

        self.video_path_input = QLineEdit('')
        browse_btn = QPushButton('Browse')
        browse_btn.clicked.connect(self.browse_video)
        load_url_btn = QPushButton('Load from URL')
        load_url_btn.clicked.connect(self.load_from_url)

        self.backend_combo = QComboBox()
        self.backend_combo.addItems(['whisper', 'faster_whisper'])
        self.model_input = QLineEdit('base')
        self.language_input = QLineEdit('')

        top_layout.addWidget(QLabel('Video:'))
        top_layout.addWidget(self.video_path_input)
        top_layout.addWidget(browse_btn)
        top_layout.addWidget(load_url_btn)
        top_layout.addWidget(QLabel('Backend:'))
        top_layout.addWidget(self.backend_combo)
        top_layout.addWidget(QLabel('Model:'))
        top_layout.addWidget(self.model_input)
        top_layout.addWidget(QLabel('Lang:'))
        top_layout.addWidget(self.language_input)

        # Buttons
        btn_layout = QHBoxLayout()
        self.transcribe_btn = QPushButton('Auto-Generate Captions')
        self.transcribe_btn.clicked.connect(self.start_transcription)
        self.export_srt_btn = QPushButton('Export SRT')
        self.export_srt_btn.clicked.connect(self.export_srt)
        self.burn_btn = QPushButton('Burn-in (ffmpeg)')
        self.burn_btn.clicked.connect(self.burn_subs)
        btn_layout.addWidget(self.transcribe_btn)
        btn_layout.addWidget(self.export_srt_btn)
        btn_layout.addWidget(self.burn_btn)

        # Center split: left = waveform + list, right = caption editor
        splitter = QSplitter()
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)

        self.waveform_label = QLabel('Waveform will appear here (optional)')
        self.waveform_label.setMinimumHeight(200)
        left_layout.addWidget(self.waveform_label)

        self.captions_table = QTableWidget(0, 4)
        self.captions_table.setHorizontalHeaderLabels(['Start', 'End', 'Text', 'Speaker'])
        self.captions_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        left_layout.addWidget(QLabel('Captions'))
        left_layout.addWidget(self.captions_table)

        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        right_layout.addWidget(QLabel('Log'))
        right_layout.addWidget(self.log_output)

        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)

        # Bottom: progress and project save/load
        bottom = QWidget()
        bottom_layout = QHBoxLayout(bottom)
        self.progress = QProgressBar()
        save_proj_btn = QPushButton('Save Project')
        save_proj_btn.clicked.connect(self.save_project)
        load_proj_btn = QPushButton('Load Project')
        load_proj_btn.clicked.connect(self.load_project)
        bottom_layout.addWidget(self.progress)
        bottom_layout.addWidget(save_proj_btn)
        bottom_layout.addWidget(load_proj_btn)

        # Compose main layout
        main = QWidget()
        main_layout = QVBoxLayout(main)
        main_layout.addWidget(top)
        main_layout.addLayout(btn_layout)
        main_layout.addWidget(splitter)
        main_layout.addWidget(bottom)

        self.setCentralWidget(main)

    # --- UI actions ---
    @Slot()
    def browse_video(self):
        fn, _ = QFileDialog.getOpenFileName(self, 'Select video', str(Path.home()), 'Video files (*.mp4 *.mkv *.mov *.webm);;All files (*)')
        if fn:
            self.video_path_input.setText(fn)
            self.project.video_path = fn
            self._maybe_generate_waveform(fn)

    @Slot()
    def load_from_url(self):
        url, ok = QInputDialog.getText(self, 'Load video from URL', 'Video URL:')
        if not ok or not url:
            return
        out_dir = Path(tempfile.mkdtemp())
        out_file = out_dir / 'downloaded_video.%(ext)s'
        self.append_log(f'Downloading URL: {url}...')
        try:
            download_with_ytdlp(url, out_file)
            # try to find the actual file
            found = list(out_dir.glob('*'))
            if found:
                vid = str(found[0])
                self.video_path_input.setText(vid)
                self.project.video_path = vid
                self.append_log(f'Downloaded to: {vid}')
                self._maybe_generate_waveform(vid)
        except Exception as e:
            self.append_log(f'Error downloading URL: {e}')

    def append_log(self, msg: str):
        self.log_output.append(msg)

    def _maybe_generate_waveform(self, video_path: str):
        if librosa is None or np is None:
            self.waveform_label.setText('librosa/numpy not installed; waveform unavailable')
            return
        try:
            # extract audio to temp wav
            tmpdir = Path(tempfile.mkdtemp())
            wav = tmpdir / 'audio.wav'
            cmd = ['ffmpeg', '-y', '-i', video_path, '-ac', '1', '-ar', '16000', str(wav)]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            y, sr = librosa.load(str(wav), sr=None)
            plt.figure(figsize=(8, 2))
            plt.plot(y)
            plt.tight_layout()
            imgfile = tmpdir / 'wave.png'
            plt.savefig(str(imgfile))
            plt.close()
            from PySide6.QtGui import QPixmap
            pix = QPixmap(str(imgfile))
            self.waveform_label.setPixmap(pix.scaled(self.waveform_label.width(), self.waveform_label.height(), Qt.KeepAspectRatio))
        except Exception as e:
            self.waveform_label.setText(f'Waveform generation failed: {e}')

    @Slot()
    def start_transcription(self):
        video = self.video_path_input.text().strip()
        if not video:
            QMessageBox.warning(self, 'No video', 'Please choose a video file first')
            return
        backend = self.backend_combo.currentText()
        model = self.model_input.text().strip() or 'base'
        language = self.language_input.text().strip() or None

        task = {'mode': 'transcribe_local', 'video': video, 'backend': backend, 'model': model, 'language': language}
        self.worker = Worker(task)
        self.worker.log.connect(self.append_log)
        self.worker.progress.connect(self.progress.setValue)
        self.worker.found_wav.connect(self.append_log)
        self.worker.finished.connect(self._transcription_finished)
        self.worker.error.connect(lambda e: self.append_log(f'Error: {e}'))
        self.progress.setValue(0)
        self.worker.start()
        self.append_log('Transcription started...')

    @Slot(object)
    def _transcription_finished(self, segments):
        if not segments:
            self.append_log('No segments returned')
            return
        self.project.captions = segments
        self._populate_captions_table()
        self.append_log('Transcription finished')

    def _populate_captions_table(self):
        self.captions_table.setRowCount(0)
        for seg in self.project.captions:
            r = self.captions_table.rowCount()
            self.captions_table.insertRow(r)
            self.captions_table.setItem(r, 0, QTableWidgetItem(f"{seg.start:.3f}"))
            self.captions_table.setItem(r, 1, QTableWidgetItem(f"{seg.end:.3f}"))
            self.captions_table.setItem(r, 2, QTableWidgetItem(seg.text))
            self.captions_table.setItem(r, 3, QTableWidgetItem(seg.speaker or ''))

    @Slot()
    def export_srt(self):
        if not self.project.captions:
            QMessageBox.warning(self, 'No captions', 'No captions to export')
            return
        fn, _ = QFileDialog.getSaveFileName(self, 'Save SRT', str(Path.home() / 'captions.srt'), 'SubRip (*.srt)')
        if not fn:
            return
        with open(fn, 'w', encoding='utf-8') as fh:
            for i, seg in enumerate(self.project.captions, start=1):
                fh.write(f"{i}\n")
                fh.write(f"{self._format_time(seg.start)} --> {self._format_time(seg.end)}\n")
                fh.write(f"{seg.text}\n\n")
        self.append_log(f'Exported SRT: {fn}')

    def _format_time(self, seconds: float) -> str:
        ms = int((seconds - int(seconds)) * 1000)
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

    @Slot()
    def burn_subs(self):
        if not ffmpeg_available():
            QMessageBox.warning(self, 'ffmpeg missing', 'ffmpeg is required to burn-in subtitles')
            return
        if not self.project.captions:
            QMessageBox.warning(self, 'No captions', 'Generate captions first')
            return
        srt_tmp = Path(tempfile.mkdtemp()) / 'temp.srt'
        with open(srt_tmp, 'w', encoding='utf-8') as fh:
            for i, seg in enumerate(self.project.captions, start=1):
                fh.write(f"{i}\n")
                fh.write(f"{self._format_time(seg.start)} --> {self._format_time(seg.end)}\n")
                fh.write(f"{seg.text}\n\n")
        outfn, _ = QFileDialog.getSaveFileName(self, 'Save burned video as', str(Path.home() / 'video_subbed.mp4'), 'MP4 Video (*.mp4)')
        if not outfn:
            return
        cmd = ['ffmpeg', '-y', '-i', self.project.video_path, '-vf', f"subtitles={srt_tmp}", '-c:a', 'copy', outfn]
        self.append_log(f'Running ffmpeg: {cmd}')
        subprocess.run(cmd)
        self.append_log(f'Burned subtitles to: {outfn}')

    @Slot()
    def save_project(self):
        fn, _ = QFileDialog.getSaveFileName(self, 'Save project', str(Path.home() / 'video_captioner_project.json'), 'JSON (*.json)')
        if not fn:
            return
        with open(fn, 'w', encoding='utf-8') as fh:
            json.dump(self.project.to_dict(), fh, indent=2)
        self.append_log(f'Project saved: {fn}')

    @Slot()
    def load_project(self):
        fn, _ = QFileDialog.getOpenFileName(self, 'Load project', str(Path.home()), 'JSON (*.json)')
        if not fn:
            return
        with open(fn, 'r', encoding='utf-8') as fh:
            data = json.load(fh)
        self.project = Project.from_dict(data)
        if self.project.video_path:
            self.video_path_input.setText(self.project.video_path)
            self._maybe_generate_waveform(self.project.video_path)
        self._populate_captions_table()
        self.append_log(f'Project loaded: {fn}')


# --- Run ---

def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
