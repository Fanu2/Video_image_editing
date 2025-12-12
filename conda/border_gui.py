import cv2
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, ttk, colorchooser, messagebox
import os


def add_border_cv2(image, border_size, border_color, frame_design=None):
    """Add border + optional frame image."""
    img = image.copy()

    # Add border
    bordered = cv2.copyMakeBorder(
        img,
        border_size,
        border_size,
        border_size,
        border_size,
        cv2.BORDER_CONSTANT,
        value=border_color
    )

    # Overlay frame design if provided
    if frame_design is not None:
        fh, fw = frame_design.shape[:2]
        h, w = bordered.shape[:2]

        frame_resized = cv2.resize(frame_design, (w, h))
        bordered = frame_resized

    return bordered


class BorderGUI:
    def __init__(self, root):
        self.root = root
        root.title("Image Border + Frame Designer")
        root.geometry("620x720")
        root.resizable(False, False)

        self.image_cv = None
        self.frame_cv = None
        self.preview_tk = None

        # --- GUI Elements ---
        tk.Button(root, text="Select Image", command=self.load_image).pack(pady=6)
        tk.Button(root, text="Select Frame Design (optional)", command=self.load_frame).pack(pady=6)

        # Border size
        size_frame = tk.Frame(root)
        size_frame.pack(pady=5)
        tk.Label(size_frame, text="Border Size:").pack(side="left")
        self.border_size = tk.IntVar(value=30)
        tk.Spinbox(size_frame, from_=0, to=200, textvariable=self.border_size, width=6).pack(side="left")

        # Border color
        color_frame = tk.Frame(root)
        color_frame.pack(pady=5)
        tk.Label(color_frame, text="Border Color:").pack(side="left")
        self.border_color = (255, 255, 255)
        tk.Button(color_frame, text="Pick Color", command=self.pick_color).pack(side="left")

        # Preview panel
        self.preview_label = tk.Label(root, text="Preview will appear here", bg="#ddd", width=60, height=20)
        self.preview_label.pack(pady=15)

        # Action buttons
        tk.Button(root, text="Generate Preview", command=self.update_preview).pack(pady=6)
        tk.Button(root, text="Save Image", command=self.export_image).pack(pady=10)

        self.status = tk.Label(root, text="Waiting...", fg="blue")
        self.status.pack()

    # ---------------------------
    def load_image(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.jpeg *.png")])
        if not path:
            return

        self.image_cv = cv2.imread(path)
        if self.image_cv is None:
            messagebox.showerror("Error", "Cannot load image.")
            return

        self.status.config(text="Image loaded ✔️", fg="green")
        self.update_preview()

    # ---------------------------
    def load_frame(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg")])
        if not path:
            return

        frame = cv2.imread(path)
        if frame is None:
            messagebox.showerror("Error", "Cannot load frame design.")
            return

        self.frame_cv = frame
        self.status.config(text="Frame design loaded ✔️", fg="green")
        self.update_preview()

    # ---------------------------
    def pick_color(self):
        color = colorchooser.askcolor(title="Choose Border Color")
        if color[0] is not None:
            r, g, b = map(int, color[0])
            self.border_color = (b, g, r)  # Convert to BGR for OpenCV

    # ---------------------------
    def update_preview(self):
        if self.image_cv is None:
            return

        bordered = add_border_cv2(
            self.image_cv,
            border_size=self.border_size.get(),
            border_color=self.border_color,
            frame_design=self.frame_cv
        )

        preview = cv2.cvtColor(bordered, cv2.COLOR_BGR2RGB)
        preview_pil = Image.fromarray(preview)
        preview_pil.thumbnail((580, 580))

        self.preview_tk = ImageTk.PhotoImage(preview_pil)
        self.preview_label.configure(image=self.preview_tk)
        self.preview_label.image = self.preview_tk

        self.status.config(text="Preview updated ✔️", fg="green")

    # ---------------------------
    def export_image(self):
        if self.image_cv is None:
            messagebox.showerror("Error", "Load an image first.")
            return

        path = filedialog.asksaveasfilename(defaultextension=".jpg")
        if not path:
            return

        bordered = add_border_cv2(
            self.image_cv,
            border_size=self.border_size.get(),
            border_color=self.border_color,
            frame_design=self.frame_cv
        )

        cv2.imwrite(path, bordered)
        self.status.config(text="Image saved ✔️", fg="green")
        messagebox.showinfo("Saved", f"Image saved:\n{path}")


# ---------------------------
# Run App
# ---------------------------
if __name__ == "__main__":
    root = tk.Tk()
    BorderGUI(root)
    root.mainloop()

