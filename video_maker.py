"""
video_maker_gui.py
A Tkinter GUI for creating video from images or replacing audio in an existing video.
Dependencies (conda): moviepy, pillow, numpy
"""

import os
import threading
import platform
from functools import partial
from queue import Queue, Empty
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from tkinter import (
    Tk, Frame, Label, Entry, Button, StringVar, OptionMenu, filedialog,
    messagebox, IntVar, Checkbutton, Scale, HORIZONTAL, Toplevel
)
from tkinter.ttk import Progressbar, Combobox, Separator

from moviepy.editor import (
    ImageSequenceClip, VideoFileClip, AudioFileClip, CompositeVideoClip,
    ImageClip, concatenate_videoclips
)
from moviepy.audio.fx.all import audio_loop

# ---------------------------
# Utilities
# ---------------------------
def get_default_font_path():
    """Return a common system font path; fallback to None."""
    try:
        if platform.system() == "Windows":
            return "C:\\Windows\\Fonts\\arial.ttf"
        elif platform.system() == "Darwin":
            return "/System/Library/Fonts/Supplemental/Arial.ttf"
        else:
            return "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    except Exception:
        return None

def load_font(size=48):
    path = get_default_font_path()
    try:
        if path and os.path.exists(path):
            return ImageFont.truetype(path, size=size)
    except Exception:
        pass
    return ImageFont.load_default()

def make_text_image(text, size, fontsize=48, color=(255,255,255,255), bgcolor=(0,0,0,0), padding=20):
    """Create an RGBA PIL image with text centered. Returns numpy array with alpha."""
    w, h = size
    img = Image.new("RGBA", (w, h), bgcolor)
    draw = ImageDraw.Draw(img)
    font = load_font(size=fontsize)
    bbox = draw.textbbox((0,0), text, font=font)
    tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
    x = (w - tw) // 2
    y = (h - th) // 2
    draw.text((x, y), text, font=font, fill=color)
    return np.array(img)

def resize_keep_aspect(img, target_size):
    pil = Image.fromarray(img)
    pil = pil.convert("RGB")
    pil.thumbnail(target_size, Image.LANCZOS)
    # paste centered onto background of target_size
    bg = Image.new("RGB", target_size, (0,0,0))
    x = (target_size[0] - pil.width) // 2
    y = (target_size[1] - pil.height) // 2
    bg.paste(pil, (x,y))
    return np.array(bg)

# ---------------------------
# Video Processing Functions
# ---------------------------
def create_slideshow_from_images(
    folder, output_path, text_overlay, fps, image_duration,
    resolution, add_music_path=None, crossfade=False, loop_music=True,
    progress_queue: Queue = None
):
    """
    Create a video slideshow from images in 'folder'.
    - folder: path to images
    - output_path: path to produce (mp4)
    - text_overlay: dict with keys 'text','fontsize','color','position' (position is ignored here -- text centered)
    - fps: int
    - image_duration: seconds per image
    - resolution: (w,h)
    - add_music_path: optional path to audio to add
    - crossfade: boolean (applies crossfade between images)
    - loop_music: whether to loop music to match video duration
    - progress_queue: queue for status updates (UI)
    """
    files = sorted([p for p in os.listdir(folder) if p.lower().endswith(('.jpg','.jpeg','.png'))])
    if not files:
        raise ValueError("No images found in folder.")

    frames = []
    total_images = len(files)
    target_w, target_h = resolution
    step = 0

    # Create frame clips (each image shown for image_duration)
    clips = []
    for i, fname in enumerate(files, start=1):
        path = os.path.join(folder, fname)
        img = Image.open(path).convert("RGB")
        img_np = np.array(img)
        # resize while keeping aspect ratio, letterbox/pad
        img_np = resize_keep_aspect(img_np, (target_w, target_h))
        # add text overlay using PIL to avoid ImageMagick dependency
        if text_overlay and text_overlay.get("text"):
            # prepare text image and composite with alpha
            txt_img = Image.new("RGBA", (target_w, target_h), (0,0,0,0))
            draw = ImageDraw.Draw(txt_img)
            font = load_font(size=text_overlay.get("fontsize", 48))
            text = text_overlay["text"]
            bbox = draw.textbbox((0,0), text, font=font)
            tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
            # position options: top, center, bottom
            pos = text_overlay.get("position","bottom")
            x = (target_w - tw)//2
            if pos == "top":
                y = 20
            elif pos == "center":
                y = (target_h - th)//2
            else:
                y = target_h - th - 30
            draw.text((x,y), text, font=font, fill=tuple(text_overlay.get("color", (255,255,255,255))))
            # composite
            base = Image.fromarray(img_np).convert("RGBA")
            combined = Image.alpha_composite(base, txt_img).convert("RGB")
            img_np = np.array(combined)

        clip = ImageSequenceClip([img_np], fps=fps).set_duration(image_duration)
        clips.append(clip)

        step += 1
        if progress_queue:
            progress_queue.put(("progress_fraction", step/total_images*0.5))  # first-half

    # apply crossfade if requested
    if crossfade:
        # concatenate with crossfade of 1 second (or shorter if image_duration small)
        cf = min(1.0, image_duration/2.0)
        final_clip = concatenate_videoclips(clips, method="compose", padding=-cf)
    else:
        final_clip = concatenate_videoclips(clips, method="compose")

    duration = final_clip.duration

    # Handle music
    if add_music_path:
        audio = AudioFileClip(add_music_path)
        if loop_music:
            audio = audio_loop(audio, duration=duration)
        else:
            audio = audio.subclip(0, min(audio.duration, duration))
        final_clip = final_clip.set_audio(audio)
    else:
        final_clip = final_clip.set_audio(None)

    # write video
    if progress_queue:
        progress_queue.put(("status", "Rendering video..."))
    final_clip.write_videofile(output_path, codec="libx264", fps=fps, audio_codec="aac", threads=4, verbose=False, logger=None)
    if progress_queue:
        progress_queue.put(("done", output_path))

