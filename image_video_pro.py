import os
import threading
import tkinter as tk
from tkinter import filedialog, ttk, messagebox

from PIL import Image, ImageDraw, ImageFont
import numpy as np
from moviepy.editor import ImageSequenceClip, AudioFileClip
import subprocess


# ============================
# IMAGE RESIZE
# ============================
def resize_image(path, size):
    img = Image.open(path).convert("RGB")
    return img.resize(size, Image.LANCZOS)


# ============================
# CROSSFADE FRAMES
# ============================
def crossfade(imgA, imgB, steps):
    result = []
    arrA = np.array(imgA)
    arrB = np.array(imgB)

    for t in range(steps):
        alpha = t / steps
        blended = (arrA * (1 - alpha) + arrB * alpha).astype(np.uint8)
        result.append(blended)

    return result


# ============================
# ADD TEXT OVERLAY
# ============================
def apply_text(frame, text, pos, size, color):
    if not text.strip():
        return frame

    img = Image.fromarray(frame)
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("DejaVuSans.ttf", size)
    except:
        font = ImageFont.load_default()

    draw.text(pos, text, fill=color, font=font)
    return np.array(img)


# ============================
# ADD WATERMARK IMAGE
# ============================
def apply_watermark(frame, wm_path, scale=0.2):
    if not wm_path:
        return frame

    img = Image.fromarray(frame)
    wm = Image.open(wm_path).convert("RGBA")

    # scale
    w = int(img.width * scale)
    ratio = w / wm.width
    new_h = int(wm.height * ratio)
    wm = wm.resize((w, new_h), Image.LANCZOS)

    # position bottom right
    x = img.width - wm.width - 20
    y = img.height - wm.height - 20

    img.paste(wm, (x, y), wm)
    return np.array(img)


