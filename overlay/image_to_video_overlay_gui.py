"""
Image-to-Video Overlay GUI — Stable Rewrite

This is a clean, stable, single-file PySide6 application that:
- Lets you choose a base MP4 video (local) or load from a web URL (yt-dlp, optional)
- Lets you pick a folder containing images (PNG/JPG). Images will be layered over the video
- Applies a vertical alpha gradient mask to each image (top-to-bottom transparency)
- Applies per-image position, scale, fade-in/fade-out, start/end times
- Preview pane for images
- Multi-select + Apply to Selected / Apply to All
- Rendering runs in a background thread so the UI stays responsive

Dependencies:
    pip install PySide6 moviepy Pillow numpy yt-dlp

Requirements:
- ffmpeg must be installed and accessible in PATH.

Usage:
    python image_to_video_overlay_gui.py

Notes:
- This rewrite focuses on stability and clarity. It validates inputs and shows meaningful errors.
- Warning about DBus themes is harmless; the app will still run.
"""

import os
os.environ.setdefault('QT_LOGGING_RULES', '*.debug=false;qt.qpa.theme=false')

import sys
import tempfile
import traceback
from pathlib import Path
from typing import List, Tuple, Optional

from PySide6.QtCore import Qt, Slot, QThread, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QListWidget, QListWidgetItem,
    QDoubleSpinBox, QFormLayout, QLineEdit, QMessageBox, QProgressBar,
    QCheckBox
)

# third-party libs
try:
    from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip
    import moviepy.video.fx.all as vfx
    import numpy as np
    from PIL import Image
except Exception as e:
    print('Missing dependency:', e)
    raise


# ---------- utilities ----------

def generate_vertical_alpha_mask(size: Tuple[int, int], top_alpha: float = 1.0, bottom_alpha: float = 0.0) -> Image.Image:
    w, h = size
    grad = np.linspace(top_alpha, bottom_alpha, h, dtype=np.float32)
    mask_arr = np.tile(grad[:, None], (1, w))
    mask_img = Image.fromarray((mask_arr * 255).astype('uint8'), mode='L')
    return mask_img


def apply_alpha_gradient_to_image(img_path: Path, target_size: Tuple[int, int], top_alpha: float = 1.0, bottom_alpha: float = 0.0) -> Image.Image:
    img = Image.open(img_path).convert('RGBA')
    img = img.resize(target_size, Image.LANCZOS)
    mask = generate_vertical_alpha_mask(target_size, top_alpha, bottom_alpha)
    r, g, b, _ = img.split()
    img_with_alpha = Image.merge('RGBA', (r, g, b, mask))
    return img_with_alpha


# ---------- data model ----------
class OverlayItem:
    def __init__(self, path: Path):
        self.path = path
        self.x = 0.5
        self.y = 0.5
        self.scale = 0.5
        self.top_alpha = 1.0
        self.bottom_alpha = 0.0
        self.start = 0.0
        self.end = None
        self.fade_in = 0.5
        self.fade_out = 0.5


