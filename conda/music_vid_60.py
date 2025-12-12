import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk, ImageEnhance
import imageio
import numpy as np
import cv2
import threading
from moviepy.editor import VideoFileClip, AudioFileClip
import os

# =========================
# VERTICAL SHORTS CONFIG
# =========================
VIDEO_SECONDS = 60
VIDEO_FPS = 24
TOTAL_FRAMES = VIDEO_SECONDS * VIDEO_FPS  # 1440 frames

EXPORT_WIDTH = 1080
EXPORT_HEIGHT = 1920   # 9:16 Vertical Shorts
PREVIEW_SIZE = 360

BASE_EFFECTS = 50
FRAMES_PER_EFFECT = TOTAL_FRAMES // BASE_EFFECTS


# =========================
# EFFECT GENERATOR
# =========================
def generate_effects():
    effects = []
    for i in range(BASE_EFFECTS):
        t = i / (BASE_EFFECTS - 1)

        brightness = 0.2 + (t * 2.2)
        contrast   = 0.3 + (t * 2.4)
        saturation = 0.0 + (t * 3.5)
        warmth     = -120 + int(t * 240)   # shift color balance
        invert     = i % 12 == 0           # periodic inversion

        effects.append((brightness, contrast, saturation, warmth, invert))
    return effects


# =========================
# EFFECT APPLICATION
# =========================
def apply_effect(img, b, c, s, warmth, invert):
    img = ImageEnhance.Brightness(img).enhance(b)
    img = ImageEnhance.Contrast(img).enhance(c)
    img = ImageEnhance.Color(img).enhance(s)

    frame = np.array(img, dtype=np.int16)

    # Warm/cool shift: (R += warmth, B -= warmth)
    frame[..., 0] = np.clip(frame[..., 0] + warmth, 0, 255)
    frame[..., 2] = np.clip(frame[..., 2] - warmth, 0, 255)

    if invert:
        frame = 255 - frame

    return frame.astype(np.uint8)


# =========================
# VERTICAL FIT
# =========================
def fit_to_vertical(img):
    img_ratio = img.width / img.height
    target_ratio = EXPORT_WIDTH / EXPORT_HEIGHT

    if img_ratio > target_ratio:
        new_width = int(img.height * target_ratio)
        new_height = img.height
    else:
        new_width = img.width
        new_height = int(img.width / target_ratio)

    left = (img.width - new_width) // 2
    top = (img.height - new_height) // 2

    img = img.crop((left, top, left + new_width, top + new_height))
    return img.resize((EXPORT_WIDTH, EXPORT_HEIGHT))


# =========================
# MAIN APPLICATION
# =========================
class FiftyShadesVertical:
    def __init__(self, root):
        self.root = root
        self.root.title("50 Shades – 60s Vertical Shorts Generator")
        self.root.geometry("520x780")
        self.root.resizable(False, False)

        self.image = None
        self.preview_image = None
        self.audio_path = None

        self.preview_label = tk.Label(root)
        self.preview_label.pack(pady=15)

        tk.Button(root, text="Load Image", command=self.load_image).pack(pady=6)
        tk.Button(root, text="Add MP3 Music", command=self.load_audio).pack(pady=6)
        tk.Button(root, text="Preview Effects", command=self.preview).pack(pady=6)
        tk.Button(root, text="Export 60s Vertical MP4", command=self.export_threaded).pack(pady=6)

        self.progress = ttk.Progressbar(root, length=420)
        self.progress.pack(pady=15)

        self.status = tk.Label(root, text="Waiting for image...", fg="blue")
        self.status.pack(pady=10)

    # -------------------------
    def load_image(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg")])
        if not path:
            return

        self.image = Image.open(path).convert("RGB")

        self.preview_image = self.image.copy()
        self.preview_image.thumbnail((PREVIEW_SIZE, PREVIEW_SIZE))

        tk_img = ImageTk.PhotoImage(self.preview_image)
        self.preview_label.configure(image=tk_img)
        self.preview_label.image = tk_img

        self.status.config(text="Image loaded ✅", fg="green")

    # -------------------------
    def load_audio(self):
        path = filedialog.askopenfilename(filetypes=[("Audio", "*.mp3")])
        if path:
            self.audio_path = path
            self.status.config(text="MP3 loaded ✅", fg="green")

    # -------------------------
    def preview(self):
        if not self.image:
            self.status.config(text="Load an image first ❌", fg="red")
            return

        effects = generate_effects()
        self.status.config(text="Previewing effects...", fg="orange")

        for b, c, s, w, inv in effects:
            frame = apply_effect(self.preview_image, b, c, s, w, inv)
            tk_frame = ImageTk.PhotoImage(Image.fromarray(frame))
            self.preview_label.configure(image=tk_frame)
            self.preview_label.image = tk_frame

            self.root.update()
            self.root.after(70)

        self.status.config(text="Preview complete ✅", fg="green")

    # -------------------------
    def export_threaded(self):
        threading.Thread(target=self.export_video, daemon=True).start()

    # -------------------------
    def export_video(self):
        if not self.image:
            self.status.config(text="Load an image first ❌", fg="red")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".mp4")
        if not save_path:
            return

        temp_path = "temp_vertical_no_audio.mp4"

        self.status.config(text="Rendering 60s Vertical MP4...", fg="orange")
        self.progress["value"] = 0
        self.root.update()

        base_img = fit_to_vertical(self.image)
        effects = generate_effects()

        # Safe ffmpeg writer
        writer = imageio.get_writer(temp_path, fps=VIDEO_FPS, codec="libx264")

        total_written = 0
        last_frame = None

        for i in range(len(effects) - 1):
            params1 = effects[i]
            params2 = effects[i + 1]

            frame_a = apply_effect(base_img, *params1)
            frame_b = apply_effect(base_img, *params2)

            blends = blend_frames(frame_a, frame_b, FRAMES_PER_EFFECT)

            for frame in blends:
                writer.append_data(frame)
                last_frame = frame
                total_written += 1

                self.progress["value"] = (total_written / TOTAL_FRAMES) * 100
                self.root.update()

        # pad video to exact 1440 frames (MoviePy requires exact duration)
        while total_written < TOTAL_FRAMES:
            writer.append_data(last_frame)
            total_written += 1

        writer.close()

        # -------------------------
        # ADD MUSIC (Optional)
        # -------------------------
        if self.audio_path:
            self.status.config(text="Adding MP3 music...", fg="orange")
            self.root.update()

            video_clip = VideoFileClip(temp_path)
            audio_clip = AudioFileClip(self.audio_path)

            # trim or loop audio
            if audio_clip.duration > VIDEO_SECONDS:
                audio_clip = audio_clip.subclip(0, VIDEO_SECONDS)
            else:
                audio_clip = audio_clip.audio_loop(duration=VIDEO_SECONDS)

            final = video_clip.set_audio(audio_clip)
            final.write_videofile(save_path, fps=VIDEO_FPS, codec="libx264", audio_codec="aac")

            video_clip.close()
            audio_clip.close()
            os.remove(temp_path)
        else:
            os.rename(temp_path, save_path)

        self.progress["value"] = 100
        self.status.config(text="✅ 60s Vertical Video Exported!", fg="green")


# =========================
# RUN APP
# =========================
root = tk.Tk()
app = FiftyShadesVertical(root)
root.mainloop()
