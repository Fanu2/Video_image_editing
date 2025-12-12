import os
import threading
import tempfile
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from PIL import Image
from moviepy.editor import ImageSequenceClip, AudioFileClip


# ==========================
# Core Resize Function
# ==========================
def resize_image(path, size):
    img = Image.open(path)
    return img.resize(size, Image.LANCZOS)


# ==========================
# Video Creation Logic
# ==========================
def create_video(images_folder, audio_path, save_path, size, progress_callback=None):
    image_files = sorted([
        os.path.join(images_folder, f)
        for f in os.listdir(images_folder)
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ])

    if not image_files:
        raise RuntimeError("No images found in the selected folder.")

    if not os.path.isfile(audio_path):
        raise RuntimeError("Invalid audio file selected.")

    audio_clip = AudioFileClip(audio_path)
    duration = audio_clip.duration
    frames_per_image = duration / len(image_files)

    resized_images = []
    temp_dir = tempfile.mkdtemp()

    # Resize images
    for i, img_path in enumerate(image_files):
        img = resize_image(img_path, size)
        temp_path = os.path.join(temp_dir, f"frame_{i}.jpg")
        img.save(temp_path, "JPEG")
        resized_images.append(temp_path)

        if progress_callback:
            progress_callback(int(((i + 1) / len(image_files)) * 40))

    # Create video
    clip = ImageSequenceClip(resized_images, durations=[frames_per_image] * len(resized_images))
    clip = clip.set_audio(audio_clip)

    if progress_callback:
        progress_callback(70)

    clip.write_videofile(save_path, codec="libx264", fps=24, audio_codec="aac")

    # Cleanup
    for p in resized_images:
        try:
            os.remove(p)
        except:
            pass

    if progress_callback:
        progress_callback(100)


# ==========================
# GUI
# ==========================
class ImageSoundVideoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎬 Images + Sound → Auto-Synced Video")
        self.root.geometry("600x360")
        self.root.resizable(False, False)

        self.images_folder = None
        self.audio_path = None

        self.build_ui()

    def build_ui(self):
        padding = {"padx": 8, "pady": 6}

        # Images folder
        tk.Button(self.root, text="📁 Select Images Folder", command=self.choose_folder)\
            .pack(fill="x", **padding)

        # Audio file
        tk.Button(self.root, text="🎵 Select MP3 Audio", command=self.choose_audio)\
            .pack(fill="x", **padding)

        # Resolution
        frame_res = tk.Frame(self.root)
        frame_res.pack(fill="x", **padding)

        tk.Label(frame_res, text="Resolution:").pack(side="left")
        self.res_var = tk.StringVar(value="1920x1080")
        resolutions = ["1920x1080", "1280x720", "1080x1920"]
        ttk.Combobox(frame_res, textvariable=self.res_var, values=resolutions, width=12)\
            .pack(side="left", padx=10)

        # Export button
        tk.Button(self.root, text="🎞 Create Video", command=self.start_thread)\
            .pack(fill="x", **padding)

        # Progress bar
        self.progress = ttk.Progressbar(self.root, length=500)
        self.progress.pack(pady=10)

        # Status
        self.status = tk.Label(self.root, text="Waiting...", fg="blue")
        self.status.pack()

    # ------------------- UI Helpers -------------------
    def choose_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.images_folder = folder
            self.status.config(text="Images folder selected ✔️", fg="green")

    def choose_audio(self):
        audio = filedialog.askopenfilename(filetypes=[("Audio", "*.mp3")])
        if audio:
            self.audio_path = audio
            self.status.config(text="Audio file selected ✔️", fg="green")

    def update_progress(self, value):
        self.progress["value"] = value
        self.root.update_idletasks()

    # ------------------- Thread -------------------
    def start_thread(self):
        thread = threading.Thread(target=self.create_video_safe)
        thread.start()

    # ------------------- Processing -------------------
    def create_video_safe(self):
        try:
            if not self.images_folder:
                raise RuntimeError("Please select an images folder.")
            if not self.audio_path:
                raise RuntimeError("Please select an MP3 audio file.")

            save_path = filedialog.asksaveasfilename(defaultextension=".mp4")
            if not save_path:
                return

            width, height = map(int, self.res_var.get().split("x"))
            size = (width, height)

            self.status.config(text="Processing...", fg="orange")
            self.progress["value"] = 0

            create_video(
                self.images_folder,
                self.audio_path,
                save_path,
                size,
                progress_callback=self.update_progress
            )

            self.status.config(text="✔️ Video Created Successfully!", fg="green")
            self.progress["value"] = 100

        except Exception as e:
            self.status.config(text=f"❌ {str(e)}", fg="red")
            messagebox.showerror("Error", str(e))


# ==========================
# RUN
# ==========================
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageSoundVideoGUI(root)
    root.mainloop()