# ============================
# MAIN GUI
# ============================
class ImageVideoPro:

    def __init__(self, root):
        self.root = root
        root.title("🎬 Image → Video Maker PRO")
        root.geometry("640x780")
        root.resizable(False, False)

        self.folder = None
        self.audio_path = None
        self.watermark_path = None

        # ============================================
        # UI — FILE SELECTION
        # ============================================
        tk.Button(root, text="Select Image Folder", command=self.pick_folder).pack(pady=8)

        tk.Button(root, text="Optional: Select MP3 Audio", command=self.pick_audio).pack(pady=6)

        tk.Button(root, text="Optional: Select Watermark Image", command=self.pick_watermark).pack(pady=6)

        # ============================================
        # FPS
        # ============================================
        fps_frame = tk.Frame(root)
        fps_frame.pack(pady=5)
        tk.Label(fps_frame, text="FPS:").pack(side="left")
        self.fps_entry = tk.Entry(fps_frame, width=6)
        self.fps_entry.insert(0, "24")
        self.fps_entry.pack(side="left")

        # ============================================
        # TRANSITION
        # ============================================
        fade_frame = tk.Frame(root)
        fade_frame.pack()
        tk.Label(fade_frame, text="Crossfade frames between images:").pack(side="left")
        self.fade_entry = tk.Entry(fade_frame, width=6)
        self.fade_entry.insert(0, "8")
        self.fade_entry.pack(side="left", padx=5)

        # ============================================
        # TARGET MODE
        # ============================================
        tk.Label(root, text="Video Shape:").pack()
        self.mode = tk.StringVar(value="horizontal")
        tk.Radiobutton(root, text="Horizontal 1920×1080", variable=self.mode, value="horizontal").pack()
        tk.Radiobutton(root, text="Vertical 1080×1920 (Reels/TikTok)", variable=self.mode, value="vertical").pack()

        # ============================================
        # TEXT OVERLAY
        # ============================================
        tk.Label(root, text="Optional Text Overlay:").pack(pady=5)

        overlay_frame = tk.Frame(root)
        overlay_frame.pack()

        tk.Label(overlay_frame, text="Text:").grid(row=0, column=0)
        self.text_entry = tk.Entry(overlay_frame, width=25)
        self.text_entry.grid(row=0, column=1, padx=5)

        tk.Label(overlay_frame, text="Font Size:").grid(row=1, column=0)
        self.font_size = tk.Entry(overlay_frame, width=6)
        self.font_size.insert(0, "40")
        self.font_size.grid(row=1, column=1)

        # Position
        tk.Label(overlay_frame, text="Text Position (x,y):").grid(row=2, column=0)
        self.pos_x = tk.Entry(overlay_frame, width=5)
        self.pos_x.insert(0, "50")
        self.pos_x.grid(row=2, column=1, sticky="w")

        self.pos_y = tk.Entry(overlay_frame, width=5)
        self.pos_y.insert(0, "50")
        self.pos_y.grid(row=2, column=1, padx=40)

        # ============================================
        # RENDER BUTTON
        # ============================================
        tk.Button(root, text="Create Video", command=self.start_thread, bg="#4477ff", fg="white").pack(pady=15)

        # ============================================
        # PROGRESS
        # ============================================
        self.progress = ttk.Progressbar(root, length=520)
        self.progress.pack(pady=10)

        self.status = tk.Label(root, text="Waiting…", fg="blue")
        self.status.pack()

    # =================================================================
    def pick_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder = folder
            self.status.config(text="Images folder selected ✓", fg="green")

    def pick_audio(self):
        path = filedialog.askopenfilename(filetypes=[("MP3", "*.mp3")])
        if path:
            self.audio_path = path
            self.status.config(text="MP3 selected ✓", fg="green")

    def pick_watermark(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg")])
        if path:
            self.watermark_path = path
            self.status.config(text="Watermark selected ✓", fg="green")

    # =================================================================
    def start_thread(self):
        threading.Thread(target=self.build_video_safe, daemon=True).start()

    def build_video_safe(self):
        try:
            self.build_video()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status.config(text="Error ❌", fg="red")

    # =================================================================
    def build_video(self):

        if not self.folder:
            raise ValueError("Select an image folder first!")

        fps = int(self.fps_entry.get())
        fade_frames = int(self.fade_entry.get())

        images = sorted([
            os.path.join(self.folder, f)
            for f in os.listdir(self.folder)
            if f.lower().endswith((".png", ".jpg", ".jpeg"))
        ])

        if not images:
            raise ValueError("No images found!")

        # Output path
        save_path = filedialog.asksaveasfilename(defaultextension=".mp4")
        if not save_path:
            return

        # Determine resolution
        if self.mode.get() == "horizontal":
            size = (1920, 1080)
        else:
            size = (1080, 1920)

        self.status.config(text="Processing images…")
        self.progress["value"] = 5

        frames = []
        total = len(images)

        # Process images + fades
        for idx, img_path in enumerate(images):
            base = resize_image(img_path, size)

            # apply text
            txt = self.text_entry.get()
            pos = (int(self.pos_x.get()), int(self.pos_y.get()))
            fsize = int(self.font_size.get())

            frame = np.array(base)
            frame = apply_text(frame, txt, pos, fsize, (255, 255, 255))

            # watermark
            frame = apply_watermark(frame, self.watermark_path)

            frames.append(frame)

            # crossfade with next image
            if idx < total - 1:
                next_img = resize_image(images[idx + 1], size)
                next_frame = np.array(next_img)
                next_frame = apply_text(next_frame, txt, pos, fsize, (255, 255, 255))
                next_frame = apply_watermark(next_frame, self.watermark_path)

                frames.extend(crossfade(frame, next_frame, fade_frames))

            self.progress["value"] = 5 + (idx / total) * 60
            self.root.update()

        self.status.config(text="Building MP4…")
        self.progress["value"] = 70

        clip = ImageSequenceClip(frames, fps=fps)

        # Add audio if available
        if self.audio_path:
            audio = AudioFileClip(self.audio_path)
            clip = clip.set_audio(audio)

        clip.write_videofile(save_path, codec="libx264")

        self.progress["value"] = 100
        self.status.config(text="Video created successfully ✓", fg="green")

        # Ask to preview
        if messagebox.askyesno("Preview", "Open video now?"):
            subprocess.Popen(["ffplay", save_path])


# ============================
# RUN APP
# ============================
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageVideoPro(root)
    root.mainloop()

