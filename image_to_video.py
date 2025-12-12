import os
import threading
import tkinter as tk
from tkinter import filedialog, ttk, colorchooser, messagebox

import numpy as np
from PIL import Image, ImageFont, ImageDraw

from moviepy.editor import ImageSequenceClip, AudioFileClip


# ============================================================
# ---------- IMAGE UTILITIES
# ============================================================

def load_and_resize(img, target_w, target_h):
    """Load image as PIL and resize for consistent MoviePy frames."""
    img = img.convert("RGB")

    # center crop to match aspect ratio
    src_w, src_h = img.size
    src_ratio = src_w / src_h
    dst_ratio = target_w / target_h

    if src_ratio > dst_ratio:
        # too wide → crop sides
        new_w = int(src_h * dst_ratio)
        x1 = (src_w - new_w) // 2
        img = img.crop((x1, 0, x1 + new_w, src_h))
    else:
        # too tall → crop top/bottom
        new_h = int(src_w / dst_ratio)
        y1 = (src_h - new_h) // 2
        img = img.crop((0, y1, src_w, y1 + new_h))

    return img.resize((target_w, target_h), Image.LANCZOS)


def apply_text(frame, text, color, size, x, y, outline):
    """Draw text onto a numpy frame."""
    img = Image.fromarray(frame)
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", size)
    except:
        font = ImageFont.load_default()

    if outline > 0:
        for ox in range(-outline, outline + 1):
            for oy in range(-outline, outline + 1):
                draw.text((x + ox, y + oy), text, font=font, fill="black")

    draw.text((x, y), text, font=font, fill=color)
    return np.array(img)


def apply_ken_burns(frame, zoom_start, zoom_end, rot_start, rot_end,
                    pan_x_start, pan_x_end, pan_y_start, pan_y_end, t):
    """Apply smooth zoom, rotation, and panning on frame."""

    img = Image.fromarray(frame)
    w, h = img.size

    # smooth values for this frame
    zoom = zoom_start + (zoom_end - zoom_start) * t
    rot = rot_start + (rot_end - rot_start) * t
    px = pan_x_start + (pan_x_end - pan_x_start) * t
    py = pan_y_start + (pan_y_end - pan_y_start) * t

    # zoom
    new_w = int(w * zoom)
    new_h = int(h * zoom)
    img = img.resize((new_w, new_h), Image.LANCZOS)

    # rotate
    img = img.rotate(rot, expand=True)

    # pan crop
    rw, rh = img.size
    cx = int((rw - w) / 2 + px)
    cy = int((rh - h) / 2 + py)

    img = img.crop((cx, cy, cx + w, cy + h))

    # safety → force exact final size
    img = img.resize((w, h), Image.LANCZOS)

    return np.array(img)


# ============================================================
# ---------- GUI APP
# ============================================================

