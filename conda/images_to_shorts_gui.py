import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image
import imageio.v2 as imageio
import numpy as np
import cv2
import threading
import os

from moviepy.editor import VideoFileClip, AudioFileClip
from moviepy.audio.fx.all import audio_loop  # FIXED

# =========================
# CONFIG
# =========================
VIDEO_SECONDS = 60
VIDEO_FPS = 24
TOTAL_FRAMES = VIDEO_SECONDS * VIDEO_FPS

EXPORT_WIDTH = 1088
EXPORT_HEIGHT = 1920


# =========================
# FIT IMAGE TO 9:16
# =========================
def fit_to_vertical(img: Image.Image) -> Image.Image:
    img_ratio = img.width / img.height
    target_ratio = EXPORT_WIDTH / EXPORT_HEIGHT

    if img_ratio > target_ratio:
        new_height = img.height
        new_width = int(new_height * target_ratio)
    else:
        new_width = img.width
        new_height = int(new_width / target_ratio)

    left = (img.width - new_width) // 2
    top = (img.height - new_height) // 2
    right = left + new_width
    bottom = top + new_height

    img = img.crop((left, top, right, bottom))
    return img.resize((EXPORT_WIDTH, EXPORT_HEIGHT))


# =========================
# TEXT OVERLAY
# =========================
def add_text_overlay(frame: np.ndarray, text: str, frame_index: int) -> np.ndarray:
    if not text:
        return frame

    h, w, _ = frame.shape
    y = int(h * 0.9 + 20 * np.sin(frame_index / 12))

    bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    overlay = bgr.copy()

    cv2.putText(
        overlay,
        text,
        (int(w * 0.1), y),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.2,
        (255, 255, 255),
        3,
        cv2.LINE_AA
    )

    blended = cv2.addWeighted(overlay, 0.7, bgr, 0.3, 0)
    return cv2.cvtColor(blended, cv2.COLOR_BGR2RGB)


# =========================
# GUI APP
# =========================
class ImagesToShortsGUI:
    def __init__(self, root):
        self.root = root
        root.title("Images → YouTube Shorts Maker")
        root.geometry("560x320")
        root.resizable(False, False)

        self.images_folder = None
        self.audio_path = None

        tk.Button(root, text="Select Images Folder", command=self.select_images_folder).pack(pady=5)
        tk.Button(root, text="Select MP3 (optional)", command=self.select_audio).pack(pady=5)

        text_frame = tk.Frame(root)
        text_frame.pack(pady=5)

        tk.Label(text_frame, text="Overlay Text:").pack(side=tk.LEFT, padx=5)
        self.text_entry = tk.Entry(text_frame, width=30)
        self.text_entry.insert(0, "Follow for more ✨")
        self.text_entry.pack(side=tk.LEFT)

        tk.Button(root, text="Create Shorts Video", command=self.start_thread).pack(pady=10)

        self.progress = ttk.Progressbar(root, length=440)
        self.progress.pack(pady=10)

        self.status = tk.Label(root, text="Waiting...", fg="blue")
        self.status.pack(pady=5)

    # ---- Safe UI Updates ----
    def ui(self, text=None, value=None, color=None):
        def _update():
            if text: self.status.config(text=text)
            if value is not None: self.progress["value"] = value
            if color: self.status.config(fg=color)
        self.root.after(0, _update)

    def select_images_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.images_folder = folder
            self.ui("Images folder selected ✔", 0, "green")

    def select_audio(self):
        path = filedialog.askopenfilename(filetypes=[("MP3", "*.mp3")])
        if path:
            self.audio_path = path
            self.ui("MP3 selected ✔", None, "green")

    def start_thread(self):
        threading.Thread(target=self.build_video, daemon=True).start()

    # =========================
    # MAIN BUILDER
    # =========================
    def build_video(self):
        if not self.images_folder:
            self.ui("Select images folder first ❌", None, "red")
            return

        images = sorted(
            f for f in os.listdir(self.images_folder)
            if f.lower().endswith(("jpg", "jpeg", "png"))
        )

        if not images:
            self.ui("No images found ❌", None, "red")
            return

        save_path = filedialog.asksaveasfilename(
            defaultextension=".mp4",
            filetypes=[("MP4 Video", "*.mp4")]
        )
        if not save_path:
            return

        temp_path = save_path + ".temp.mp4"

        # ---- Process images ----
        self.ui("Loading & resizing images...", 0, "orange")

        pil_images = []
        for im_name in images:
            try:
                img = Image.open(os.path.join(self.images_folder, im_name)).convert("RGB")
                img = fit_to_vertical(img)
                pil_images.append(img)
            except Exception as e:
                print("Error loading image:", e)

        if not pil_images:
            self.ui("No valid images ❌", None, "red")
            return

        num_images = len(pil_images)
        frames_per_img = max(1, TOTAL_FRAMES // num_images)

        writer = imageio.get_writer(
            temp_path,
            fps=VIDEO_FPS,
            codec="libx264",
            ffmpeg_params=["-preset", "fast", "-crf", "23"]
        )

        overlay_text = self.text_entry.get().strip()
        total = 0
        frame_index = 0

        self.ui("Rendering frames...", 0, "orange")

        # ---- Build frames ----
        for img in pil_images:
            base = np.array(img)
            for _ in range(frames_per_img):
                if total >= TOTAL_FRAMES:
                    break
                frame = add_text_overlay(base, overlay_text, frame_index)
                writer.append_data(frame)

                total += 1
                frame_index += 1
                self.ui(value=(total / TOTAL_FRAMES) * 70)

        # pad if short
        while total < TOTAL_FRAMES:
            base = np.array(pil_images[-1])
            frame = add_text_overlay(base, overlay_text, frame_index)
            writer.append_data(frame)
            total += 1
            frame_index += 1
            self.ui(value=(total / TOTAL_FRAMES) * 70)

        writer.close()

        # ---- Add audio (optional) ----
        if self.audio_path:
            try:
                self.ui("Attaching audio...", 85, "orange")
                video = VideoFileClip(temp_path)
                audio = AudioFileClip(self.audio_path)

                if audio.duration > VIDEO_SECONDS:
                    audio = audio.subclip(0, VIDEO_SECONDS)
                else:
                    audio = audio_loop(audio, duration=VIDEO_SECONDS)

                final = video.set_audio(audio)
                final.write_videofile(save_path, codec="libx264", audio_codec="aac")

                video.close()
                final.close()
                audio.close()
                os.remove(temp_path)

            except Exception as e:
                print("Audio attach error:", e)
                os.rename(temp_path, save_path)

        else:
            os.rename(temp_path, save_path)

        self.ui("✔ Shorts video created!", 100, "green")


if __name__ == "__main__":
    root = tk.Tk()
    app = ImagesToShortsGUI(root)
    root.mainloop()
