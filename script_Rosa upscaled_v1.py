import os
from PIL import Image

def create_svg_from_image(image_path, svg_path, scale_factor=2):
    # Open the image using Pillow
    img = Image.open(image_path)

    # Upscale the image
    new_size = (img.width * scale_factor, img.height * scale_factor)
    img_resized = img.resize(new_size, Image.Resampling.LANCZOS)

    # Save the upscaled image as BMP (intermediate format)
    temp_bmp_path = image_path.replace('.jpg', '.bmp')
    img_resized.save(temp_bmp_path, format='BMP')

    # Convert BMP to SVG using potrace
    os.system(f"potrace -s -o {svg_path} {temp_bmp_path}")

    # Remove the temporary BMP file
    os.remove(temp_bmp_path)

def convert_images_to_svg(input_folder, output_folder, scale_factor=2):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".jpg"):
            image_path = os.path.join(input_folder, filename)
            svg_filename = filename.replace('.jpg', '.svg')
            svg_path = os.path.join(output_folder, svg_filename)
            create_svg_from_image(image_path, svg_path, scale_factor)
            print(f"Converted and upscaled {filename} to {svg_filename}")

# Example usage
input_folder = "/home/jasvir/Music/Jacinta3/"
output_folder = "/home/jasvir/Music/Jacinta3/svg/"
convert_images_to_svg(input_folder, output_folder, scale_factor=2)
