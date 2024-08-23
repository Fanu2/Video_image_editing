from PIL import Image, ImageDraw, ImageFont
import os


def insert_text(image_path, text, font_path, font_size, position, output_path):
    # Open the image file
    with Image.open(image_path) as img:
        # Check image mode
        if img.mode != 'RGB':
            img = img.convert('RGB')

        # Initialize ImageDraw
        draw = ImageDraw.Draw(img)

        # Load the font
        try:
            font = ImageFont.truetype(font_path, font_size)
        except IOError:
            print(f"Font file '{font_path}' not found.")
            return

        # Draw text on image
        try:
            draw.text(position, text, font=font, fill="white")  # Change fill color if needed
        except Exception as e:
            print(f"Error drawing text: {e}")
            return

        # Save the image with text
        img.save(output_path)
        print(f"Image saved with text at {output_path}")


def main():
    # Path to the image
    image_path = '//home/jasvir/Music/Movie work/Insert text into image/1.jpg'

    # Text to insert
    text = "Jodha my love"

    # Path to the font file
    font_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf'

    # Font size
    font_size = 36

    # Text position (x, y)
    position = (50, 450)

    # Output path
    output_path = '/home/jasvir/Music/Movie work/Insert text into image/output_image.jpg'

    # Insert text into image
    insert_text(image_path, text, font_path, font_size, position, output_path)


if __name__ == "__main__":
    main()
