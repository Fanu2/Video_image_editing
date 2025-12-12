import subprocess
import json
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import threading


# ==============================
# Get video duration using ffprobe
# ==============================
def get_video_duration(video_path):
    command = [
        "ffprobe",
        "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=duration",
        "-of", "json",
        video_path
    ]
    result = subprocess.run(command, capture_output=True, text=True)

    try:
        data = json.loads(result.stdout)
        return float(data["streams"][0]["duration"])
    except Exception as e:
        raise RuntimeError(f"Could not read video duration:\n{e}")


# ==============================
# GUI CLASS
# ==============================
class PiPVideoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎬 Picture-in-Picture Video Maker")
        self.root.geometry("600x560")
        self.root.resizable(False, False)

        self.bg_video = None
        self.pip_video = None

        self.build_ui()

    def build_ui(self):
        pad = {"padx": 10, "pady": 6}

        ttk.Label(self.root, text="🎞 Background Video").pack(anchor="w", **pad)
        tk.Button(self.root, text="Select Background Video", command=self.select_bg).pack(fill="x", **pad)

        ttk.Label(self.root, text="📌 PiP Video").pack(anchor="w", **pad)
        tk.Button(self.root, text="Select PiP Video", command=self.select_pip).pack(fill="x", **pad)

        # -------------------------
        # PiP POSITION CONTROLS
        # -------------------------
        frm_pos = ttk.LabelFrame(self.root, text="PiP Position (pixels)")
        frm_pos.pack(fill="x", padx=10, pady=10)

        self.x_scale = tk.Scale(frm_pos, from_=0, to=1000, orient="horizontal", label="X Offset")
        self.x_scale.pack(fill="x", padx=5, pady=5)

        self.y_scale = tk.Scale(frm_pos, from_=0, to=1000, orient="horizontal", label="Y Offset")
        self.y_scale.pack(fill="x", padx=5, pady=5)

        # -------------------------
        # PiP SIZE CONTROLS
        # -------------------------
        frm_size = ttk.LabelFrame(self.root, text="PiP Size (pixels)")
        frm_size.pack(fill="x", padx=10, pady=10)

        self.w_scale = tk.Scale(frm_size, from_=50, to=1000, orient="horizontal", label="Width")
        self.w_scale.set(320)
        self.w_scale.pack(fill="x", padx=5, pady=5)

        self.h_scale = tk.Scale(frm_size, from_=50, to=1000, orient="horizontal", label="Height")
        self.h_scale.set(180)
        self.h_scale.pack(fill="x", padx=5, pady=5)

        # -------------------------
        # CREATE BUTTON
        # -------------------------
        tk.Button(self.root, text="🚀 Create PiP Video", command=self.start_thread)\
            .pack(fill="x", padx=10, pady=15)

        # Progress + status
        self.progress = ttk.Progressbar(self.root, length=500)
        self.progress.pack(pady=4)

        self.status = ttk.Label(self.root, text="Waiting...", foreground="blue")
        self.status.pack()

    # ==========================
    # File Selection
    # ==========================
    def select_bg(self):
        path = filedialog.askopenfilename(filetypes=[("Videos", "*.mp4 *.mov *.mkv")])
        if path:
            self.bg_video = path
            self.status.config(text="Background video selected ✔", foreground="green")

    def select_pip(self):
        path = filedialog.askopenfilename(filetypes=[("Videos", "*.mp4 *.mov *.mkv")])
        if path:
            self.pip_video = path
            self.status.config(text="PiP video selected ✔", foreground="green")

    # ==========================
    # Thread wrapper
    # ==========================
    def start_thread(self):
        thread = threading.Thread(target=self.create_video_safe)
        thread.start()

    def create_video_safe(self):
        try:
            self.progress["value"] = 0
            self.status.config(text="Processing...", foreground="orange")
            self.create_pip_video()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status.config(text="❌ Error occurred", foreground="red")

    # ==========================
    # MAIN PROCESS
    # ==========================
    def create_pip_video(self):

        if not self.bg_video:
            raise RuntimeError("Select a background video first!")
        if not self.pip_video:
            raise RuntimeError("Select a PiP video first!")

        save_path = filedialog.asksaveasfilename(defaultextension=".mp4")
        if not save_path:
            return

        self.progress["value"] = 10

        # Get durations
        bg_dur = get_video_duration(self.bg_video)
        pip_dur = get_video_duration(self.pip_video)
        shortest = min(bg_dur, pip_dur)

        x = int(self.x_scale.get())
        y = int(self.y_scale.get())
        w = int(self.w_scale.get())
        h = int(self.h_scale.get())

        self.status.config(text="Running FFmpeg…")

        cmd = [
            "ffmpeg",
            "-i", self.bg_video,
            "-i", self.pip_video,
            "-filter_complex",
            f"[1:v]scale={w}:{h}[pip];[0:v][pip]overlay={x}:{y}",
            "-codec:a", "copy",
            "-t", str(shortest),
            save_path
        ]

        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        for i in range(10, 100, 5):
            self.progress["value"] = i
            self.root.update_idletasks()

        process.wait()

        if process.returncode != 0:
            stderr = process.stderr.read()
            raise RuntimeError(f"FFmpeg failed:\n{stderr}")

        self.progress["value"] = 100
        self.status.config(text="✔ PiP Video Created Successfully!", foreground="green")
        messagebox.showinfo("Success", f"Video saved:\n{save_path}")


# ==========================
# RUN APPLICATION
# ==========================
if __name__ == "__main__":
    root = tk.Tk()
    app = PiPVideoGUI(root)
    root.mainloop()
