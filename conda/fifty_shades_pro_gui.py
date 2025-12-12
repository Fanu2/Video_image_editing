import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk, ImageEnhance
import imageio
import numpy as np
import cv2
import threading
import os

# ==============================
# CONFIG (SAFE + HIGH QUALITY)
# ==============================
FILTER_COUNT = 50
VIDEO_FPS = 24
EXPORT_SIZE = 1080   # 1080x1080 video
PREVIEW_SIZE = 420
TRANSITION_STEPS = 6  # Smooth blending frames


# ==============================
# FILTER GENERATION
# ==============================
def generate_filters():
    filters = []
    for i in range(FILTER_COUNT):
        t = i / (FILTER_COUNT - 1)

        brightness = 0.6 + (t * 0.8)
        contrast = 0.6 + (t * 0.8)
        saturation = 0.4 + (t * 1.4)

        filters.append((brightness, contrast, saturation))
    return filters


# ==============================
# IMAGE PROCESSING
# ==============================
def apply_filter(img, b, c, s):
    img = ImageEnhance.Brightness(img).enhance(b)
    img = ImageEnhance.Contrast(img).enhance(c)
    img = ImageEnhance.Color(img).enhance(s)
    return img


def blend_frames(a, b, steps):
    result = []
    for i in range(steps):
        alpha = i / steps
        blended = cv2.addWeighted(a, 1 - alpha, b, alpha, 0)
        result.append(blended)
    return result


# ==============================
# MAIN APP
# ==============================
class FiftyShadesPro:
    def __init__(self, root):
        self.root = root
        self.root.title("50 Shades Video Generator – Pro Edition")
        self.root.geometry("520x700")
        self.root.resizable(False, False)

        self.image = None
        self.preview_label = tk.Label(root)
        self.preview_label.pack(pady=15)

        tk.Button(root, text="Load Image", command=self.load_image).pack(pady=8)
        tk.Button(root, text="Preview Animation", command=self.preview).pack(pady=8)
        tk.Button(root, text="Export 1080p MP4", command=self.export_threaded).pack(pady=8)

        self.progress = ttk.Progressbar(root, length=400)
        self.progress.pack(pady=15)

        self.status = tk.Label(root, text="Waiting for image...", fg="blue")
        self.status.pack(pady=10)

    # --------------------------
    def load_image(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg")])
        if not path:
            return

        try:
            self.image = Image.open(path).convert("RGB")
        except Exception as e:
            self.status.config(text=f"Failed to load image: {e}", fg="red")
            return

        self.preview_img = self.image.copy()
        self.preview_img.thumbnail((PREVIEW_SIZE, PREVIEW_SIZE))

        tk_img = ImageTk.PhotoImage(self.preview_img)
        self.preview_label.configure(image=tk_img)
        self.preview_label.image = tk_img

        self.status.config(text="Image loaded ✅", fg="green")

    # --------------------------
    def preview(self):
        if self.image is None:
            self.status.config(text="Load an image first ❌", fg="red")
            return

        filters = generate_filters()
        self.status.config(text="Previewing...", fg="orange")

        for b, c, s in filters:
            frame = apply_filter(self.preview_img, b, c, s)
            tk_frame = ImageTk.PhotoImage(frame)
            self.preview_label.configure(image=tk_frame)
            self.preview_label.image = tk_frame
            self.root.update()
            self.root.after(80)

        self.status.config(text="Preview complete ✅", fg="green")

    # --------------------------
    def export_threaded(self):
        thread = threading.Thread(target=self.export_video)
        thread.start()

    # --------------------------
    def export_video(self):
        if self.image is None:
            self.status.config(text="Load an image first ❌", fg="red")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".mp4")
        if not save_path:
            return

        self.progress["value"] = 0
        self.status.config(text="Rendering 1080p video...", fg="orange")

        # Make square HD base
        base = self.image.resize((EXPORT_SIZE, EXPORT_SIZE))

        filters = generate_filters()

        try:
            writer = imageio.get_writer(save_path, fps=VIDEO_FPS)
        except Exception as e:
            self.status.config(text=f"FFmpeg Error: {e}", fg="red")
            return

        prev_frame = None
        frames_written = 0

        for i, (b, c, s) in enumerate(filters):
            processed = apply_filter(base, b, c, s)
            frame = np.array(processed)

            # smooth transition frames
            if prev_frame is not None:
                blends = blend_frames(prev_frame, frame, TRANSITION_STEPS)
                for f in blends:
                    writer.append_data(f)
                    frames_written += 1

            writer.append_data(frame)
            prev_frame = frame
            frames_written += 1

            self.progress["value"] = (i / FILTER_COUNT) * 100
            self.root.update()

        writer.close()

        self.progress["value"] = 100
        self.status.config(text="1080p MP4 Exported ✅", fg="green")


# ==============================
# RUN
# ==============================
root = tk.Tk()
app = FiftyShadesPro(root)
root.mainloop()
