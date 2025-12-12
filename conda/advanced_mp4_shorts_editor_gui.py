#!/usr/bin/env python3
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import threading
import os
import math
import tempfile
import uuid
import shutil

import cv2
import numpy as np
from PIL import Image
import imageio.v2 as imageio

from moviepy.editor import VideoFileClip, AudioFileClip
from moviepy.audio.fx.all import audio_loop


# =========================
# CONFIG
# =========================
VERTICAL_W = 1080   # phone-friendly width
VERTICAL_H = 1920   # phone-friendly height


# =========================
# IMAGE FIT FOR SHORTS
# =========================
def crop_to_vertical(frame):
    # frame is numpy array in RGB (moviepy returns RGB)
    h, w, _ = frame.shape
    target_ratio = VERTICAL_W / VERTICAL_H
    current_ratio = w / h

    if current_ratio > target_ratio:
        # too wide -> crop width
        new_w = int(h * target_ratio)
        x1 = (w - new_w) // 2
        frame = frame[:, x1:x1 + new_w]
    else:
        # too tall -> crop height
        new_h = int(w / target_ratio)
        y1 = (h - new_h) // 2
        frame = frame[y1:y1 + new_h, :]

    # resize to exact target
    return cv2.resize(frame, (VERTICAL_W, VERTICAL_H))


# =========================
# TEXT BAR OVERLAY
# =========================
def add_caption_bars(frame, top_text, bottom_text):
    # frame is RGB numpy array; convert to BGR for OpenCV drawing then back
    bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    h, w, _ = bgr.shape
    bar_h = int(h * 0.12)

    overlay = bgr.copy()

    # Top bar
    cv2.rectangle(overlay, (0, 0), (w, bar_h), (0, 0, 0), -1)
    cv2.putText(
        overlay, str(top_text)[:80],
        (int(w * 0.03), int(bar_h * 0.65)),
        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2, cv2.LINE_AA
    )

    # Bottom bar
    cv2.rectangle(overlay, (0, h - bar_h), (w, h), (0, 0, 0), -1)
    cv2.putText(
        overlay, str(bottom_text)[:80],
        (int(w * 0.03), int(h - bar_h * 0.35)),
        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2, cv2.LINE_AA
    )

    # blend overlay with original
    blended = cv2.addWeighted(overlay, 0.75, bgr, 0.25, 0)

    # convert back to RGB
    return cv2.cvtColor(blended, cv2.COLOR_BGR2RGB)


# =========================
# UTIL: check ffmpeg available
# =========================
def check_ffmpeg():
    try:
        import subprocess
        res = subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return res.returncode == 0
    except Exception:
        return False