class ImageToVideoApp:

    def __init__(self, root):
        self.root = root
        root.title("Image → Video Pro Editor")
        root.geometry("680x580")
        root.configure(bg="#222222")

        # ------------------------------
        # Variables
        # ------------------------------
        self.images = []
        self.audio = None

        self.fps = tk.IntVar(value=24)
        self.duration = tk.DoubleVar(value=3.0)

        self.text = tk.StringVar(value="")
        self.text_color = "#FFFFFF"
        self.text_size = tk.IntVar(value=48)
        self.text_x = tk.IntVar(value=50)
        self.text_y = tk.IntVar(value=50)
        self.text_outline = tk.IntVar(value=2)

        self.zoom_start = tk.DoubleVar(value=1.00)
        self.zoom_end = tk.DoubleVar(value=1.05)
        self.rot_start = tk.DoubleVar(value=0.0)
        self.rot_end = tk.DoubleVar(value=0.0)
        self.pan_x_start = tk.DoubleVar(value=0.0)
        self.pan_y_start = tk.DoubleVar(value=0.0)
        self.pan_x_end = tk.DoubleVar(value=0.0)
        self.pan_y_end = tk.DoubleVar(value=0.0)

        # ------------------------------
        # UI Layout
        # ------------------------------

        self.make_ui()

    def make_ui(self):

        lbl = tk.Label(self.root, text="Image → Video Tool", fg="white", bg="#222222",
                       font=("Arial", 18))
        lbl.pack(pady=10)

        # File selection
        frm = tk.Frame(self.root, bg="#222222")
        frm.pack()

        tk.Button(frm, text="Select Images", command=self.load_images).grid(row=0, column=0, padx=10, pady=5)
        tk.Button(frm, text="Select Audio", command=self.load_audio).grid(row=0, column=1, padx=10, pady=5)

        # Settings
        st = tk.Frame(self.root, bg="#222222")
        st.pack(pady=5)

        tk.Label(st, text="FPS:", fg="white", bg="#222222").grid(row=0, column=0)
        tk.Entry(st, textvariable=self.fps, width=5).grid(row=0, column=1)

        tk.Label(st, text="Seconds per image:", fg="white", bg="#222222").grid(row=0, column=2)
        tk.Entry(st, textvariable=self.duration, width=5).grid(row=0, column=3)

        tk.Button(st, text="Pick Text Color", command=self.pick_color).grid(row=1, column=0, pady=5)
        tk.Entry(st, textvariable=self.text, width=25).grid(row=1, column=1, columnspan=3, pady=5)

        # Ken Burns controls
        kb = tk.Frame(self.root, bg="#222222")
        kb.pack(pady=5)

        tk.Label(kb, text="Zoom Start", fg="white", bg="#222222").grid(row=0, column=0)
        tk.Entry(kb, textvariable=self.zoom_start, width=5).grid(row=0, column=1)

        tk.Label(kb, text="Zoom End", fg="white", bg="#222222").grid(row=0, column=2)
        tk.Entry(kb, textvariable=self.zoom_end, width=5).grid(row=0, column=3)

        tk.Button(self.root, text="Render Video", command=self.start_render).pack(pady=20)

        self.progress = ttk.Progressbar(self.root, length=450)
        self.progress.pack(pady=10)

        self.status = tk.Label(self.root, text="", fg="lightgray", bg="#222222")
        self.status.pack()

    # ============================================================
    # ---------- FILE LOAD
    # ============================================================

    def load_images(self):
        files = filedialog.askopenfilenames(filetypes=[("Images", "*.png *.jpg *.jpeg")])
        if files:
            self.images = list(files)
            self.status.config(text=f"{len(files)} images loaded")

    def load_audio(self):
        f = filedialog.askopenfilename(filetypes=[("MP3 Audio", "*.mp3")])
        if f:
            self.audio = f
            self.status.config(text="Audio selected")

    def pick_color(self):
        c = colorchooser.askcolor(title="Pick Text Color")
        if c[1] is not None:
            self.text_color = c[1]

    # ============================================================
    # ---------- RENDER THREAD
    # ============================================================

    def start_render(self):
        if not self.images:
            messagebox.showerror("Error", "No images selected.")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".mp4")
        if not save_path:
            return

        t = threading.Thread(target=self._render_safe, args=(save_path,))
        t.start()

    def _render_safe(self, save_path):
        try:
            self._render(save_path)
            self.status.config(text="Done!")
        except Exception as e:
            messagebox.showerror("Render Error", str(e))
            self.status.config(text="ERROR")

    # ============================================================
    # ---------- RENDER LOGIC
    # ============================================================

    def _render(self, save_path):
        fps = self.fps.get()
        duration = self.duration.get()

        # target resolution
        w, h = 1920, 1080

        # Load & resize images
        loaded = []
        for p in self.images:
            img = Image.open(p)
            img = load_and_resize(img, w, h)
            loaded.append(img)
        total = len(loaded)

        total_frames = int(duration * fps * total)
        sequence = []

        # Build frames
        for idx, base_img in enumerate(loaded):
            base_array = np.array(base_img)

            for f in range(int(duration * fps)):
                t = f / (duration * fps - 1)

                frame = apply_ken_burns(
                    base_array,
                    self.zoom_start.get(), self.zoom_end.get(),
                    self.rot_start.get(), self.rot_end.get(),
                    self.pan_x_start.get(), self.pan_x_end.get(),
                    self.pan_y_start.get(), self.pan_y_end.get(),
                    t
                )

                if self.text.get().strip():
                    frame = apply_text(frame,
                                       self.text.get(),
                                       self.text_color,
                                       self.text_size.get(),
                                       self.text_x.get(),
                                       self.text_y.get(),
                                       self.text_outline.get())

                # --- HARD ENFORCEMENT: ensure consistent size ---
                frame = Image.fromarray(frame).resize((w, h), Image.LANCZOS)
                frame = np.array(frame)

                sequence.append(frame)

                self.progress["value"] = (len(sequence) / total_frames) * 100
                self.root.update_idletasks()

        # Build MoviePy clip
        clip = ImageSequenceClip(sequence, fps=fps)

        if self.audio:
            audio = AudioFileClip(self.audio)
            audio = audio.set_duration(clip.duration)
            clip = clip.set_audio(audio)

        clip.write_videofile(save_path, codec="libx264", audio_codec="aac")

        self.status.config(text="Video saved ✔")


# ============================================================
# ---------- MAIN
# ============================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageToVideoApp(root)
    root.mainloop()
