#!/usr/bin/env python3
"""
audio_images_video_maker.py

Create a video from an audio file and a folder of images.
Features:
 - Select audio file (mp3/m4a/wav/...)
 - Select images folder (jpg/png/webp)
 - Presets: TikTok / YouTube / Instagram / Custom
 - FPS selection
 - Target image display time (s) and option to loop images to fill song
 - Text overlay (text, font size, color, position)
 - Crossfade option
 - Non-blocking GUI (worker thread) + progress/status
Dependencies (conda):
    conda install -c conda-forge moviepy pillow numpy ffmpeg
"""
import os
import math
import tempfile
import threading
from queue import Queue, Empty
from pathlib import Path
import platform

import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
from tkinter.ttk import Combobox, Progressbar

from PIL import Image, ImageDraw, ImageFont
import numpy as np
from moviepy.editor import (
    AudioFileClip, ImageClip, concatenate_videoclips, CompositeVideoClip
)

# ---------------------------
# Helpers
# ---------------------------
def get_default_font_path():
    try:
        if platform.system() == "Windows":
            return "C:\\Windows\\Fonts\\arial.ttf"
        elif platform.system() == "Darwin":
            return "/System/Library/Fonts/Supplemental/Arial.ttf"
        else:
            return "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    except:
        return None

def load_font(size=48):
    path = get_default_font_path()
    try:
        if path and os.path.exists(path):
            return ImageFont.truetype(path, size=size)
    except Exception:
        pass
    return ImageFont.load_default()

def letterbox_image_to_size(pil_img, target_size, bgcolor=(0,0,0)):
    """Resize image preserving aspect ratio and place centered onto background size target_size (w,h)."""
    w_target, h_target = target_size
    img = pil_img.convert("RGB")
    iw, ih = img.size
    # scale to fit
    scale = min(w_target/iw, h_target/ih)
    new_w = int(iw * scale)
    new_h = int(ih * scale)
    resized = img.resize((new_w, new_h), Image.LANCZOS)
    background = Image.new("RGB", (w_target, h_target), bgcolor)
    x = (w_target - new_w) // 2
    y = (h_target - new_h) // 2
    background.paste(resized, (x,y))
    return background

def add_text_overlay_to_pil(pil_img, text, fontsize, color_rgba, position):
    """Return new PIL image with centered text (top/center/bottom). color_rgba is (r,g,b,a)."""
    if not text:
        return pil_img.copy()
    img = pil_img.convert("RGBA").copy()
    draw = ImageDraw.Draw(img)
    font = load_font(size=fontsize)
    bbox = draw.textbbox((0,0), text, font=font)
    tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
    W, H = img.size
    x = (W - tw)//2
    if position == "top":
        y = 20
    elif position == "center":
        y = (H - th)//2
    else:
        y = H - th - 30
    # stroke for readability
    stroke_color = (0,0,0,200)
    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
        draw.text((x+dx,y+dy), text, font=font, fill=stroke_color)
    draw.text((x,y), text, font=font, fill=tuple(color_rgba))
    return img.convert("RGB")

def safe_mkstemp_in_dir(dirpath, suffix=""):
    """Create a unique temp file in given directory, return path (closed fd)."""
    fd, pth = tempfile.mkstemp(suffix=suffix, dir=dirpath)
    os.close(fd)
    return pth

