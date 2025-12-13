
# 🌟 Image-to-Video Overlay GUI

### A Modern PySide6 Application for Creative Video Compositing

Overlay images onto videos with alpha gradients, fades, precise positioning, and timing — all in a clean, intuitive GUI. Perfect for lyric videos, slideshow overlays, branding, artistic effects, and more.

---

## ✨ Features

### 🎥 Video Input

* Load local videos (`.mp4`, `.mov`, `.mkv`)
* Load videos directly from **URLs** (YouTube, social platforms) using **yt-dlp**
* Automatic temporary handling of downloaded content

---

### 🖼 Image Overlays

* Import an entire folder of `.png`, `.jpg`, `.jpeg`
* Multi-select support
* Apply properties to **selected images** or **all images**
* Per-image preview pane

---

### 🎨 Overlay Controls (Per Image)

| Property               | Description                             |
| ---------------------- | --------------------------------------- |
| **X/Y Position**       | Normalized coordinates (0–1)            |
| **Scale**              | Relative to video width                 |
| **Alpha Gradient**     | Top/Bottom transparency blending        |
| **Start / End Time**   | Control exactly when each image appears |
| **Fade-In / Fade-Out** | Smooth transitions                      |

---

### 🕒 Timeline View

Visual listing of each image’s active time range.
Great for verifying synchronization.

---

### 🧰 Rendering Engine

* Uses **MoviePy** + **FFmpeg**
* Background rendering via QThread to keep UI responsive
* Detailed status and progress updates
* Full error reporting with tracebacks
* Outputs clean MP4 (`H.264 + AAC`)

---

## 📦 Installation

### 1. Install Dependencies

```bash
pip install PySide6 moviepy Pillow numpy yt-dlp
```

### 2. Install FFmpeg

Linux (Debian/MX/Ubuntu):

```bash
sudo apt install ffmpeg
```

Check installation:

```bash
ffmpeg -version
```

---

## 🚀 Usage

Run the GUI:

```bash
python image_to_video_overlay_gui.py
```

### Workflow

1. **Open Video** or **Load URL**
2. **Open Images Folder**
3. Select images → adjust properties
4. Click **Apply to Selected** or **Apply to All**
5. Choose **Output File**
6. Click **Render Video**

Your beautifully composited MP4 will appear at the chosen output path.

---

## 🛠 Advanced Tips

### Faster Rendering

MoviePy is CPU-based and may be slow for large projects.
Optimizations available:

* GPU encoding (NVENC/VAAPI)
* FFmpeg-layer compositing (10–20× faster)
* Image caching
* Resolution pre-scaling

Ask me if you want these upgrades added.

---

## ⚠ Notes

### DBus Warnings

On lightweight Linux environments, you may see:

```
qt.qpa.theme.dbus: Session DBus not running.
```

This is **harmless** and does not affect functionality.

### Stopping Mid-Render

Stopping the GUI while rendering:

* Does not harm your system
* Leaves a partial, unusable output file (safe to delete)
* FFmpeg processes may run briefly but clean up automatically

A **Cancel Render** button can be added on request.

---

## 🧩 Project Structure (Single-File Application)

```
image_to_video_overlay_gui.py
```

* GUI Layout (PySide6)
* Video/Image loading
* Overlay item model
* Alpha gradient engine (Pillow + NumPy)
* MoviePy render worker in QThread
* URL downloader (yt-dlp)
* Timeline and preview components

---

## ❤️ Contributing / Improvements

Planned or optional enhancements:

* Drag-and-drop images
* Real video preview with overlay simulation
* Multiple overlay groups
* Keyframed animation
* GPU render pipeline
* Project save/load system

Tell me what you want next — I can build it.

---

## 📄 License

This project is completely yours; choose any license you prefer.
I can generate MIT/GPL/Apache licenses on request.

