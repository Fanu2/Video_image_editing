#!/usr/bin/env python3
"""
M4A Cover Editor with Automatic FFmpeg Fix (Final Version)
----------------------------------------------------------

Features:
✔ View current cover
✔ Replace cover with new image
✔ Add text overlay (top, center, bottom)
✔ Overwrite or Save As new file
✔ Auto-detect invalid M4A and repair using FFmpeg
✔ Unique temp files using mkstemp() (no conflicts)
✔ Fully supports filenames with spaces
✔ Conda-friendly (Mutagen + Pillow + FFmpeg)

Install:
    conda install -c conda-forge python-mutagen pillow ffmpeg
"""

import os
import io
import subprocess
import tempfile
import platform
import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
from tkinter.ttk import Button, Entry, Combobox

from PIL import Image, ImageDraw, ImageFont, ImageTk
from mutagen.mp4 import MP4, MP4Cover


# ===============================================================
# Font Helpers
# ===============================================================

def get_default_font_path():
    if platform.system() == "Windows":
        return "C:\\Windows\\Fonts\\arial.ttf"
    elif platform.system() == "Darwin":
        return "/System/Library/Fonts/Supplemental/Arial.ttf"
    return "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def load_font(size=40):
    path = get_default_font_path()
    try:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    except:
        pass
    return ImageFont.load_default()


# ===============================================================
# Image Helpers
# ===============================================================

def pil_to_tk(img, maxsize=(360,360)):
    w, h = img.size
    mw, mh = maxsize
    scale = min(mw / w, mh / h, 1.0)
    if scale < 1:
        img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
    return ImageTk.PhotoImage(img)


def add_text_overlay(img, text, size, color, pos):
    if not text:
        return img.copy()

    img = img.convert("RGBA").copy()
    draw = ImageDraw.Draw(img)
    font = load_font(size)

    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    W, H = img.size
    x = (W - tw) // 2

    if pos == "top":
        y = 20
    elif pos == "center":
        y = (H - th) // 2
    else:
        y = H - th - 20

    # Outline
    for dx, dy in [(-2,0),(2,0),(0,-2),(0,2)]:
        draw.text((x+dx, y+dy), text, font=font, fill=(0,0,0,200))

    draw.text((x, y), text, font=font, fill=color)
    return img


def pil_to_bytes(img):
    fmt = "JPEG"
    if img.mode in ("RGBA","LA"):
        fmt = "PNG"

    bio = io.BytesIO()
    if fmt == "JPEG":
        if img.mode == "RGBA":
            img = img.convert("RGB")
        img.save(bio, format="JPEG", quality=95)
    else:
        img.save(bio, format="PNG")

    return bio.getvalue(), fmt


# ===============================================================
# FFprobe / FFmpeg Utilities
# ===============================================================

def is_mp4_container(path):
    try:
        cmd = [
            "ffprobe", "-v", "error",
            "-show_entries", "format=format_name",
            "-of", "default=noprint_wrappers=1:nokey=1",
            path
        ]
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True).strip()
        return ("mp4" in out) or ("m4a" in out) or ("mov" in out)
    except:
        return False


def ffmpeg_fix_to_m4a(src, dest, reencode=False):
    try:
        if not reencode:
            cmd = [
                "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                "-i", src, "-c", "copy", "-map", "0",
                "-movflags", "+faststart",
                dest
            ]
        else:
            cmd = [
                "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                "-i", src,
                "-c:a", "aac", "-b:a", "192k",
                "-vn", "-movflags", "+faststart",
                dest
            ]

        subprocess.check_call(cmd)
        return True
    except:
        return False


# ===============================================================
# Mutagen Embedding with Auto-Fix
# ===============================================================

def load_cover(path):
    audio = MP4(path)
    covr = audio.tags.get("covr")
    if not covr:
        return None
    try:
        return Image.open(io.BytesIO(bytes(covr[0]))).convert("RGBA")
    except:
        return None


def embed_cover_safe(input_file, output_file, pil_img):
    """Embed cover using Mutagen safely."""
    audio = MP4(input_file)
    img_bytes, fmt = pil_to_bytes(pil_img)

    cov = MP4Cover(img_bytes,
                   imageformat=MP4Cover.FORMAT_PNG if fmt == "PNG" else MP4Cover.FORMAT_JPEG)

    audio.tags["covr"] = [cov]
    audio.save(output_file)


