import tkinter as tk
from tkinter import filedialog, ttk, colorchooser, messagebox
from PIL import Image, ImageOps, ImageTk
import threading


# ============================================
# IMAGE COMBINE LOGIC
# ============================================
def resize_images_to_same_size(image1, image2, size):
    img1_resized = image1.resize(size, Image.LANCZOS)
    img2_resized = image2.resize(size, Image.LANCZOS)
    return img1_resized, img2_resized


def combine_images_with_border(image1_path, image2_path, output_path, size, border_size=10, background_color=(255, 255, 255)):
    img1 = Image.open(image1_path)
    img2 = Image.open(image2_path)

    img1_resized, img2_resized = resize_images_to_same_size(img1, img2, size)

    total_width = img1_resized.width + img2_resized.width + 3 * border_size
    max_height = max(img1_resized.height, img2_resized.height) + 2 * border_size

    new_image = Image.new('RGB', (total_width, max_height), background_color)

    new_image.paste(
        ImageOps.expand(img1_resized, border=border_size, fill=background_color),
        (border_size, border_size)
    )

    new_image.paste(
        ImageOps.expand(img2_resized, border=border_size, fill=background_color),
        (img1_resized.width + 2 * border_size, border_size)
    )

    new_image.save(output_path)


# ============================================
# GUI APPLICATION
# ============================================
class ImageCombinerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("📸 Image Combiner – Beautiful GUI")
        self.root.geometry("660x520")
        self.root.configure(bg="#1e1e1e")

        self.image1_path = None
        self.image2_path = None
        self.bg_color = (255, 255, 255)

        self.create_ui()

    # ----------------------------------------
    def create_ui(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", padding=6, relief="flat", background="#3b3b3b", foreground="white")
        style.map("TButton", background=[("active", "#505050")])

        # Top section
        frame = tk.Frame(self.root, bg="#1e1e1e")
        frame.pack(pady=10)

        ttk.Button(frame, text="Select Image 1", command=self.load_image1).grid(row=0, column=0, padx=10)
        ttk.Button(frame, text="Select Image 2", command=self.load_image2).grid(row=0, column=1, padx=10)

        # Preview area
        preview_frame = tk.Frame(self.root, bg="#1e1e1e")
        preview_frame.pack()

        self.preview1 = tk.Label(preview_frame, bg="#1e1e1e")
        self.preview1.grid(row=0, column=0, padx=10)

        self.preview2 = tk.Label(preview_frame, bg="#1e1e1e")
        self.preview2.grid(row=0, column=1, padx=10)

        # Inputs
        settings = tk.Frame(self.root, bg="#1e1e1e")
        settings.pack(pady=20)

        tk.Label(settings, text="Resize Width:", fg="white", bg="#1e1e1e").grid(row=0, column=0)
        self.width_entry = tk.Entry(settings, width=6)
        self.width_entry.insert(0, "300")
        self.width_entry.grid(row=0, column=1, padx=8)

        tk.Label(settings, text="Resize Height:", fg="white", bg="#1e1e1e").grid(row=0, column=2)
        self.height_entry = tk.Entry(settings, width=6)
        self.height_entry.insert(0, "300")
        self.height_entry.grid(row=0, column=3, padx=8)

        tk.Label(settings, text="Border Size:", fg="white", bg="#1e1e1e").grid(row=1, column=0, pady=10)
        self.border_entry = tk.Entry(settings, width=6)
        self.border_entry.insert(0, "10")
        self.border_entry.grid(row=1, column=1, padx=8)

        ttk.Button(settings, text="Pick Background Color", command=self.pick_color).grid(row=1, column=2, padx=10)

        # Export button
        ttk.Button(self.root, text="✨ Combine & Save", command=self.start_process).pack(pady=10)

        # Status
        self.status = tk.Label(self.root, text="Waiting...", fg="lightgray", bg="#1e1e1e")
        self.status.pack()

    # ----------------------------------------
    def update_preview(self, label, path):
        if not path:
            return
        img = Image.open(path)
        img.thumbnail((200, 200))
        tk_img = ImageTk.PhotoImage(img)
        label.configure(image=tk_img)
        label.image = tk_img

    # ----------------------------------------
    def load_image1(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.jpeg *.png")])
        if path:
            self.image1_path = path
            self.update_preview(self.preview1, path)
            self.status.config(text="Image 1 Loaded ✔")

    # ----------------------------------------
    def load_image2(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.jpeg *.png")])
        if path:
            self.image2_path = path
            self.update_preview(self.preview2, path)
            self.status.config(text="Image 2 Loaded ✔")

    # ----------------------------------------
    def pick_color(self):
        color = colorchooser.askcolor(initialcolor=self.bg_color)
        if color and color[0]:
            self.bg_color = tuple(map(int, color[0]))
            self.status.config(text=f"Selected Color: {self.bg_color}")

    # ----------------------------------------
    def start_process(self):
        if not self.image1_path or not self.image2_path:
            self.status.config(text="❌ Select both images first!", fg="red")
            return

        threading.Thread(target=self.process, daemon=True).start()

    # ----------------------------------------
    def process(self):
        try:
            self.status.config(text="Processing...", fg="orange")

            width = int(self.width_entry.get())
            height = int(self.height_entry.get())
            border = int(self.border_entry.get())

            save_path = filedialog.asksaveasfilename(defaultextension=".jpg")
            if not save_path:
                return

            combine_images_with_border(
                self.image1_path,
                self.image2_path,
                save_path,
                size=(width, height),
                border_size=border,
                background_color=self.bg_color
            )

            self.status.config(text=f"✔ Saved Successfully: {save_path}", fg="green")

        except Exception as e:
            self.status.config(text=f"Error: {e}", fg="red")


# ============================================
# RUN APP
# ============================================
root = tk.Tk()
app = ImageCombinerGUI(root)
root.mainloop()
