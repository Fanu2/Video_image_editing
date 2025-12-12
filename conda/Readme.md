

# 🎥 Video Creation & Editing GUI (Conda-Compatible)

This repository contains a modern, fully Conda-friendly **Tkinter-based multimedia GUI application** for:

* Creating videos from **folders of images**
* Adding **background music** (loop or trim automatically)
* Adding **text overlays** (fully customizable)
* Choosing **platform presets** (TikTok, YouTube, Instagram, Facebook, Custom)
* Importing existing videos and **replacing their audio**
* Exporting high-quality **MP4** videos without ImageMagick

All tools run entirely inside a standard **Conda environment** — no external GUI frameworks or system-level dependencies needed.

---

# 📦 Features

## 1️⃣ **Create Video From Images**

* Select a folder of `.png` / `.jpg` images.
* Choose FPS (12 / 24 / 30 / 60).
* Choose image duration.
* Optional crossfade transitions.
* Choose platform presets:

  * YouTube 16:9 (1920×1080)
  * TikTok 9:16 (1080×1920)
  * Instagram Square 1:1 (1080×1080)
  * Facebook 720p (1280×720)
  * Custom resolution
* Add optional background music (supports `.mp3`, `.wav`, `.aac`, `.m4a`, etc.)
* Add optional global text overlay.

## 2️⃣ **Replace Audio in Existing Video**

* Import any MP4, MOV, AVI, MKV video.
* Strip all existing audio.
* Add new background music.
* Auto-loop audio to match video duration.
* Optional text overlay.
* Optional automatic resizing to platform presets.

## 3️⃣ **Text Overlay System**

* Fully PIL-based — **no ImageMagick required**.
* Supports:

  * Custom font size
  * RGB(A) color input
  * Position: top / center / bottom
* Clean anti-aliased rendering using Pillow.

## 4️⃣ **Built-in Tkinter GUI**

* Zero dependencies beyond Conda packages.
* Clean, modern layout.
* File dialogs for folders, video files, audio files.
* Status bar + progress bar.
* Non-blocking worker thread design keeps UI responsive.
* Output folder quick-open button.

## 5️⃣ **Cross-platform**

* Works on:

  * Windows
  * macOS
  * Linux
* Uses system font detection to avoid missing-font errors.

---

# 🐍 Conda Installation

The application requires only three non-standard packages:

```bash
conda install -c conda-forge moviepy pillow numpy
```

Tkinter comes with most Conda Python builds.
If missing on Linux:

```bash
sudo apt install python3-tk
```

---

# 🚀 Running the Application

Save the script as:

```
video_maker_gui.py
```

Run with:

```bash
python video_maker_gui.py
```

---

# 📁 Project Structure

```
.
├── video_maker_gui.py     # Full Tkinter GUI app
└── README.md              # This documentation
```

---

# 🛠 Technical Design Overview

### ✔ MoviePy

Used for:

* Image slideshows
* Video resizing
* Crossfade transitions
* Audio loop & attach
* Rendering MP4 with libx264

### ✔ Pillow (PIL)

Used for:

* Loading images
* Resizing with aspect-ratio padding
* Rendering text overlays **without ImageMagick**
* Creating RGBA overlays for videos

### ✔ Tkinter

Handles:

* GUI framework
* Folder/file pickers
* Buttons, inputs, selectors
* Progress bar
* Multithreading-safe queue for status updates

### ✔ Multithreading

Rendering happens in a worker thread.
UI remains **responsive**.

---

# 🧩 Key Features Developed for You

This README covers all GUI functionalities we created together:

| Feature                       | Status | Notes                                      |
| ----------------------------- | ------ | ------------------------------------------ |
| Image → Video generator       | ✅      | With music, text, FPS control, transitions |
| Video → Replace audio         | ✅      | Removes original audio and adds new track  |
| Text overlay system           | ✅      | No ImageMagick; fully PIL-based            |
| TikTok / YouTube / FB presets | ✅      | Automatic resolution handling              |
| Crossfade transitions         | ✅      | Optional                                   |
| Non-blocking UI               | ✅      | Threaded rendering                         |
| Real-time status updates      | ✅      | Tkinter label + queue                      |
| Progress bar                  | ✅      | Smooth staged progress                     |
| Audio looping / trimming      | ✅      | Automatic                                  |
| System font detection         | ✅      | Windows/Mac/Linux safe                     |

---

# 📤 Output

All videos are rendered as:

* MP4 container
* H.264 codec
* AAC audio
* Fully platform-optimized

---

# 🙋 Need More Features?

I can extend the GUI with:

* Per-image captions
* Per-image duration & transitions
* Drag-and-drop image ordering
* Video preview window
* Multi-layer overlays (stickers, logos, watermarks)
* Ken Burns panning effect
* GPU accelerated encoding
* Export presets for shorts/reels with safe-frame guides

Just tell me what you'd like!

---

# ❤️ Thank You

Your GUI suite is now fully ready for video creation, editing, and social media production — 100% Conda-friendly and cross-platform.

If you want this turned into a **standalone EXE / APP**, **Qt-based version**, or **web app**, I can build that next.