def embed_cover_with_autofix(input_file, output_file, pil_img):
    """Automatically repair invalid M4A before embedding cover."""
    folder = os.path.dirname(os.path.abspath(output_file)) or os.getcwd()

    # 1) If invalid container, remux or reencode
    if not is_mp4_container(input_file):
        # Unique remux tmp
        remux_fd, remux_path = tempfile.mkstemp(dir=folder, suffix=".m4a")
        os.close(remux_fd)

        if ffmpeg_fix_to_m4a(input_file, remux_path, reencode=False):
            working_input = remux_path
        else:
            # Unique reencode tmp
            re_fd, reenc_path = tempfile.mkstemp(dir=folder, suffix=".m4a")
            os.close(re_fd)
            if not ffmpeg_fix_to_m4a(input_file, reenc_path, reencode=True):
                raise RuntimeError("FFmpeg failed to create a valid M4A for tagging.")
            working_input = reenc_path
    else:
        working_input = input_file

    # 2) Unique target for embedding
    out_fd, embed_temp = tempfile.mkstemp(dir=folder, suffix=".m4a")
    os.close(out_fd)

    try:
        # First try direct embed
        try:
            embed_cover_safe(working_input, embed_temp, pil_img)
            os.replace(embed_temp, output_file)
        except:
            # Fallback: reencode then embed
            re_fd, reenc2 = tempfile.mkstemp(dir=folder, suffix=".m4a")
            os.close(re_fd)

            if not ffmpeg_fix_to_m4a(working_input, reenc2, reencode=True):
                raise RuntimeError("FFmpeg could not repair file before embedding.")

            embed_cover_safe(reenc2, embed_temp, pil_img)
            os.replace(embed_temp, output_file)

            # Cleanup
            if os.path.exists(reenc2):
                try: os.remove(reenc2)
                except: pass

    finally:
        # Cleanup possible temp
        if os.path.exists(embed_temp):
            try: os.remove(embed_temp)
            except: pass

        if working_input != input_file:
            try: os.remove(working_input)
            except: pass


# ===============================================================
# GUI CLASS
# ===============================================================