def replace_audio_in_video(
    video_path, output_path, new_audio_path=None, text_overlay=None,
    resolution=None, progress_queue: Queue = None
):
    """
    Load an existing video, optionally strip its audio and replace with new_audio_path.
    Optionally overlay text (text_overlay dict).
    """
    if progress_queue:
        progress_queue.put(("status", "Loading video..."))
    clip = VideoFileClip(video_path)
    w, h = clip.size
    # if resolution provided and differs, resize
    if resolution and tuple(resolution) != (w,h):
        clip = clip.resize(newsize=tuple(resolution))
        w, h = clip.size

    # remove original audio
    clip = clip.without_audio()

    # add text overlay if requested (uses ImageClip made from PIL rgba)
    if text_overlay and text_overlay.get("text"):
        txt_img_np = make_text_image(
            text_overlay["text"],
            size=(w,h),
            fontsize=text_overlay.get("fontsize", 48),
            color=text_overlay.get("color", (255,255,255,255))
        )
        txt_clip = ImageClip(txt_img_np, ismask=False).set_duration(clip.duration).set_pos(("center","bottom"))
        # composite
        clip = CompositeVideoClip([clip, txt_clip])

    # attach new audio if provided
    if new_audio_path:
        audio = AudioFileClip(new_audio_path)
        audio = audio_loop(audio, duration=clip.duration)
        clip = clip.set_audio(audio)

    if progress_queue:
        progress_queue.put(("status", "Rendering output video..."))
    clip.write_videofile(output_path, codec="libx264", audio_codec="aac", threads=4, verbose=False, logger=None)

    if progress_queue:
        progress_queue.put(("done", output_path))

