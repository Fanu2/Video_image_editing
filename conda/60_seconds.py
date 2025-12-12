import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk, ImageEnhance
import imageio.v2 as imageio     # ensures compatibility with your environment
import numpy as np
import cv2
import threading

# =========================
# VIDEO CONFIG
# =========================
VIDEO_SECONDS = 60
VIDEO_FPS = 24
TOTAL_FRAMES = VIDEO_SECONDS * VIDEO_FPS  # 1440 frames
EXPORT_SIZE = 1080
PREVIEW_SIZE = 420

BASE_EFFECTS = 50
FRAMES_PER_EFFECT = max(1, TOTAL_FRAMES // BASE_EFFECTS)


# =========================
# EFFECT GENERATION
# =========================
def generate_effects():
    effects = []
    for i in range(BASE_EFFECTS):
        t = i / (BASE_EFFECTS - 1)

        brightness = 0.2 + (t * 2.2)
        contrast   = 0.3 + (t * 2.4)
        saturation = 0.0 + (t * 3.5)
        warmth     = -120 + int(t * 240)
        invert     = i % 12 == 0

        effects.append((brightness, contrast, saturation, warmth, invert))
    return effects


# =========================
# EFFECT APPLICATION
# =========================
def apply_effect(img, b, c, s, warmth, invert):
    img = ImageEnhance.Brightness(img).enhance(b)
    img = ImageEnhance.Contrast(img).enhance(c)
    img = ImageEnhance.Color(img).enhance(s)

    frame = np.array(img).astype(np.int16)

    frame[:, :, 0] = np.clip(frame[:, :, 0] + warmth, 0, 255)
    frame[:, :, 2] = np.clip(frame[:, :, 2] - warmth, 0, 255)

    if invert:
        frame = 255 - frame

    return frame.astype(np.uint8)


def blend_frames(a, b, steps):
    results = []
    steps = max(1, steps)

    for i in range(steps):
        alpha = i / steps
        try:
            blended = cv2.addWeighted(a, 1 - alpha, b, alpha, 0)
        except Exception:
            blended = a  # fallback
        results.append(blended)

    return results


# =========================
# MAIN APPLICATION
# =========================
class FiftyShadesOneMinute:
    def __init__(self, root):
        self.root = root
        self.root.title("50 Shades – 1 Minute Pro Video Generator")
        self.root.geometry("520x720")
        self.root.resizable(False, False)

        self.image = None
        self.preview_image = None

        self.preview_label = tk.Label(root)
        self.preview_label.pack(pady=15)

        tk.Button(root, text="Load Image", command=self.load_image).pack(pady=10)
        tk.Button(root, text="Preview Effects", command=self.preview).pack(pady=10)
        tk.Button(root, text="Export FULL 1-Minute MP4", command=self.export_threaded).pack(pady=10)

        self.progress = ttk.Progressbar(root, length=420)
        self.progress.pack(pady=10)

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
    def preview(self):
        if not self.image:
            self.status.config(text="Load an image first ❌", fg="red")
            return

        effects = generate_effects()

        self.status.config(text="Previewing extreme effects...", fg="orange")
        self.root.update()

        for b, c, s, w, inv in effects:
            frame = apply_effect(self.preview_image, b, c, s, w, inv)
            tk_frame = ImageTk.PhotoImage(Image.fromarray(frame))
            self.preview_label.configure(image=tk_frame)
            self.preview_label.image = tk_frame

            self.root.update_idletasks()
            self.root.after(80)

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

        self.status.config(text="Rendering FULL 60-second MP4...", fg="orange")
        self.progress["value"] = 0
        self.root.update()

        base_img = self.image.resize((EXPORT_SIZE, EXPORT_SIZE))
        effects = generate_effects()

        writer = imageio.get_writer(save_path, fps=VIDEO_FPS)

        total_written = 0

        for i in range(len(effects) - 1):
            b1, c1, s1, w1, inv1 = effects[i]
            b2, c2, s2, w2, inv2 = effects[i + 1]

            frame_a = apply_effect(base_img, b1, c1, s1, w1, inv1)
            frame_b = apply_effect(base_img, b2, c2, s2, w2, inv2)

            blended = blend_frames(frame_a, frame_b, FRAMES_PER_EFFECT)

            for f in blended:
                writer.append_data(f)
                total_written += 1

                self.progress["value"] = (total_written / TOTAL_FRAMES) * 100
                self.root.update_idletasks()

        writer.close()

        self.progress["value"] = 100
        self.status.config(text="✅ FULL 1-Minute 1080p Video Exported!", fg="green")


# =========================
# RUN
# =========================
root = tk.Tk()
app = FiftyShadesOneMinute(root)
root.mainloop()