# ---------------------------
# Video creation worker
# ---------------------------
def create_video_from_audio_and_images(
    audio_path, images_folder, output_path, preset_size, fps,
    target_display_time, loop_images, crossfade_seconds,
    text_overlay, progress_queue: Queue
):
    """
    Creates a video:
    - audio_path: path to audio file
    - images_folder: folder with images
    - output_path: final mp4 path
    - preset_size: (w,h)
    - fps: frames per second
    - target_display_time: target display time per image (used when loop_images True)
    - loop_images: boolean
    - crossfade_seconds: float or 0
    - text_overlay: dict {text, fontsize, color_rgba, position}
    - progress_queue: queue for UI updates
    """
    try:
        progress_queue.put(("status","Loading audio..."))
        audio = AudioFileClip(audio_path)
        duration = audio.duration
        progress_queue.put(("status", f"Audio loaded ({duration:.2f}s)"))

        # collect image files
        img_files = sorted([f for f in os.listdir(images_folder) if f.lower().endswith(('.jpg','.jpeg','.png','.webp'))])
        if not img_files:
            raise ValueError("No images found in selected folder.")

        full_paths = [os.path.join(images_folder, f) for f in img_files]

        # Decide per-image duration and full list of frames (with looping if requested)
        if loop_images:
            # compute number of slots to achieve target_display_time
            if target_display_time <= 0:
                raise ValueError("Target display time must be > 0")
            slots = max(1, math.ceil(duration / float(target_display_time)))
            per_image_duration = duration / slots
            # build list by cycling through images to fill `slots`
            from itertools import cycle, islice
            cyc = cycle(full_paths)
            selected = list(islice(cyc, slots))
        else:
            # no loop: distribute images evenly across the song
            n = len(full_paths)
            per_image_duration = duration / max(1, n)
            selected = full_paths.copy()

        progress_queue.put(("status", f"{len(selected)} image slots, each {per_image_duration:.2f}s"))

        clips = []
        total = len(selected)
        for idx, img_path in enumerate(selected, start=1):
            progress_queue.put(("status", f"Processing image {idx}/{total}"))
            # load and letterbox
            pil = Image.open(img_path)
            # apply text overlay (global)
            if text_overlay and text_overlay.get("text"):
                # first letterbox to create consistent image size before putting text (avoid very large fonts)
                lb = letterbox_image_to_size(pil, preset_size)
                lb = add_text_overlay_to_pil(lb, text_overlay["text"], text_overlay["fontsize"], text_overlay["color"], text_overlay["position"])
                frame = np.array(lb)
            else:
                lb = letterbox_image_to_size(pil, preset_size)
                frame = np.array(lb)

            # Convert frame to ImageClip
            clip = ImageClip(frame).set_duration(per_image_duration)
            clips.append(clip)

            progress_queue.put(("progress_fraction", idx/total*0.6))  # up to 60% for image processing

        # apply crossfade if needed
        if crossfade_seconds and crossfade_seconds > 0 and len(clips) > 1:
            # apply crossfadein to all except first clip
            cross = float(min(crossfade_seconds, per_image_duration/2.0))
            clips_faded = []
            for i, c in enumerate(clips):
                if i == 0:
                    clips_faded.append(c)
                else:
                    clips_faded.append(c.crossfadein(cross))
            final_vid = concatenate_videoclips(clips_faded, method="compose")
        else:
            final_vid = concatenate_videoclips(clips, method="compose")

        # set total duration exactly to audio duration (trim or pad)
        final_vid = final_vid.set_duration(duration)

        # attach audio (loop audio? no — audio length is source)
        final_vid = final_vid.set_audio(audio)

        progress_queue.put(("status","Rendering final video (this may take a while)..."))
        # safe temp file in output dir
        out_dir = os.path.dirname(os.path.abspath(output_path)) or os.getcwd()
        tmp_out = safe_mkstemp_in_dir(out_dir, suffix=".mp4")

        # write file
        # use write_videofile with codec libx264 and audio_codec aac
        final_vid.write_videofile(tmp_out, codec="libx264", audio_codec="aac", fps=fps, threads=4, preset="medium", verbose=False, logger=None)

        # move temp to final atomically
        os.replace(tmp_out, output_path)

        progress_queue.put(("done", output_path))
    except Exception as e:
        progress_queue.put(("error", str(e)))

