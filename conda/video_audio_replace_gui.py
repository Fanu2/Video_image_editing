import tkinter as tk
from tkinter import filedialog, ttk
import os
import math
import threading

from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips


class AudioReplaceGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Audio Replacer – Loop Video to MP3 Length")
        self.root.geometry("540x260")
        self.root.resizable(False, False)

        self.video_folder = None
        self.audio_path = None

        tk.Button(root, text="Select Videos Folder", command=self.select_folder).pack(pady=5)
        tk.Button(root, text="Select MP3 Audio", command=self.select_audio).pack(pady=5)
        tk.Button(root, text="Start Processing", command=self.start_thread).pack(pady=10)

        self.progress = ttk.Progressbar(root, length=420)
        self.progress.pack(pady=10)

        self.status = tk.Label(root, text="Waiting...", fg="blue")
        self.status.pack(pady=5)

    # -------------------------------
    # SAFE UI UPDATE (THREAD-SAFE)
    # -------------------------------
    def update_ui(self, text=None, value=None, color=None):
        def handle():
            if text is not None:
                self.status.config(text=text)
            if value is not None:
                self.progress["value"] = value
            if color is not None:
                self.status.config(fg=color)

        self.root.after(0, handle)

    # -------------------------------
    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.video_folder = folder
            self.update_ui("Video folder selected ✅", 0, "green")

    def select_audio(self):
        path = filedialog.askopenfilename(filetypes=[("MP3 Audio", "*.mp3")])
        if path:
            self.audio_path = path
            self.update_ui("MP3 audio selected ✅", None, "green")

    def start_thread(self):
        threading.Thread(target=self.process_videos, daemon=True).start()

    # -------------------------------
    # MAIN PROCESS
    # -------------------------------
    def process_videos(self):
        if not self.video_folder:
            self.update_ui("Select videos folder first ❌", None, "red")
            return

        if not self.audio_path:
            self.update_ui("Select MP3 audio first ❌", None, "red")
            return

        output_dir = filedialog.askdirectory()
        if not output_dir:
            return

        videos = sorted(
            f for f in os.listdir(self.video_folder)
            if f.lower().endswith(".mp4")
        )

        if not videos:
            self.update_ui("No .mp4 files found in folder ❌", None, "red")
            return

        # Load audio once
        try:
            base_audio = AudioFileClip(self.audio_path)
            target_duration = base_audio.duration
        except Exception as e:
            print("Audio load error:", e)
            self.update_ui("Error loading audio ❌", None, "red")
            return

        total = len(videos)

        for i, filename in enumerate(videos, start=1):
            vid_path = os.path.join(self.video_folder, filename)
            output_name = os.path.splitext(filename)[0] + "_with_audio.mp4"
            out_path = os.path.join(output_dir, output_name)

            try:
                self.update_ui(
                    text=f"Processing {i}/{total}: {filename}",
                    value=((i - 1) / total) * 100,
                    color="orange"
                )

                clip = VideoFileClip(vid_path)
                fps = clip.fps or 24  # fallback if missing

                video_duration = clip.duration

                # Loop or trim to match audio duration
                if video_duration >= target_duration:
                    base_video = clip.subclip(0, target_duration)
                else:
                    loops = math.ceil(target_duration / video_duration)
                    long_video = concatenate_videoclips([clip] * loops, method="compose")
                    base_video = long_video.subclip(0, target_duration)

                final_clip = base_video.set_audio(base_audio)

                final_clip.write_videofile(
                    out_path,
                    codec="libx264",
                    audio_codec="aac",
                    fps=fps
                )

                # Free resources
                clip.close()
                base_video.close()
                final_clip.close()

            except Exception as e:
                print("Error processing video:", filename, e)
                continue

        base_audio.close()
        self.update_ui("✅ All videos processed!", 100, "green")


# -------------------------------
# RUN
# -------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = AudioReplaceGUI(root)
    root.mainloop()
