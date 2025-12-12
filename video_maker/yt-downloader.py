import os
import subprocess
import threading
from tkinter import *
from tkinter import filedialog, messagebox, ttk

# ---------------------------
# GUI Application
# ---------------------------

class YTDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader (yt-dlp GUI)")
        self.root.geometry("600x420")
        self.root.resizable(False, False)

        # Variables
        self.url_var = StringVar()
        self.format_var = StringVar(value="best")
        self.output_folder_var = StringVar()
        self.status_var = StringVar(value="Ready")

        self._build_ui()

    # ---------------------------
    # UI Layout
    # ---------------------------
    def _build_ui(self):
        pad = {"padx": 10, "pady": 6}

        Label(self.root, text="YouTube / Video URL:", font=("Segoe UI", 10)).pack(anchor="w", **pad)
        Entry(self.root, textvariable=self.url_var, width=70).pack(**pad)

        Label(self.root, text="Download Type:", font=("Segoe UI", 10)).pack(anchor="w", **pad)

        format_frame = Frame(self.root)
        format_frame.pack(fill="x", padx=10)

        # Format dropdown
        formats = [
            ("Best Quality (Video+Audio)", "best"),
            ("Audio Only - MP3", "bestaudio[ext=mp3]/bestaudio"),
            ("Audio Only - M4A", "bestaudio[ext=m4a]/bestaudio"),
            ("1080p Video", "bestvideo[height<=1080]+bestaudio/best"),
            ("720p Video", "bestvideo[height<=720]+bestaudio/best"),
            ("Worst Quality", "worst")
        ]

        self.format_menu = ttk.Combobox(format_frame, textvariable=self.format_var,
                                        values=[f[0] for f in formats],
                                        state="readonly", width=40)
        self.format_menu.current(0)
        self.format_menu.pack(side="left")

        # Output folder
        Label(self.root, text="Output Folder:", font=("Segoe UI", 10)).pack(anchor="w", **pad)
        out_frame = Frame(self.root)
        out_frame.pack(fill="x", padx=10)

        Entry(out_frame, textvariable=self.output_folder_var, width=45).pack(side="left")
        Button(out_frame, text="Browse", command=self._choose_folder).pack(side="left", padx=6)

        # Download Button
        Button(self.root, text="Download", command=self._start_download,
               bg="#4CAF50", fg="white", width=20).pack(pady=12)

        # Progress Bar
        self.progress = ttk.Progressbar(self.root, mode="indeterminate", length=560)
        self.progress.pack(padx=10, pady=(0, 10))

        # Status Label
        Label(self.root, textvariable=self.status_var, anchor="w").pack(fill="x", padx=10)

        # Output console
        Label(self.root, text="Download Log:", font=("Segoe UI", 10)).pack(anchor="w", **pad)

        self.console = Text(self.root, height=8, state="disabled", bg="#1e1e1e", fg="#00ff00")
        self.console.pack(fill="x", padx=10)

    # ---------------------------
    # Folder Picker
    # ---------------------------
    def _choose_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_folder_var.set(folder)

    # ---------------------------
    # Start Thread
    # ---------------------------
    def _start_download(self):
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a video URL.")
            return

        output_folder = self.output_folder_var.get().strip() or os.getcwd()

        selected_format = self.format_menu.get()

        # Map dropdown label → yt-dlp format syntax
        format_map = {
            "Best Quality (Video+Audio)": "best",
            "Audio Only - MP3": "bestaudio[ext=mp3]/bestaudio",
            "Audio Only - M4A": "bestaudio[ext=m4a]/bestaudio",
            "1080p Video": "bestvideo[height<=1080]+bestaudio/best",
            "720p Video": "bestvideo[height<=720]+bestaudio/best",
            "Worst Quality": "worst"
        }

        yt_format = format_map.get(selected_format, "best")

        self.status_var.set("Downloading...")
        self.progress.start(10)

        thread = threading.Thread(
            target=self._download_video,
            args=(url, yt_format, output_folder),
            daemon=True
        )
        thread.start()

    # ---------------------------
    # Download using yt-dlp
    # ---------------------------
    def _download_video(self, url, yt_format, output_folder):
        try:
            self._write_console(f"Starting download...\nFormat: {yt_format}\nSaving to: {output_folder}\n")

            cmd = [
                "yt-dlp",
                "-f", yt_format,
                "--embed-subs",
                "--embed-thumbnail",
                "-o", os.path.join(output_folder, "%(title)s.%(ext)s"),
                url
            ]

            process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
            )

            # Live log output
            for line in process.stdout:
                self._write_console(line)

            process.wait()

            if process.returncode == 0:
                self.status_var.set("Download completed!")
                self._write_console("\n✔ Download Finished Successfully!\n")
            else:
                self.status_var.set("Error during download.")
                self._write_console("\n❌ Download failed.\n")

        except Exception as e:
            self.status_var.set("Error")
            self._write_console(f"\nERROR: {str(e)}\n")

        self.progress.stop()

    # ---------------------------
    # Console Writer
    # ---------------------------
    def _write_console(self, text):
        self.console.config(state="normal")
        self.console.insert("end", text)
        self.console.see("end")
        self.console.config(state="disabled")


# ---------------------------
# Main
# ---------------------------
def main():
    root = Tk()
    app = YTDownloaderGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