# ---------- rendering worker ----------
class RenderWorker(QThread):
    log = Signal(str)
    progress = Signal(int)
    finished = Signal(str)
    error = Signal(str)

    def __init__(self, video_path: Path, overlays: List[OverlayItem], output_path: Path, parent=None):
        super().__init__(parent)
        self.video_path = video_path
        self.overlays = overlays
        self.output_path = output_path

    def run(self):
        try:
            self.log.emit('Opening video...')
            clip = VideoFileClip(str(self.video_path))
            video_w, video_h = clip.size
            duration = clip.duration
            self.log.emit(f'Video: {video_w}x{video_h}, duration {duration:.2f}s')

            clips = [clip]
            total = len(self.overlays)
            for idx, ov in enumerate(self.overlays, start=1):
                self.log.emit(f'Preparing overlay {idx}/{total}: {ov.path.name}')
                # compute target width preserving aspect
                target_w = max(1, int(video_w * ov.scale))
                with Image.open(ov.path) as im:
                    ow, oh = im.size
                    target_h = max(1, int(target_w * oh / ow))
                img_alpha = apply_alpha_gradient_to_image(ov.path, (target_w, target_h), ov.top_alpha, ov.bottom_alpha)
                img_clip = ImageClip(np.asarray(img_alpha)).set_duration(duration)

                pos_x = int(video_w * ov.x)
                pos_y = int(video_h * ov.y)

                def pos_func(t, px=pos_x, py=pos_y, w=target_w, h=target_h):
                    return (px - w // 2, py - h // 2)

                img_clip = img_clip.set_position(pos_func)
                # Create proper grayscale 0–1 mask for MoviePy
                mask_arr = np.asarray(img_alpha.split()[-1]) / 255.0
                mask_clip = ImageClip(mask_arr, ismask=True).set_duration(duration).set_position(pos_func)
                img_clip = img_clip.set_mask(mask_clip)

                start = float(ov.start or 0.0)
                end = float(ov.end) if ov.end not in (None, 0.0) else duration
                img_clip = img_clip.set_start(start).set_end(end)

                if ov.fade_in and ov.fade_in > 0:
                    img_clip = vfx.fadein(img_clip, ov.fade_in)
                if ov.fade_out and ov.fade_out > 0:
                    img_clip = vfx.fadeout(img_clip, ov.fade_out)

                clips.append(img_clip)
                pct = int((idx / total) * 80)
                self.progress.emit(pct)

            final = CompositeVideoClip(clips)
            self.progress.emit(85)
            self.log.emit('Rendering to file...')
            # write_videofile is blocking; run in this thread
            final.write_videofile(str(self.output_path), codec='libx264', audio_codec='aac', threads=0, logger=None)
            self.progress.emit(100)
            self.finished.emit(str(self.output_path))
        except Exception as e:
            tb = traceback.format_exc()
            self.error.emit(f'{e}\n{tb}')


# ---------- main GUI ----------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Image-to-Video Overlay — Stable')
        self.resize(1000, 700)

        self.video_path: Optional[Path] = None
        self.image_items: List[OverlayItem] = []
        self.output_path: Optional[Path] = None
        self.worker: Optional[RenderWorker] = None

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)

        # top controls
        top_layout = QHBoxLayout()
        self.open_video_btn = QPushButton('Open Video')
        self.open_video_btn.clicked.connect(self.open_video)
        self.load_url_input = QLineEdit(); self.load_url_input.setPlaceholderText('Paste video URL (optional)')
        self.load_url_btn = QPushButton('Load URL')
        self.load_url_btn.clicked.connect(self.load_video_from_url)
        self.open_images_btn = QPushButton('Open Images Folder')
        self.open_images_btn.clicked.connect(self.open_images_folder)
        self.select_output_btn = QPushButton('Select Output')
        self.select_output_btn.clicked.connect(self.select_output)
        top_layout.addWidget(self.open_video_btn)
        top_layout.addWidget(self.load_url_input)
        top_layout.addWidget(self.load_url_btn)
        top_layout.addWidget(self.open_images_btn)
        top_layout.addWidget(self.select_output_btn)
        main_layout.addLayout(top_layout)

        # middle split
        mid_layout = QHBoxLayout()

        left_col = QVBoxLayout()
        self.images_list = QListWidget()
        self.images_list.setSelectionMode(QListWidget.MultiSelection)
        self.images_list.currentItemChanged.connect(self.image_selection_changed)
        left_col.addWidget(QLabel('Images (multi-select)'))
        left_col.addWidget(self.images_list)

        self.timeline_list = QListWidget()
        left_col.addWidget(QLabel('Timeline'))
        left_col.addWidget(self.timeline_list)

        mid_layout.addLayout(left_col, 2)

        # right column props + preview
        right_col = QVBoxLayout()
        props = QWidget(); props_layout = QFormLayout(props)
        self.pos_x_spin = QDoubleSpinBox(); self.pos_x_spin.setRange(0.0, 1.0); self.pos_x_spin.setSingleStep(0.01); self.pos_x_spin.setValue(0.5)
        self.pos_y_spin = QDoubleSpinBox(); self.pos_y_spin.setRange(0.0, 1.0); self.pos_y_spin.setSingleStep(0.01); self.pos_y_spin.setValue(0.5)
        self.scale_spin = QDoubleSpinBox(); self.scale_spin.setRange(0.01, 2.0); self.scale_spin.setSingleStep(0.01); self.scale_spin.setValue(0.5)
        self.top_alpha_spin = QDoubleSpinBox(); self.top_alpha_spin.setRange(0.0, 1.0); self.top_alpha_spin.setSingleStep(0.01); self.top_alpha_spin.setValue(1.0)
        self.bottom_alpha_spin = QDoubleSpinBox(); self.bottom_alpha_spin.setRange(0.0, 1.0); self.bottom_alpha_spin.setSingleStep(0.01); self.bottom_alpha_spin.setValue(0.0)
        self.start_spin = QDoubleSpinBox(); self.start_spin.setRange(0.0, 100000.0); self.start_spin.setSingleStep(0.1); self.start_spin.setValue(0.0)
        self.end_spin = QDoubleSpinBox(); self.end_spin.setRange(0.0, 100000.0); self.end_spin.setSingleStep(0.1); self.end_spin.setValue(0.0)
        self.fade_in_spin = QDoubleSpinBox(); self.fade_in_spin.setRange(0.0, 30.0); self.fade_in_spin.setSingleStep(0.1); self.fade_in_spin.setValue(0.5)
        self.fade_out_spin = QDoubleSpinBox(); self.fade_out_spin.setRange(0.0, 30.0); self.fade_out_spin.setSingleStep(0.1); self.fade_out_spin.setValue(0.5)

        props_layout.addRow('Position X (0..1)', self.pos_x_spin)
        props_layout.addRow('Position Y (0..1)', self.pos_y_spin)
        props_layout.addRow('Scale', self.scale_spin)
        props_layout.addRow('Top alpha', self.top_alpha_spin)
        props_layout.addRow('Bottom alpha', self.bottom_alpha_spin)
        props_layout.addRow('Start (s)', self.start_spin)
        props_layout.addRow('End (s)', self.end_spin)
        props_layout.addRow('Fade-in (s)', self.fade_in_spin)
        props_layout.addRow('Fade-out (s)', self.fade_out_spin)

        self.apply_selected_btn = QPushButton('Apply to Selected')
        self.apply_selected_btn.clicked.connect(self.apply_props_to_selected)
        self.apply_all_btn = QPushButton('Apply to All')
        self.apply_all_btn.clicked.connect(self.apply_props_to_all)
        props_layout.addRow(self.apply_selected_btn, self.apply_all_btn)

        right_col.addWidget(props)

        self.preview_label = QLabel('Preview')
        self.preview_label.setFixedSize(360, 240)
        self.preview_label.setStyleSheet('background: #222; color: #fff;')
        right_col.addWidget(QLabel('Preview'))
        right_col.addWidget(self.preview_label)

        mid_layout.addLayout(right_col, 1)

        main_layout.addLayout(mid_layout)

        # bottom
        bottom = QHBoxLayout()
        self.render_btn = QPushButton('Render Video')
        self.render_btn.clicked.connect(self.on_render_clicked)
        self.progress = QProgressBar(); self.progress.setValue(0)
        bottom.addWidget(self.render_btn)
        bottom.addWidget(self.progress)
        main_layout.addLayout(bottom)

        self.status = QLabel('Ready')
        main_layout.addWidget(self.status)

    # ----- UI actions -----
    @Slot()
    def open_video(self):
        fn, _ = QFileDialog.getOpenFileName(self, 'Open video', str(Path.home()), 'Video files (*.mp4 *.mov *.mkv)')
        if not fn:
            return
        self.video_path = Path(fn)
        self.status.setText(f'Loaded video: {self.video_path}')

    @Slot()
    def load_video_from_url(self):
        url = self.load_url_input.text().strip()
        if not url:
            QMessageBox.warning(self, 'No URL', 'Please paste a video URL')
            return
        try:
            import yt_dlp
            tmp = Path(tempfile.gettempdir()) / 'overlay_url_download.mp4'
            opts = {'outtmpl': str(tmp), 'quiet': True, 'merge_output_format': 'mp4'}
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([url])
            if tmp.exists():
                self.video_path = tmp
                self.status.setText(f'Loaded video from URL: {tmp}')
            else:
                QMessageBox.critical(self, 'Download failed', 'yt-dlp failed to download the URL')
        except Exception as e:
            QMessageBox.critical(self, 'URL error', str(e))

    @Slot()
    def open_images_folder(self):
        folder = QFileDialog.getExistingDirectory(self, 'Select images folder', str(Path.home()))
        if not folder:
            return
        p = Path(folder)
        image_files = sorted([x for x in p.iterdir() if x.suffix.lower() in ('.png', '.jpg', '.jpeg')])
        self.image_items = [OverlayItem(x) for x in image_files]
        self.refresh_images_list()
        self.update_timeline()
        self.status.setText(f'Loaded {len(self.image_items)} images')

    def refresh_images_list(self):
        self.images_list.clear()
        for it in self.image_items:
            item = QListWidgetItem(it.path.name)
            self.images_list.addItem(item)

    @Slot()
    def select_output(self):
        fn, _ = QFileDialog.getSaveFileName(self, 'Select output file', str(Path.home() / 'output.mp4'), 'MP4 Video (*.mp4)')
        if not fn:
            return
        self.output_path = Path(fn)
        self.status.setText(f'Output: {self.output_path}')

    @Slot()
    def image_selection_changed(self, cur: QListWidgetItem, prev: QListWidgetItem):
        if cur is None:
            return
        idx = self.images_list.row(cur)
        it = self.image_items[idx]
        self.pos_x_spin.setValue(it.x)
        self.pos_y_spin.setValue(it.y)
        self.scale_spin.setValue(it.scale)
        self.top_alpha_spin.setValue(it.top_alpha)
        self.bottom_alpha_spin.setValue(it.bottom_alpha)
        self.start_spin.setValue(it.start)
        self.end_spin.setValue(0.0 if it.end is None else it.end)
        self.fade_in_spin.setValue(it.fade_in)
        self.fade_out_spin.setValue(it.fade_out)
        # preview image
        try:
            px = QPixmap(str(it.path))
            if not px.isNull():
                px = px.scaled(self.preview_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.preview_label.setPixmap(px)
        except Exception:
            pass

    @Slot()
    def apply_props_to_selected(self):
        selected = self.images_list.selectedItems()
        if not selected:
            QMessageBox.warning(self, 'No selection', 'Select one or more images first')
            return
        for cur in selected:
            idx = self.images_list.row(cur)
            it = self.image_items[idx]
            it.x = float(self.pos_x_spin.value())
            it.y = float(self.pos_y_spin.value())
            it.scale = float(self.scale_spin.value())
            it.top_alpha = float(self.top_alpha_spin.value())
            it.bottom_alpha = float(self.bottom_alpha_spin.value())
            it.start = float(self.start_spin.value())
            endv = float(self.end_spin.value())
            it.end = None if endv == 0.0 else endv
            it.fade_in = float(self.fade_in_spin.value())
            it.fade_out = float(self.fade_out_spin.value())
        self.status.setText(f'Applied to {len(selected)} images')
        self.update_timeline()

    @Slot()
    def apply_props_to_all(self):
        if not self.image_items:
            QMessageBox.warning(self, 'No images', 'Load images first')
            return
        for it in self.image_items:
            it.x = float(self.pos_x_spin.value())
            it.y = float(self.pos_y_spin.value())
            it.scale = float(self.scale_spin.value())
            it.top_alpha = float(self.top_alpha_spin.value())
            it.bottom_alpha = float(self.bottom_alpha_spin.value())
            it.start = float(self.start_spin.value())
            endv = float(self.end_spin.value())
            it.end = None if endv == 0.0 else endv
            it.fade_in = float(self.fade_in_spin.value())
            it.fade_out = float(self.fade_out_spin.value())
        self.status.setText('Applied to all images')
        self.update_timeline()

    def update_timeline(self):
        self.timeline_list.clear()
        for it in self.image_items:
            start = it.start
            end = it.end if it.end is not None else 0.0
            self.timeline_list.addItem(f"{it.path.name}: {start:.2f} - {('end' if it.end is None else f'{end:.2f}')}")

    # ---------- Render glue ----------
    @Slot()
    def on_render_clicked(self):
        print('Render button clicked')
        if not self.video_path:
            QMessageBox.warning(self, 'No video', 'Load or select a base video first')
            return
        if not self.image_items:
            QMessageBox.warning(self, 'No images', 'Load images folder first')
            return
        if not self.output_path:
            QMessageBox.warning(self, 'No output', 'Select an output file')
            return

        # start worker
        self.render_btn.setEnabled(False)
        self.worker = RenderWorker(self.video_path, self.image_items, self.output_path)
        self.worker.log.connect(lambda s: self.status.setText(s))
        self.worker.progress.connect(self.progress.setValue)
        self.worker.finished.connect(self.on_render_finished)
        self.worker.error.connect(self.on_render_error)
        self.worker.start()

    @Slot(str)
    def on_render_finished(self, outpath: str):
        self.render_btn.setEnabled(True)
        self.status.setText(f'Rendered: {outpath}')
        self.progress.setValue(100)
        QMessageBox.information(self, 'Done', f'Rendered to: {outpath}')

    @Slot(str)
    def on_render_error(self, msg: str):
        self.render_btn.setEnabled(True)
        self.status.setText('Error')
        QMessageBox.critical(self, 'Render error', msg)


# ---------- run ----------
def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