# ---------------------------
# GUI
# ---------------------------
class VideoMakerApp:
    def __init__(self, root):
        self.root = root
        root.title("Modern Video Maker")
        root.geometry("720x640")
        root.resizable(False, False)

        # State variables
        self.mode_var = StringVar(value="Images -> Video")  # or "Replace Audio"
        self.input_folder = StringVar()
        self.input_video = StringVar()
        self.output_file = StringVar(value="output.mp4")
        self.music_file = StringVar()
        self.text_overlay = {
            "text": "",
            "fontsize": 48,
            "color": (255,255,255,255),
            "position": "bottom"
        }
        self.fps_var = StringVar(value="24")
        self.image_duration_var = StringVar(value="2.0")
        self.crossfade_var = IntVar(value=1)
        self.preset_var = StringVar(value="YouTube 16:9 (1920x1080)")

        # Queue for worker -> UI messages
        self.progress_queue = Queue()

        self._build_ui()
        self._periodic_check()

    def _build_ui(self):
        pad = {"padx":10, "pady":6}

        # Mode selection
        Label(self.root, text="Mode:", font=("Segoe UI", 10, "bold")).pack(anchor="w", **pad)
        mode_frame = Frame(self.root)
        mode_frame.pack(fill="x", **pad)
        Button(mode_frame, text="Images -> Video", command=lambda: self._set_mode("Images -> Video")).pack(side="left", padx=6)
        Button(mode_frame, text="Replace Audio in Video", command=lambda: self._set_mode("Replace Audio")).pack(side="left", padx=6)

        Separator(self.root, orient="horizontal").pack(fill="x", pady=8)

        # Input for images
        self.images_frame = Frame(self.root)
        self.images_frame.pack(fill="x", **pad)
        Label(self.images_frame, text="Images Folder:").grid(row=0, column=0, sticky="w")
        Entry(self.images_frame, textvariable=self.input_folder, width=50).grid(row=0, column=1, columnspan=2, sticky="w")
        Button(self.images_frame, text="Browse", command=self._browse_folder).grid(row=0, column=3, padx=6)

        # Input for video (only shown in Replace Audio mode)
        self.video_frame = Frame(self.root)
        Label(self.video_frame, text="Input Video:").grid(row=0, column=0, sticky="w")
        Entry(self.video_frame, textvariable=self.input_video, width=50).grid(row=0, column=1, columnspan=2, sticky="w")
        Button(self.video_frame, text="Browse", command=self._browse_video).grid(row=0, column=3, padx=6)

        # Music selection
        Label(self.root, text="Music (optional):").pack(anchor="w", **pad)
        music_frame = Frame(self.root)
        music_frame.pack(fill="x", **pad)
        Entry(music_frame, textvariable=self.music_file, width=50).pack(side="left")
        Button(music_frame, text="Browse", command=self._browse_music).pack(side="left", padx=6)
        Button(music_frame, text="Preview Music", command=self._preview_music).pack(side="left", padx=6)

        # Text overlay controls
        Label(self.root, text="Text overlay (applies to entire video):").pack(anchor="w", **pad)
        txt_frame = Frame(self.root)
        txt_frame.pack(fill="x", **pad)
        self.text_var = StringVar()
        Entry(txt_frame, textvariable=self.text_var, width=40).pack(side="left")
        Button(txt_frame, text="Settings", command=self._text_settings).pack(side="left", padx=6)

        # Video settings
        Label(self.root, text="Video settings:").pack(anchor="w", **pad)
        sett_frame = Frame(self.root)
        sett_frame.pack(fill="x", **pad)
        Label(sett_frame, text="FPS:").grid(row=0, column=0, sticky="w")
        fps_combo = Combobox(sett_frame, textvariable=self.fps_var, values=["12","24","30","60"], width=5)
        fps_combo.grid(row=0, column=1, sticky="w")
        Label(sett_frame, text="Image duration (s):").grid(row=0, column=2, sticky="w", padx=(10,0))
        Entry(sett_frame, textvariable=self.image_duration_var, width=6).grid(row=0, column=3, sticky="w")

        Checkbutton(sett_frame, text="Crossfade between images", variable=self.crossfade_var).grid(row=1, column=0, columnspan=2, sticky="w", pady=6)

        # Presets
        Label(self.root, text="Platform preset (resolution):").pack(anchor="w", **pad)
        presets = [
            "YouTube 16:9 (1920x1080)",
            "TikTok 9:16 (1080x1920)",
            "Instagram Square (1080x1080)",
            "Facebook 1280x720",
            "Custom..."
        ]
        OptionMenu(self.root, self.preset_var, *presets, command=self._preset_changed).pack(fill="x", padx=10)

        # Output file
        out_frame = Frame(self.root)
        out_frame.pack(fill="x", **pad)
        Label(out_frame, text="Output file:").grid(row=0, column=0, sticky="w")
        Entry(out_frame, textvariable=self.output_file, width=50).grid(row=0, column=1, sticky="w")
        Button(out_frame, text="Choose", command=self._choose_output).grid(row=0, column=2, padx=6)

        # Actions
        action_frame = Frame(self.root)
        action_frame.pack(fill="x", pady=12)
        Button(action_frame, text="Start", command=self._start).pack(side="left", padx=8)
        Button(action_frame, text="Open output folder", command=self._open_output_folder).pack(side="left", padx=8)
        Button(action_frame, text="Quit", command=self.root.quit).pack(side="right", padx=8)

        # Progress bar & status
        self.status_label = Label(self.root, text="Ready", anchor="w")
        self.status_label.pack(fill="x", padx=10)
        self.progress = Progressbar(self.root, orient=HORIZONTAL, length=600, mode="determinate")
        self.progress.pack(padx=10, pady=(0,10))

        # Start with Images -> Video mode visible
        self._set_mode("Images -> Video")

    def _set_mode(self, mode):
        self.mode_var.set(mode)
        if mode == "Images -> Video":
            self.video_frame.pack_forget()
            self.images_frame.pack(fill="x", padx=10, pady=6)
        else:
            self.images_frame.pack_forget()
            self.video_frame.pack(fill="x", padx=10, pady=6)

    def _browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.input_folder.set(folder)

    def _browse_video(self):
        path = filedialog.askopenfilename(filetypes=[("Video files","*.mp4 *.mov *.avi *.mkv"), ("All files","*.*")])
        if path:
            self.input_video.set(path)

    def _browse_music(self):
        path = filedialog.askopenfilename(filetypes=[("Audio files","*.mp3 *.wav *.m4a *.aac"), ("All files","*.*")])
        if path:
            self.music_file.set(path)

    def _choose_output(self):
        path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 video","*.mp4")])
        if path:
            self.output_file.set(path)

    def _preview_music(self):
        mp = self.music_file.get().strip()
        if not mp or not os.path.exists(mp):
            messagebox.showwarning("No music", "Please select a valid music file first.")
            return
        # Quick preview: spawn system default player (non-blocking)
        try:
            if platform.system() == "Windows":
                os.startfile(mp)
            elif platform.system() == "Darwin":
                # macOS
                os.system(f"open '{mp}' &")
            else:
                os.system(f"xdg-open '{mp}' &")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file: {e}")

    def _text_settings(self):
        # small toplevel to configure font size, color, position
        top = Toplevel(self.root)
        top.title("Text settings")
        top.geometry("360x220")
        Label(top, text="Text to overlay:").pack(anchor="w", padx=10, pady=(10,2))
        txt_entry = Entry(top, width=40, textvariable=self.text_var)
        txt_entry.pack(padx=10, pady=(0,10))

        Label(top, text="Font size:").pack(anchor="w", padx=10)
        fs_var = StringVar(value=str(self.text_overlay.get("fontsize",48)))
        Entry(top, textvariable=fs_var, width=6).pack(anchor="w", padx=10)

        Label(top, text="Position:").pack(anchor="w", padx=10, pady=(8,0))
        pos_var = StringVar(value=self.text_overlay.get("position","bottom"))
        OptionMenu(top, pos_var, "top","center","bottom").pack(anchor="w", padx=10)

        Label(top, text="Color (R,G,B[,A]):").pack(anchor="w", padx=10, pady=(8,0))
        color_var = StringVar(value="255,255,255,255")
        Entry(top, textvariable=color_var, width=20).pack(anchor="w", padx=10)

        def save_and_close():
            self.text_overlay["text"] = self.text_var.get().strip()
            try:
                self.text_overlay["fontsize"] = int(fs_var.get())
            except:
                self.text_overlay["fontsize"] = 48
            self.text_overlay["position"] = pos_var.get()
            try:
                parts = [int(x.strip()) for x in color_var.get().split(",")]
                if len(parts) == 3: parts.append(255)
                self.text_overlay["color"] = tuple(parts)
            except:
                self.text_overlay["color"] = (255,255,255,255)
            top.destroy()

        Button(top, text="Save", command=save_and_close).pack(pady=12)

    def _preset_changed(self, val):
        if val == "Custom...":
            # ask user to enter custom resolution
            resp = filedialog.asksaveasfilename(title="Enter custom resolution example filename (we'll parse size from name)", defaultextension=".mp4")
            # not ideal — simpler: show dialog to type resolution
            res = self._ask_text("Enter resolution as WIDTHxHEIGHT (e.g. 1280x720):", "1280x720")
            if res:
                self.preset_var.set(res.strip())
        else:
            self.preset_var.set(val)

    def _ask_text(self, prompt, default=""):
        win = Toplevel(self.root)
        win.title("Input")
        Label(win, text=prompt).pack(padx=10, pady=(10,0))
        sv = StringVar(value=default)
        Entry(win, textvariable=sv).pack(padx=10, pady=8)
        result = {"value": None}
        def ok():
            result["value"] = sv.get().strip()
            win.destroy()
        Button(win, text="OK", command=ok).pack(pady=8)
        win.transient(self.root)
        win.grab_set()
        self.root.wait_window(win)
        return result["value"]

    def _open_output_folder(self):
        path = self.output_file.get()
        if not path:
            messagebox.showinfo("No output", "Output file not set.")
            return
        folder = os.path.dirname(os.path.abspath(path)) or "."
        try:
            if platform.system() == "Windows":
                os.startfile(folder)
            elif platform.system() == "Darwin":
                os.system(f"open '{folder}' &")
            else:
                os.system(f"xdg-open '{folder}' &")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open folder: {e}")

    def _get_resolution(self):
        preset = self.preset_var.get()
        if "1920x1080" in preset:
            return (1920,1080)
        if "1080x1920" in preset:
            return (1080,1920)
        if "1080x1080" in preset:
            return (1080,1080)
        if "1280x720" in preset:
            return (1280,720)
        # fallback parsing like "WIDTHxHEIGHT"
        if "x" in preset:
            try:
                parts = preset.split("(")[0].strip()
                w,h = parts.split("x")[:2]
                return (int(w), int(h))
            except:
                pass
        # default
        return (1920,1080)

    def _start(self):
        mode = self.mode_var.get()
        outp = self.output_file.get().strip()
        if not outp:
            messagebox.showerror("Missing output", "Please set an output filename.")
            return

        if mode == "Images -> Video":
            folder = self.input_folder.get().strip()
            if not folder or not os.path.isdir(folder):
                messagebox.showerror("Missing folder", "Please select a valid images folder.")
                return
            music = self.music_file.get().strip() or None
            try:
                fps = int(self.fps_var.get())
                image_duration = float(self.image_duration_var.get())
            except:
                messagebox.showerror("Invalid settings", "FPS and image duration must be numbers.")
                return
            crossfade = bool(self.crossfade_var.get())
            resolution = self._get_resolution()
            text = self.text_overlay.copy()
            text["text"] = self.text_var.get().strip()

            # run worker thread
            self.progress["value"] = 0
            self.status_label.config(text="Queued...")
            worker = threading.Thread(
                target=self._worker_create_images_video,
                args=(folder, outp, text, fps, image_duration, resolution, music, crossfade),
                daemon=True
            )
            worker.start()

        else:
            video = self.input_video.get().strip()
            if not video or not os.path.exists(video):
                messagebox.showerror("Missing video", "Please select a valid input video.")
                return
            music = self.music_file.get().strip() or None
            resolution = self._get_resolution()
            text = self.text_overlay.copy()
            text["text"] = self.text_var.get().strip()

            self.progress["value"] = 0
            self.status_label.config(text="Queued...")
            worker = threading.Thread(
                target=self._worker_replace_audio,
                args=(video, outp, music, text, resolution),
                daemon=True
            )
            worker.start()

    # Worker wrappers that report to progress_queue
    def _worker_create_images_video(self, folder, outp, text, fps, image_duration, resolution, music, crossfade):
        try:
            create_slideshow_from_images(
                folder=folder,
                output_path=outp,
                text_overlay=text,
                fps=fps,
                image_duration=image_duration,
                resolution=resolution,
                add_music_path=music,
                crossfade=crossfade,
                loop_music=True,
                progress_queue=self.progress_queue
            )
        except Exception as e:
            self.progress_queue.put(("error", str(e)))

    def _worker_replace_audio(self, video, outp, music, text, resolution):
        try:
            replace_audio_in_video(
                video_path=video,
                output_path=outp,
                new_audio_path=music,
                text_overlay=text,
                resolution=resolution,
                progress_queue=self.progress_queue
            )
        except Exception as e:
            self.progress_queue.put(("error", str(e)))

    # Poll the queue and update UI
    def _periodic_check(self):
        try:
            while True:
                item = self.progress_queue.get_nowait()
                if item[0] == "status":
                    self.status_label.config(text=item[1])
                elif item[0] == "progress_fraction":
                    frac = item[1]
                    # map 0..1 to progressbar 0..90 (final writing will fill to 100)
                    self.progress["value"] = min(90, frac*100)
                elif item[0] == "done":
                    out = item[1]
                    self.progress["value"] = 100
                    self.status_label.config(text=f"Done: {out}")
                    messagebox.showinfo("Completed", f"Video saved to:\n{out}")
                elif item[0] == "error":
                    self.status_label.config(text=f"Error: {item[1]}")
                    messagebox.showerror("Error", item[1])
                else:
                    # unknown message
                    pass
        except Empty:
            pass
        # schedule next check
        self.root.after(250, self._periodic_check)

# ---------------------------
# Main
# ---------------------------
def main():
    root = Tk()
    style_font = ("Segoe UI", 10)
    root.option_add("*Font", style_font)
    app = VideoMakerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

