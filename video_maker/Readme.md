
# 🌟 Multimedia Suite – Audio, Image & Video Creation Tools

### ✨ Powered by Python • MoviePy • Pillow • Mutagen • FFmpeg • Tkinter GUI

---

## 📦 Overview

This project contains two powerful, user-friendly multimedia tools:

---

## 🎧 **1. M4A Cover Editor (Auto-Fix Enabled)**

A modern Tkinter-based GUI that lets you:

* View embedded cover art inside `.m4a`, `.mp4`, `.m4b`
* Add or replace cover art with any image (`jpg/png/webp`)
* Add text overlays (color, font size, position)
* **Automatically fix corrupted or non-standard M4A files**
  (missing *moov* atom, wrong container, WebM/Opus renamed M4A, etc.)
* Works flawlessly with:

  * Paths containing **spaces**
  * Unicode filenames
  * Conda environments
* Safe saving using per-directory **unique temp files**

> 💡 Thanks to FFmpeg auto-fix + Mutagen tagging,
> this editor handles almost any broken audio file commonly downloaded from YouTube or TikTok.

---

## 🎬 **2. Audio + Images → Video Maker**

Create **professional-quality MP4 videos** from:

* A single audio track (MP3, M4A, WAV, FLAC, AAC, OGG...)
* A folder of images

Features:

### 🖼 Image Handling

* Images resized with **smart letterboxing**
* Loop images if too few
* Distribute evenly if looping is off
* Adjustable FPS
* Adjustable per-image duration
* Optional crossfade transitions

### 🎞 Resolution Presets

* **YouTube (1920×1080)**
* **TikTok Vertical (1080×1920)**
* **Instagram Square (1080×1080)**
* **Custom resolution input**

### ✍ Text Overlays

* Customizable text
* Font size selection
* Top / Center / Bottom
* Color picker
* Anti-aliased outline for readability

### 💾 Output

* Safe temp video writing using FFmpeg
* Automatic audio/video synchronization
* Threaded rendering (GUI stays responsive)

---

---

# 🚀 Installation

### ✔ 1. Create or activate your Conda environment

```bash
conda create -n media python=3.10
conda activate media
```

### ✔ 2. Install required dependencies

```bash
conda install -c conda-forge moviepy pillow numpy python-mutagen ffmpeg
```

---

# 📁 File Structure

```
multimedia_suite/
│
├── m4a_cover_editor.py
├── audio_images_video_maker.py
└── README.md   ← (this file)
```

---

# 🖥 Running the Apps

## 🎵 Run M4A Cover Editor

```bash
python m4a_cover_editor.py
```

## 🎥 Run Audio + Images → Video Maker

```bash
python audio_images_video_maker.py
```

---

# 🧠 How It Works (Short Technical Overview)

### 🔧 M4A Auto-Fixing

Many files downloaded from YouTube Shorts / Reels appear as `.m4a` but are actually:

* WebM
* Opus
* Missing `moov` atom
* Incomplete MP4 headers

The editor automatically:

1. Detects invalid containers using **ffprobe**
2. Attempts a **remux** (copy streams → proper M4A)
3. If that fails → **re-encodes to AAC** with FFmpeg
4. Only then embeds cover art using Mutagen
5. Writes safely via unique `mkstemp()` temporary files

This design makes the editor extremely reliable even with broken source files.

---

# 🎨 Screenshots (optional placeholders)

> **You can replace these with real screenshots later.**

### M4A Cover Editor

```
+-----------------------------+
|      [ current cover ]      |
|   (extract / replace UI )   |
+-----------------------------+
```

### Audio + Images → Video Maker

```
+-------------------------------------+
| audio file  [ browse ]              |
| images folder [ browse ]            |
| resolution preset (TikTok/YouTube)  |
| fps | crossfade | display time      |
| text overlay settings               |
| [ Create Video ]                    |
+-------------------------------------+
```

---

# 🔮 Future Enhancements (optional)

You can request ChatGPT to add:

* Batch cover editing for multiple M4A files
* Ken Burns zoom/pan effect for images
* Per-image captions
* AI-generated covers or backgrounds
* Drag-and-drop image reordering
* Spotify-style lyric animations
* Adjustable audio fade-in/out
* Full preset manager (bitrate, CRF, profiles)

---

# ❤️ Credits

Developed with:

* **Python 3.10+**
* **MoviePy**
* **Pillow**
* **Mutagen**
* **FFmpeg**
* **Tkinter**

Special thanks to ChatGPT for generating high-quality, production-ready code and documentation.

---

# 📜 License

MIT License — free to use, modify, and distribute.

---

If you'd like, I can also:

📌 Create icons & branding
📌 Add screenshots
📌 Format README with emojis or minimal style
📌 Generate a setup.py / pyinstaller build

Just tell me!
