import os
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

import cv2
from PIL import Image


class FiftyShadesGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Fifty Shades Image → Video Maker")
        self.geometry("700x500")

        # ---------- Default settings ----------
        self.default_url = "https://fifty-shades-react.vercel.app/"
        self.output_dir = os.path.abspath("downloaded_images")
        self.output_video = "fifty_shades_video.mp4"
        self.seconds_per_image = 2
        self.fps = 30

        # ---------- UI ----------
        self.create_widgets()

    def create_widgets(self):
        padding = {"padx": 10, "pady": 5}

        # URL
        url_frame = ttk.Frame(self)
        url_frame.pack(fill="x", **padding)

        ttk.Label(url_frame, text="Page URL:").pack(side="left")
        self.url_entry = ttk.Entry(url_frame)
        self.url_entry.pack(side="left", fill="x", expand=True, padx=(5, 0))
        self.url_entry.insert(0, self.default_url)

        # Output directory
        outdir_frame = ttk.Frame(self)
        outdir_frame.pack(fill="x", **padding)

        ttk.Label(outdir_frame, text="Output folder:").pack(side="left")
        self.outdir_entry = ttk.Entry(outdir_frame)
        self.outdir_entry.pack(side="left", fill="x", expand=True, padx=(5, 0))
        self.outdir_entry.insert(0, self.output_dir)

        browse_btn = ttk.Button(outdir_frame, text="Browse…", command=self.browse_output_dir)
        browse_btn.pack(side="left", padx=(5, 0))

        # Output video name
        video_frame = ttk.Frame(self)
        video_frame.pack(fill="x", **padding)

        ttk.Label(video_frame, text="Output video file:").pack(side="left")
        self.video_entry = ttk.Entry(video_frame)
        self.video_entry.pack(side="left", fill="x", expand=True, padx=(5, 0))
        self.video_entry.insert(0, self.output_video)

        # Seconds per image & FPS
        settings_frame = ttk.Frame(self)
        settings_frame.pack(fill="x", **padding)

        ttk.Label(settings_frame, text="Seconds per image:").pack(side="left")
        self.seconds_spin = ttk.Spinbox(settings_frame, from_=1, to=20, width=5)
        self.seconds_spin.pack(side="left", padx=(5, 20))
        self.seconds_spin.delete(0, "end")
        self.seconds_spin.insert(0, str(self.seconds_per_image))

        ttk.Label(settings_frame, text="FPS:").pack(side="left")
        self.fps_spin = ttk.Spinbox(settings_frame, from_=1, to=60, width=5)
        self.fps_spin.pack(side="left", padx=(5, 0))
        self.fps_spin.delete(0, "end")
        self.fps_spin.insert(0, str(self.fps))

        # Start button
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", **padding)

        self.start_btn = ttk.Button(btn_frame, text="Create Video", command=self.start_process_thread)
        self.start_btn.pack(side="left")

        # Progress bar
        self.progress = ttk.Progressbar(btn_frame, mode="indeterminate")
        self.progress.pack(side="left", fill="x", expand=True, padx=(10, 0))

        # Log window
        log_frame = ttk.LabelFrame(self, text="Log")
        log_frame.pack(fill="both", expand=True, **padding)

        self.log_text = tk.Text(log_frame, wrap="word", height=15)
        self.log_text.pack(fill="both", expand=True)
        self.log_text.config(state="disabled")

    # ---------- UI Helpers ----------
    def browse_output_dir(self):
        selected = filedialog.askdirectory(initialdir=self.output_dir)
        if selected:
            self.outdir_entry.delete(0, "end")
            self.outdir_entry.insert(0, selected)

    def log(self, message: str):
        self.log_text.config(state="normal")
        try:
            self.log_text.insert("end", message + "\n")
        except:
            # remove emojis if tk can't render them
            cleaned = message.encode("ascii", "ignore").decode()
            self.log_text.insert("end", cleaned + "\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")
        self.update_idletasks()

    def set_ui_busy(self, busy: bool):
        if busy:
            self.start_btn.config(state="disabled")
            self.progress.start(80)
        else:
            self.start_btn.config(state="normal")
            self.progress.stop()

    # ---------- Threading ----------
    def start_process_thread(self):
        t = threading.Thread(target=self.run_process_safe, daemon=True)
        t.start()

    def run_process_safe(self):
        try:
            self.set_ui_busy(True)
            self.run_process()
        except Exception as e:
            self.log(f"Error: {e}")
            messagebox.showerror("Error", str(e))
        finally:
            self.set_ui_busy(False)

    # ---------- Main Logic ----------
    def run_process(self):
        url = self.url_entry.get().strip()
        outdir = self.outdir_entry.get().strip()
        video_name = self.video_entry.get().strip()

        if not url:
            raise ValueError("URL cannot be empty.")

        if not video_name.lower().endswith(".mp4"):
            video_name += ".mp4"

        os.makedirs(outdir, exist_ok=True)

        try:
            seconds_per_image = int(self.seconds_spin.get())
            fps = int(self.fps_spin.get())
        except ValueError:
            raise ValueError("Seconds per image and FPS must be integers.")

        if seconds_per_image <= 0 or fps <= 0:
            raise ValueError("Seconds per image and FPS must be positive.")

        # --- Fetch webpage ---
        self.log("Fetching webpage...")
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        image_tags = soup.find_all("img")
        image_urls = [urljoin(url, img.get("src")) for img in image_tags if img.get("src")]

        self.log(f"Found {len(image_urls)} images.")

        if not image_urls:
            raise RuntimeError("No images found on page.")

        # --- Download images ---
        downloaded = []
        for i, img_url in enumerate(image_urls):
            try:
                self.log(f"Downloading {img_url}")
                r = requests.get(img_url, stream=True, timeout=10)
                r.raise_for_status()

                filename = os.path.join(outdir, f"img_{i:03d}.jpg")
                with open(filename, "wb") as f:
                    for chunk in r.iter_content(4096):
                        f.write(chunk)

                downloaded.append(filename)

            except Exception as e:
                self.log(f"Failed to download {img_url}: {e}")

        if not downloaded:
            raise RuntimeError("No images downloaded. Cannot create video.")

        # --- Create video ---
        self.log("Creating video...")

        first_img = Image.open(downloaded[0])
        width, height = first_img.size

        # Best for cross-platform mp4 creation (needs ffmpeg installed)
        fourcc = cv2.VideoWriter_fourcc(*"avc1")

        output_path = os.path.join(outdir, video_name)
        video = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        frames_per_img = fps * seconds_per_image

        for img_path in downloaded:
            self.log(f"Adding to video: {os.path.basename(img_path)}")
            frame = cv2.imread(img_path)

            if frame is None:
                self.log(f"Skipping unreadable image: {img_path}")
                continue

            frame = cv2.resize(frame, (width, height))

            for _ in range(frames_per_img):
                video.write(frame)

        video.release()

        self.log(f"Video created: {output_path}")
        messagebox.showinfo("Done", f"Video created:\n{output_path}")


# Run App
if __name__ == "__main__":
    app = FiftyShadesGUI()
    app.mainloop()