# ---------------------------
# GUI
# ---------------------------
class App:
    def __init__(self, root):
        self.root = root
        root.title("Audio + Images → Video Maker")
        root.geometry("760x520")
        root.resizable(False, False)

        self.audio_path = tk.StringVar()
        self.images_folder = tk.StringVar()
        self.output_path = tk.StringVar(value="output.mp4")

        self.preset_var = tk.StringVar(value="YouTube 1920x1080")
        self.fps_var = tk.StringVar(value="24")
        self.target_display_var = tk.StringVar(value="3.0")
        self.loop_var = tk.IntVar(value=1)
        self.crossfade_var = tk.StringVar(value="0.5")
        self.text_var = tk.StringVar(value="")
        self.fontsize_var = tk.IntVar(value=48)
        self.text_position_var = tk.StringVar(value="bottom")
        self.text_color = (255,255,255,255)

        # progress queue from worker -> UI
        self.queue = Queue()

        self._build_ui()
        self._periodic_check()

    def _build_ui(self):
        pad = {"padx":8, "pady":6}
        # Audio
        tk.Label(self.root, text="Audio file:").pack(anchor="w", **pad)
        f1 = tk.Frame(self.root)
        f1.pack(fill="x", padx=10)
        tk.Entry(f1, textvariable=self.audio_path, width=60).pack(side="left")
        tk.Button(f1, text="Browse", command=self._browse_audio).pack(side="left", padx=6)

        # Images folder
        tk.Label(self.root, text="Images folder:").pack(anchor="w", **pad)
        f2 = tk.Frame(self.root)
        f2.pack(fill="x", padx=10)
        tk.Entry(f2, textvariable=self.images_folder, width=60).pack(side="left")
        tk.Button(f2, text="Browse", command=self._browse_images).pack(side="left", padx=6)

        # Output
        tk.Label(self.root, text="Output file (mp4):").pack(anchor="w", **pad)
        f3 = tk.Frame(self.root)
        f3.pack(fill="x", padx=10)
        tk.Entry(f3, textvariable=self.output_path, width=60).pack(side="left")
        tk.Button(f3, text="Choose", command=self._choose_output).pack(side="left", padx=6)

        # Settings
        tk.Label(self.root, text="Video settings:").pack(anchor="w", **pad)
        sett = tk.Frame(self.root)
        sett.pack(fill="x", padx=10)

        tk.Label(sett, text="Preset:").grid(row=0, column=0, sticky="w")
        presets = ["YouTube 1920x1080", "TikTok 1080x1920", "Instagram 1080x1080", "Custom..."]
        self.preset_box = Combobox(sett, values=presets, textvariable=self.preset_var, width=22, state="readonly")
        self.preset_box.grid(row=0, column=1, sticky="w", padx=6)
        self.preset_box.bind("<<ComboboxSelected>>", self._preset_changed)

        tk.Label(sett, text="FPS:").grid(row=0, column=2, sticky="w", padx=(12,0))
        tk.Entry(sett, textvariable=self.fps_var, width=6).grid(row=0, column=3, sticky="w")

        tk.Label(sett, text="Crossfade (s):").grid(row=1, column=0, sticky="w", pady=(8,0))
        tk.Entry(sett, textvariable=self.crossfade_var, width=6).grid(row=1, column=1, sticky="w", padx=6)

        tk.Checkbutton(sett, text="Loop images to meet target display time", variable=self.loop_var).grid(row=1, column=2, columnspan=2, sticky="w", padx=(12,0))

        tk.Label(sett, text="Target image display time (s):").grid(row=2, column=0, sticky="w", pady=(8,0))
        tk.Entry(sett, textvariable=self.target_display_var, width=6).grid(row=2, column=1, sticky="w", padx=6)
        tk.Label(sett, text="(used when Loop is checked)").grid(row=2, column=2, columnspan=2, sticky="w")

        # Text overlay
        tk.Label(self.root, text="Text overlay (optional):").pack(anchor="w", **pad)
        tframe = tk.Frame(self.root)
        tframe.pack(fill="x", padx=10)
        tk.Entry(tframe, textvariable=self.text_var, width=50).pack(side="left")
        tk.Button(tframe, text="Text Settings", command=self._text_settings).pack(side="left", padx=6)

        # Start
        act = tk.Frame(self.root)
        act.pack(fill="x", pady=12)
        tk.Button(act, text="Create Video", bg="#4CAF50", fg="white", width=16, command=self._start).pack(side="left", padx=8)
        tk.Button(act, text="Open output folder", command=self._open_output_folder).pack(side="left", padx=6)

        # Status & progress
        self.status = tk.Label(self.root, text="Ready", anchor="w")
        self.status.pack(fill="x", padx=10)
        self.progress = Progressbar(self.root, orient="horizontal", length=700, mode="determinate")
        self.progress.pack(padx=10, pady=(4,10))

    def _preset_changed(self, evt=None):
        v = self.preset_var.get()
        if v == "Custom...":
            res = self._ask_text("Enter resolution WIDTHxHEIGHT (e.g. 1280x720):", "1280x720")
            if res:
                self.preset_var.set(res.strip())

    def _ask_text(self, prompt, default=""):
        win = tk.Toplevel(self.root)
        win.title("Input")
        tk.Label(win, text=prompt).pack(padx=10, pady=(10,0))
        sv = tk.StringVar(value=default)
        tk.Entry(win, textvariable=sv, width=20).pack(padx=10, pady=8)
        result = {"val": None}
        def ok():
            result["val"] = sv.get().strip()
            win.destroy()
        tk.Button(win, text="OK", command=ok).pack(pady=8)
        win.transient(self.root)
        win.grab_set()
        self.root.wait_window(win)
        return result["val"]

    def _text_settings(self):
        top = tk.Toplevel(self.root)
        top.title("Text settings")
        tk.Label(top, text="Font size:").pack(anchor="w", padx=8, pady=(8,0))
        fs = tk.IntVar(value=self.fontsize_var.get())
        tk.Entry(top, textvariable=fs, width=6).pack(anchor="w", padx=8)

        tk.Label(top, text="Position:").pack(anchor="w", padx=8, pady=(8,0))
        pos = tk.StringVar(value=self.text_position_var.get())
        Combobox(top, textvariable=pos, values=["top","center","bottom"], width=12).pack(anchor="w", padx=8)

        tk.Label(top, text="Color:").pack(anchor="w", padx=8, pady=(8,0))
        cframe = tk.Frame(top); cframe.pack(anchor="w", padx=8)
        color_box = tk.Label(cframe, text="   ", bg=self._rgb_to_hex(self.text_color[:3]), relief="ridge")
        color_box.pack(side="left")
        def pick():
            res = colorchooser.askcolor()
            if res and res[1]:
                color_box.config(bg=res[1])
                self.text_color = (int(res[0][0]), int(res[0][1]), int(res[0][2]), 255)
        tk.Button(cframe, text="Pick", command=pick).pack(side="left", padx=6)

        def save_and_close():
            self.fontsize_var.set(fs.get())
            self.text_position_var.set(pos.get())
            top.destroy()

        tk.Button(top, text="Save", command=save_and_close).pack(pady=10)

    def _rgb_to_hex(self, rgb):
        return "#%02x%02x%02x" % tuple(rgb)

    def _browse_audio(self):
        p = filedialog.askopenfilename(filetypes=[("Audio files","*.mp3 *.m4a *.wav *.aac *.flac *.ogg"), ("All files","*.*")])
        if p:
            self.audio_path.set(os.path.abspath(p))

    def _browse_images(self):
        p = filedialog.askdirectory()
        if p:
            self.images_folder.set(os.path.abspath(p))

    def _choose_output(self):
        p = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 video","*.mp4")])
        if p:
            self.output_path.set(os.path.abspath(p))

    def _open_output_folder(self):
        path = self.output_path.get().strip()
        if not path:
            messagebox.showinfo("No output", "Output file not set.")
            return
        folder = os.path.dirname(path) or "."
        try:
            if platform.system() == "Windows":
                os.startfile(folder)
            elif platform.system() == "Darwin":
                os.system(f"open '{folder}' &")
            else:
                os.system(f"xdg-open '{folder}' &")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _start(self):
        audio = self.audio_path.get().strip()
        images = self.images_folder.get().strip()
        out = self.output_path.get().strip()

        if not audio or not os.path.exists(audio):
            messagebox.showerror("Error", "Please select a valid audio file.")
            return
        if not images or not os.path.isdir(images):
            messagebox.showerror("Error", "Please select a valid images folder.")
            return
        if not out:
            messagebox.showerror("Error", "Please choose an output filename.")
            return

        preset = self.preset_var.get()
        if "1920x1080" in preset:
            size = (1920,1080)
        elif "1080x1920" in preset:
            size = (1080,1920)
        elif "1080x1080" in preset:
            size = (1080,1080)
        elif "x" in preset:
            try:
                parts = preset.split("x")
                size = (int(parts[0]), int(parts[1]))
            except:
                size = (1920,1080)
        else:
            size = (1920,1080)

        try:
            fps = int(self.fps_var.get())
        except:
            fps = 24

        try:
            crossfade = float(self.crossfade_var.get())
        except:
            crossfade = 0.0

        try:
            target_display = float(self.target_display_var.get())
        except:
            target_display = 3.0

        loop_images = bool(self.loop_var.get())

        text_overlay = {
            "text": self.text_var.get().strip(),
            "fontsize": int(self.fontsize_var.get()),
            "color": self.text_color,
            "position": self.text_position_var.get()
        }

        # Start worker
        self.progress['value'] = 0
        self.status.config(text="Queued...")
        worker = threading.Thread(
            target=create_video_from_audio_and_images,
            args=(audio, images, out, size, fps, target_display, loop_images, crossfade, text_overlay, self.queue),
            daemon=True
        )
        worker.start()

    def _periodic_check(self):
        try:
            while True:
                msg = self.queue.get_nowait()
                typ, val = msg[0], msg[1]
                if typ == "status":
                    self.status.config(text=val)
                elif typ == "progress_fraction":
                    frac = float(val)
                    self.progress['value'] = min(95, frac*100)
                elif typ == "done":
                    self.progress['value'] = 100
                    self.status.config(text=f"Done: {val}")
                    messagebox.showinfo("Done", f"Video saved to:\n{val}")
                elif typ == "error":
                    self.status.config(text=f"Error: {val}")
                    messagebox.showerror("Error", val)
                else:
                    pass
        except Empty:
            pass
        self.root.after(250, self._periodic_check)

# ---------------------------
# Run
# ---------------------------
def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()