# =========================
# MAIN GUI
# =========================
class MP4ShortsEditor:
    def __init__(self, root):
        self.root = root
        root.title("Advanced MP4 Shorts Editor")
        root.geometry("760x560")
        root.resizable(False, False)

        self.video_path = None
        self.audio_path = None

        # top frame for file selection
        topf = tk.Frame(root)
        topf.pack(pady=6, fill="x")

        tk.Button(topf, text="Select MP4 Video", command=self.select_video, width=18).grid(row=0, column=0, padx=6)
        tk.Button(topf, text="Select MP3 (optional)", command=self.select_audio, width=18).grid(row=0, column=1, padx=6)

        # --- PRESET TRIM ---
        preset_frame = tk.Frame(root)
        preset_frame.pack(pady=6, fill="x")

        tk.Label(preset_frame, text="Trim Preset:").grid(row=0, column=0, sticky="w")
        self.trim_var = tk.StringVar(value="60")

        for i, txt in enumerate(["15", "30", "60", "Custom"]):
            tk.Radiobutton(preset_frame, text=txt, value=txt, variable=self.trim_var).grid(row=0, column=i+1, padx=6)

        # --- CUSTOM TRIM ---
        custom_frame = tk.Frame(root)
        custom_frame.pack(pady=4, fill="x")
        tk.Label(custom_frame, text="Custom Start (s)").grid(row=0, column=0, sticky="w")
        self.start_entry = tk.Entry(custom_frame, width=8)
        self.start_entry.insert(0, "0")
        self.start_entry.grid(row=0, column=1, padx=4)

        tk.Label(custom_frame, text="Custom End (s)").grid(row=0, column=2, sticky="w")
        self.end_entry = tk.Entry(custom_frame, width=8)
        self.end_entry.grid(row=0, column=3, padx=4)

        # --- TEXT BARS ---
        text_frame = tk.Frame(root)
        text_frame.pack(pady=6, fill="x")

        tk.Label(text_frame, text="Top Bar Text").grid(row=0, column=0, sticky="w")
        self.top_text = tk.Entry(text_frame, width=56)
        self.top_text.insert(0, "TOP CAPTION")
        self.top_text.grid(row=0, column=1, padx=6)

        tk.Label(text_frame, text="Bottom Bar Text").grid(row=1, column=0, sticky="w")
        self.bottom_text = tk.Entry(text_frame, width=56)
        self.bottom_text.insert(0, "FOLLOW FOR MORE")
        self.bottom_text.grid(row=1, column=1, padx=6, pady=4)

        # --- OPTIONS ---
        options = tk.Frame(root)
        options.pack(pady=6, fill="x")

        self.strip_audio = tk.BooleanVar(value=True)
        self.fade_audio = tk.BooleanVar(value=True)
        self.loop_audio = tk.BooleanVar(value=False)
        self.vertical_crop = tk.BooleanVar(value=True)

        tk.Checkbutton(options, text="Strip original audio", variable=self.strip_audio).grid(row=0, column=0, sticky="w", padx=6)
        tk.Checkbutton(options, text="Audio fade in/out", variable=self.fade_audio).grid(row=0, column=1, sticky="w", padx=6)
        tk.Checkbutton(options, text="Loop audio to match video", variable=self.loop_audio).grid(row=1, column=0, sticky="w", padx=6)
        tk.Checkbutton(options, text="Vertical Shorts crop 9:16", variable=self.vertical_crop).grid(row=1, column=1, sticky="w", padx=6)

        # --- ACTION ---
        action_frame = tk.Frame(root)
        action_frame.pack(pady=10)
        tk.Button(action_frame, text="Process & Export", command=self.start_thread, width=20).pack()

        # progress/status
        self.progress = ttk.Progressbar(root, length=700)
        self.progress.pack(pady=6)

        self.status = tk.Label(root, text="Waiting...", fg="blue")
        self.status.pack()

        # check ffmpeg early
        if not check_ffmpeg():
            messagebox.showwarning("FFmpeg missing", "FFmpeg not found. Please install ffmpeg (conda: conda install -c conda-forge ffmpeg).")

    def ui(self, text=None, value=None, color=None):
        def _u():
            if text is not None:
                self.status.config(text=text)
            if value is not None:
                try:
                    self.progress["value"] = value
                except Exception:
                    pass
            if color is not None:
                self.status.config(fg=color)
        self.root.after(0, _u)

    def select_video(self):
        p = filedialog.askopenfilename(filetypes=[("MP4", "*.mp4"), ("All", "*.*")])
        if p:
            self.video_path = p
            self.ui("Video loaded ✅", 0, "green")

    def select_audio(self):
        p = filedialog.askopenfilename(filetypes=[("MP3/WAV", "*.mp3;*.wav"), ("All", "*.*")])
        if p:
            self.audio_path = p
            self.ui("Audio loaded ✅", None, "green")

    def start_thread(self):
        t = threading.Thread(target=self.process_video, daemon=True)
        t.start()

    def process_video(self):
        try:
            if not self.video_path:
                self.ui("Please select MP4 ❌", None, "red")
                return

            save_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4", "*.mp4")])
            if not save_path:
                self.ui("Cancelled", None, "orange")
                return

            self.ui("Loading video...", 5, "orange")
            clip = VideoFileClip(self.video_path)
            duration = clip.duration or 0.0

            # --- TRIM LOGIC ---
            if self.trim_var.get() != "Custom":
                # preset values represent desired output length in seconds; we trim to that many seconds from start
                preset = float(self.trim_var.get())
                start_time = 0.0
                end_time = min(preset, duration)
            else:
                try:
                    start_time = max(0.0, float(self.start_entry.get() or 0))
                    end_time = min(duration, float(self.end_entry.get()) if self.end_entry.get() else duration)
                    if end_time <= start_time:
                        raise ValueError("End time must be greater than start time.")
                except Exception as e:
                    clip.close()
                    self.ui(f"Invalid trim times: {e}", None, "red")
                    return

            # create trimmed clip (moviepy)
            trimmed = clip.subclip(start_time, end_time)

            # --- FRAME PROCESSING ---
            self.ui("Rendering frames & applying captions...", 20, "orange")
            tmp_dir = tempfile.mkdtemp(prefix="mp4shorts_")
            tmp_video = os.path.join(tmp_dir, f"{uuid.uuid4().hex}.mp4")

            # Use imageio writer (ffmpeg-backed); ensure RGB frames are provided
            fps = getattr(trimmed, "fps", 30) or 30
            writer = None
            try:
                writer = imageio.get_writer(tmp_video, fps=fps, codec="libx264",
                                            ffmpeg_params=["-preset", "fast", "-crf", "23"])
            except Exception as e:
                trimmed.close()
                clip.close()
                shutil.rmtree(tmp_dir, ignore_errors=True)
                self.ui(f"Could not open video writer: {e}", None, "red")
                return

            frame_count = 0
            total_frames = math.ceil((end_time - start_time) * fps) if fps > 0 else None
            try:
                for frame in trimmed.iter_frames(dtype="uint8", progress_bar=False):
                    # MoviePy yields RGB frames
                    if self.vertical_crop.get():
                        frame = crop_to_vertical(frame)

                    frame = add_caption_bars(frame, self.top_text.get(), self.bottom_text.get())
                    writer.append_data(frame)

                    frame_count += 1
                    if total_frames:
                        percent = 20 + int(60 * (frame_count / total_frames))  # map to 20..80
                        self.ui(None, percent)

            except Exception as e:
                self.ui(f"Frame rendering error: {e}", None, "red")
                try:
                    writer.close()
                except:
                    pass
                trimmed.close()
                clip.close()
                shutil.rmtree(tmp_dir, ignore_errors=True)
                return
            finally:
                try:
                    if writer:
                        writer.close()
                except:
                    pass
                try:
                    trimmed.close()
                except:
                    pass
                try:
                    clip.close()
                except:
                    pass

            self.ui("Frame rendering complete", 80, "orange")

            # open the temporary video as a clip for audio composition & final export
            final_clip = VideoFileClip(tmp_video)

            # --- AUDIO ---
            if self.audio_path:
                self.ui("Processing audio...", 85, "orange")
                try:
                    audio = AudioFileClip(self.audio_path)
                except Exception as e:
                    final_clip.close()
                    shutil.rmtree(tmp_dir, ignore_errors=True)
                    self.ui(f"Error loading audio: {e}", None, "red")
                    return

                # If audio longer than video, trim; if shorter and user wants loop, loop it
                if audio.duration > final_clip.duration:
                    audio = audio.subclip(0, final_clip.duration)
                else:
                    if self.loop_audio.get():
                        try:
                            audio = audio_loop(audio, duration=final_clip.duration)
                        except Exception:
                            # fallback: set duration (silence might be appended by ffmpeg)
                            try:
                                audio = audio.set_duration(final_clip.duration)
                            except Exception:
                                pass
                    else:
                        audio = audio.set_duration(min(audio.duration, final_clip.duration))

                if self.fade_audio.get():
                    try:
                        audio = audio.audio_fadein(0.7).audio_fadeout(0.7)
                    except Exception:
                        pass

                try:
                    final_clip = final_clip.set_audio(audio)
                except Exception as e:
                    self.ui(f"Could not attach audio: {e}", None, "red")
                    final_clip.close()
                    shutil.rmtree(tmp_dir, ignore_errors=True)
                    return

            else:
                if self.strip_audio.get():
                    # remove audio
                    try:
                        final_clip = final_clip.without_audio()
                    except Exception:
                        pass

            # --- EXPORT ---
            self.ui("Exporting final video...", 92, "orange")

            try:
                # use moviepy's writer which uses ffmpeg; show progress via a callback is possible but heavy;
                final_clip.write_videofile(save_path, codec="libx264", audio_codec="aac", threads=0, preset="medium")
            except Exception as e:
                self.ui(f"Export failed: {e}", None, "red")
                final_clip.close()
                shutil.rmtree(tmp_dir, ignore_errors=True)
                return
            finally:
                try:
                    final_clip.close()
                except:
                    pass

            # cleanup
            try:
                shutil.rmtree(tmp_dir, ignore_errors=True)
            except:
                pass

            self.ui("✅ Export complete!", 100, "green")

        except Exception as e:
            self.ui(f"Unexpected error: {e}", None, "red")


if __name__ == "__main__":
    root = tk.Tk()
    app = MP4ShortsEditor(root)
    root.mainloop()