class M4AEditorGUI:
    def __init__(self, root):
        self.root = root
        root.title("M4A Cover Editor (Auto-Fix Enabled)")
        root.geometry("900x600")
        root.resizable(False, False)

        self.m4a = None
        self.cover_img = None
        self.new_img_path = None
        self.modified_img = None
        self.text_color = (255,255,255,255)

        self.build_ui()

    def build_ui(self):
        left = tk.Frame(self.root)
        left.pack(side="left", padx=12, pady=12)

        right = tk.Frame(self.root)
        right.pack(side="right", padx=12, pady=12)

        # === LOAD M4A ===
        tk.Label(left, text="1) Select M4A File", font=("Segoe UI", 12, "bold")).pack(anchor="w")
        f = tk.Frame(left)
        f.pack(fill="x")
        self.entry_m4a = tk.Entry(f, width=50)
        self.entry_m4a.pack(side="left")
        Button(f, text="Browse", command=self.load_m4a).pack(side="left", padx=6)

        tk.Label(left, text="Current Cover:").pack(anchor="w", pady=(10,0))
        self.lbl_current = tk.Label(left, text="(no cover)", width=48, height=16, relief="sunken")
        self.lbl_current.pack()

        Button(left, text="Extract Cover", command=self.extract_cover).pack(pady=4)

        # === LOAD IMAGE ===
        tk.Label(left, text="2) Select New Image", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(12,0))
        fi = tk.Frame(left)
        fi.pack(fill="x")
        self.entry_img = tk.Entry(fi, width=50)
        self.entry_img.pack(side="left")
        Button(fi, text="Browse", command=self.load_image).pack(side="left", padx=6)

        tk.Label(left, text="Preview:").pack(anchor="w", pady=(10,0))
        self.lbl_preview = tk.Label(left, text="(no preview)", width=48, height=12, relief="sunken")
        self.lbl_preview.pack()

        # === TEXT OVERLAY ===
        tk.Label(right, text="3) Text Overlay", font=("Segoe UI", 12, "bold")).pack(anchor="w")

        tk.Label(right, text="Text:").pack(anchor="w")
        self.entry_text = tk.Entry(right, width=40)
        self.entry_text.pack(anchor="w")

        tk.Label(right, text="Font Size:").pack(anchor="w")
        self.size_var = tk.IntVar(value=40)
        tk.Entry(right, textvariable=self.size_var, width=6).pack(anchor="w")

        tk.Label(right, text="Color:").pack(anchor="w")
        cf = tk.Frame(right)
        cf.pack(anchor="w")
        self.colbox = tk.Label(cf, text="   ", bg="#ffffff", relief="ridge")
        self.colbox.pack(side="left")
        Button(cf, text="Pick", command=self.pick_color).pack(side="left", padx=5)

        tk.Label(right, text="Position:").pack(anchor="w")
        self.pos_var = tk.StringVar(value="bottom")
        Combobox(right, textvariable=self.pos_var,
                 values=["top","center","bottom"], width=10).pack(anchor="w")

        Button(right, text="Apply Text & Preview", command=self.apply_text).pack(fill="x", pady=10)

        # === SAVE ===
        tk.Label(right, text="4) Save", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(16,4))
        Button(right, text="Overwrite Original", command=self.save_overwrite).pack(fill="x", pady=4)
        Button(right, text="Save As...", command=self.save_as).pack(fill="x", pady=4)

        self.status = tk.Label(right, text="Status: Ready", anchor="w")
        self.status.pack(fill="x", pady=10)

    # ===============================================================
    # ACTIONS
    # ===============================================================

    def load_m4a(self):
        path = filedialog.askopenfilename(
            filetypes=[("M4A Files","*.m4a *.mp4 *.m4b"),("All files","*.*")]
        )
        if not path: return

        self.m4a = os.path.abspath(path)
        self.entry_m4a.delete(0, tk.END)
        self.entry_m4a.insert(0, self.m4a)

        img = load_cover(self.m4a)
        self.cover_img = img

        if img:
            tkimg = pil_to_tk(img)
            self.lbl_current.config(text="", image=tkimg)
            self.lbl_current.image = tkimg
        else:
            self.lbl_current.config(text="(no cover)", image="")

        self.status.config(text="Loaded M4A")

    def extract_cover(self):
        if not self.cover_img:
            messagebox.showinfo("No cover", "This file has no cover.")
            return

        out = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG","*.png"),("JPEG","*.jpg *.jpeg"),("All","*.*")]
        )
        if not out: return

        self.cover_img.save(out)
        self.status.config(text="Cover extracted")

    def load_image(self):
        path = filedialog.askopenfilename(
            filetypes=[
                ("Images","*.jpg *.jpeg *.png *.webp"),
                ("All files","*.*")]
        )
        if not path: return

        self.new_img_path = os.path.abspath(path)
        self.entry_img.delete(0, tk.END)
        self.entry_img.insert(0, self.new_img_path)

        img = Image.open(self.new_img_path).convert("RGBA")
        self.modified_img = img.copy()

        tkimg = pil_to_tk(img)
        self.lbl_preview.config(text="", image=tkimg)
        self.lbl_preview.image = tkimg

        self.status.config(text="Image loaded")

    def pick_color(self):
        c = colorchooser.askcolor()
        if c and c[1]:
            r,g,b = c[0]
            self.text_color = (int(r),int(g),int(b),255)
            self.colbox.config(bg=c[1])

    def apply_text(self):
        if self.new_img_path:
            base = Image.open(self.new_img_path).convert("RGBA")
        elif self.cover_img:
            base = self.cover_img.copy()
        else:
            messagebox.showerror("Error","No image loaded.")
            return

        txt = self.entry_text.get().strip()
        size = self.size_var.get()
        pos = self.pos_var.get()

        new = add_text_overlay(base, txt, size, self.text_color, pos)
        self.modified_img = new

        tkimg = pil_to_tk(new)
        self.lbl_preview.config(image=tkimg, text="")
        self.lbl_preview.image = tkimg

        self.status.config(text="Overlay applied")

    def save_overwrite(self):
        if not self.m4a:
            messagebox.showerror("Error","No M4A loaded.")
            return
        if not self.modified_img:
            messagebox.showerror("Error","No modified cover.")
            return
        try:
            embed_cover_with_autofix(self.m4a, self.m4a, self.modified_img)
            self.status.config(text="Saved (overwrite)")
            messagebox.showinfo("Done","Cover successfully updated.")
            self.load_m4a()
        except Exception as e:
            messagebox.showerror("Save Failed", str(e))

    def save_as(self):
        if not self.m4a or not self.modified_img:
            messagebox.showerror("Error","Missing M4A or cover.")
            return

        out = filedialog.asksaveasfilename(
            defaultextension=".m4a",
            filetypes=[("M4A","*.m4a"),("All","*.*")]
        )
        if not out:
            return

        try:
            embed_cover_with_autofix(self.m4a, out, self.modified_img)
            self.status.config(text="Saved new file")
            messagebox.showinfo("Done","Saved as:\n" + out)
        except Exception as e:
            messagebox.showerror("Save Failed", str(e))


# ===============================================================
# MAIN
# ===============================================================

def main():
    root = tk.Tk()
    M4AEditorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
