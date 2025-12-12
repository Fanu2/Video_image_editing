import tkinter as tk
from tkinter import filedialog, ttk
import threading
import numpy as np
import os
from PIL import Image, ImageTk
from moviepy.editor import ImageClip, CompositeVideoClip

# ==============================
# CONFIG
# ==============================
FPS = 24
DURATION = 10           # seconds
FRAMES = FPS * DURATION
RADIUS = 300
PREVIEW_SIZE = 380


# ==============================
# FORCE ANY IMAGE → RGB 3-CHANNEL
# ==============================
def ensure_rgb(frame):
    frame = np.array(frame)

    # If grayscale
    if frame.ndim == 2:
        frame = np.stack([frame] * 3, axis=-1)

    # If RGBA → RGB
    if frame.shape[2] == 4:
        frame = frame[:, :, :3]

    return frame.astype(np.uint8)


# ==============================
# GUI CLASS
# ==============================
class CirclesGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Rotating Circles Video Maker")
        self.root.geometry("600x650")
        self.root.resizable(False, False)

        self.center_image_path = None
        self.rotating_image_paths = []

        # Preview label
        self.preview_label = tk.Label(root)
        self.preview_label.pack(pady=15)

        # Buttons
        tk.Button(root, text="Select Central Image", command=self.select_center).pack(pady=5)
        tk.Button(root, text="Select Rotating Images", command=self.select_rotating).pack(pady=5)
        tk.Button(root, text="Generate Video", command=self.start_thread).pack(pady=10)

        # Progress Bar
        self.progress = ttk.Progressbar(root, length=450)
        self.progress.pack(pady=10)

        # Status label
        self.status = tk.Label(root, text="Waiting...", fg="blue")
        self.status.pack()

    # -----------------------------
    def select_center(self):
        path = filedialog.askopenfilename(filetypes=[("PNG Images", "*.png"), ("JPG", "*.jpg")])
        if path:
            self.center_image_path = path
            img = Image.open(path).convert("RGB")
            img.thumbnail((PREVIEW_SIZE, PREVIEW_SIZE))
            tk_img = ImageTk.PhotoImage(img)
            self.preview_label.configure(image=tk_img)
            self.preview_label.image = tk_img
            self.status.config(text="Central image loaded ✔", fg="green")

    # -----------------------------
    def select_rotating(self):
        paths = filedialog.askopenfilenames(filetypes=[("PNG Images", "*.png"), ("JPG", "*.jpg")])
        if paths:
            self.rotating_image_paths = list(paths)
            self.status.config(text=f"{len(paths)} rotating images loaded ✔", fg="green")

    # -----------------------------
    def start_thread(self):
        t = threading.Thread(target=self.generate_video, daemon=True)
        t.start()

    # -----------------------------
    def generate_video(self):
        if not self.center_image_path:
            self.status.config(text="Select central image ❌", fg="red")
            return
        if not self.rotating_image_paths:
            self.status.config(text="Select rotating images ❌", fg="red")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".mp4")
        if not save_path:
            return

        self.status.config(text="Rendering video...", fg="orange")
        self.progress["value"] = 0
        self.root.update()

        # Load center
        center_img = Image.open(self.center_image_path).convert("RGB")
        W, H = center_img.size
        center_clip = ImageClip(ensure_rgb(center_img)).set_duration(DURATION)

        # Pre-load rotating images
        rot_imgs = [ensure_rgb(Image.open(p).convert("RGB")) for p in self.rotating_image_paths]
        N = len(rot_imgs)
        angle_step = 360 / N

        # Store all generated frames
        frames = []

        # Generate all frames
        for f in range(FRAMES):
            angle_offset = f * (360 / FRAMES)
            frame = ensure_rgb(center_img.copy())

            # Convert to float for compositing
            frame = frame.astype(np.uint8)

            for i, img in enumerate(rot_imgs):
                angle = (i * angle_step + angle_offset) % 360
                rad = np.deg2rad(angle)

                x = int(W/2 + RADIUS * np.cos(rad) - img.shape[1] // 2)
                y = int(H/2 + RADIUS * np.sin(rad) - img.shape[0] // 2)

                # Bound check
                if 0 <= x < W and 0 <= y < H:
                    h, w = img.shape[:2]
                    if y + h < H and x + w < W:
                        frame[y:y+h, x:x+w] = img

            frames.append(frame)

            # Progress update
            self.progress["value"] = (f / FRAMES) * 100
            self.root.update()

        # Convert frames → MoviePy clip
        final = ImageClip(frames[0]).set_duration(DURATION)

        def make_frame(t):
            idx = int(t * FPS)
            if idx >= len(frames):
                idx = len(frames) - 1
            frame = frames[idx]

            # Safety: ensure RGB always
            frame = ensure_rgb(frame)
            return frame

        final = final.set_make_frame(make_frame)

        # Export video
        final.write_videofile(save_path, fps=FPS, codec="libx264")

        self.status.config(text="✔ Video exported successfully!", fg="green")
        self.progress["value"] = 100


# ==============================
# RUN APP
# ==============================
root = tk.Tk()
gui = CirclesGUI(root)
root.mainloop()
