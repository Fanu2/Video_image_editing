import os
import numpy as np
import platform
from tkinter import Tk, Label, Entry, Button, filedialog, StringVar, OptionMenu, messagebox
from moviepy.editor import ImageSequenceClip
from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------
# FONT HANDLER
# ---------------------------------------------------------
def get_default_font(size=70):
    """Return a default font from system or fallback."""
    try:
        if platform.system() == "Windows":
            font_path = "C:\\Windows\\Fonts\\arial.ttf"
        elif platform.system() == "Darwin":
            font_path = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
        else:
            font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

        return ImageFont.truetype(font_path, size=size)

    except IOError:
        print("Font not found, using default PIL font.")
        return ImageFont.load_default()


# ---------------------------------------------------------
# IMAGE PROCESSING
# ---------------------------------------------------------
def add_text_to_image(image_path, text):
    img = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(img)
    font = get_default_font(size=70)

    # Center text
    text_bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
    x = (img.width - tw) // 2
    y = img.height - th - 40

    draw.text((x, y), text, fill="white", font=font)
    return np.array(img)


def resize_image(img_array, target_size):
    img = Image.fromarray(img_array)
    img = img.resize(target_size)
    return np.array(img)


# ---------------------------------------------------------
# VIDEO CREATION
# ---------------------------------------------------------
def create_animation(folder, output, text, fps, resolution):
    if not os.path.isdir(folder):
        raise FileNotFoundError("Invalid folder!")

    file_list = sorted([f for f in os.listdir(folder) if f.lower().endswith(('.jpg', '.png'))])
    if not file_list:
        raise ValueError("No images found in selected folder.")

    target_size = tuple(map(int, resolution.split("x")))

    frames = []
    for file in file_list:
        path = os.path.join(folder, file)
        frame = add_text_to_image(path, text)
        frame = resize_image(frame, target_size)
        frames.append(frame)

    clip = ImageSequenceClip(frames, fps=int(fps))
    clip.write_videofile(output, codec="libx264", fps=int(fps))

    return True


# ---------------------------------------------------------
# GUI APPLICATION
# ---------------------------------------------------------
class App:
    def __init__(self, root):
        self.root = root
        root.title("Video Animation Creator")
        root.geometry("500x350")

        # Folder
        Label(root, text="Input Image Folder:").pack()
        self.folder_var = StringVar()
        Entry(root, textvariable=self.folder_var, width=50).pack()
        Button(root, text="Browse", command=self.select_folder).pack()

        # Output file
        Label(root, text="Output Video File (mp4):").pack()
        self.output_var = StringVar(value="output.mp4")
        Entry(root, textvariable=self.output_var, width=50).pack()

        # Text overlay
        Label(root, text="Overlay Text:").pack()
        self.text_var = StringVar(value="Love u Jodha")
        Entry(root, textvariable=self.text_var, width=50).pack()

        # FPS
        Label(root, text="FPS:").pack()
        self.fps_var = StringVar(value="24")
        fps_options = ["12", "24", "30", "60"]
        OptionMenu(root, self.fps_var, *fps_options).pack()

        # Resolution
        Label(root, text="Resolution:").pack()
        self.res_var = StringVar(value="1920x1080")
        res_options = ["1280x720", "1920x1080", "2560x1440"]
        OptionMenu(root, self.res_var, *res_options).pack()

        # Create button
        Button(root, text="Create Video", command=self.run).pack(pady=15)

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_var.set(folder)

    def run(self):
        folder = self.folder_var.get()
        output = self.output_var.get()
        text = self.text_var.get()
        fps = self.fps_var.get()
        resolution = self.res_var.get()

        if not folder:
            messagebox.showerror("Error", "Please select a folder.")
            return

        try:
            create_animation(folder, output, text, fps, resolution)
            messagebox.showinfo("Success", "Video created successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))


# ---------------------------------------------------------
# START GUI
# ---------------------------------------------------------
if __name__ == "__main__":
    root = Tk()
    App(root)
    root.mainloop()

