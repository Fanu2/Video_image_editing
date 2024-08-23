import os
import tkinter as tk
from PIL import Image, ImageTk
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


class ImageSlideshow:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Slideshow")
        self.images_folder = "/home/jasvir/Documents/Slide show/"  # Update with your image folder path
        self.images = self.load_images_from_folder(self.images_folder)
        self.current_image_index = 0
        self.total_images = len(self.images)

        # Display image
        self.image_label = tk.Label(self.root)
        self.image_label.pack()

        # Buttons for navigation
        self.prev_button = tk.Button(self.root, text='Previous', command=self.show_previous_image)
        self.prev_button.pack(side='left')

        self.next_button = tk.Button(self.root, text='Next', command=self.show_next_image)
        self.next_button.pack(side='right')

        # Save button
        self.save_pdf_button = tk.Button(self.root, text='Save as PDF', command=self.save_as_pdf)
        self.save_pdf_button.pack()

        # Show first image
        self.show_image(self.current_image_index)

    def load_images_from_folder(self, folder):
        images = []
        for filename in os.listdir(folder):
            if filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                image_path = os.path.join(folder, filename)
                images.append(Image.open(image_path))
        return images

    def show_image(self, index):
        image = self.images[index]
        image = image.resize((600, 400))  # Resize images as needed
        photo = ImageTk.PhotoImage(image)
        self.image_label.configure(image=photo)
        self.image_label.image = photo

    def show_previous_image(self):
        self.current_image_index = (self.current_image_index - 1) % self.total_images
        self.show_image(self.current_image_index)

    def show_next_image(self):
        self.current_image_index = (self.current_image_index + 1) % self.total_images
        self.show_image(self.current_image_index)

    def save_as_pdf(self):
        pdf_filename = "slideshow_pdf.pdf"
        pdf_path = os.path.join(self.images_folder, pdf_filename)

        # Create PDF canvas
        c = canvas.Canvas(pdf_path, pagesize=letter)

        # Iterate through images and add to PDF pages
        for image in self.images:
            image_resized = image.resize((500, 350))  # Resize images as needed
            c.drawImage(image_resized, 50, 50, width=image_resized.width, height=image_resized.height)
            c.showPage()

        c.save()
        print(f"Slideshow saved as PDF: {pdf_path}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageSlideshow(root)
    root.mainloop()
