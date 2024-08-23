from PIL import Image, ImageEnhance, ImageOps

def apply_color_transformations(input_image_path, output_folder):
    # Open the original image
    image = Image.open(input_image_path)

    # Create a grayscale version
    grayscale_image = ImageOps.grayscale(image)
    grayscale_image.save(f"{output_folder}/grayscale.png")

    # Create a color-tinted version (e.g., red tint)
    red_tint = image.copy()
    red_layer = Image.new('RGB', red_tint.size, (255, 0, 0))  # Red color
    red_tint = Image.blend(red_tint, red_layer, alpha=0.3)  # Adjust alpha to control the tint strength
    red_tint.save(f"{output_folder}/red_tint.png")

    # Increase color saturation
    enhancer = ImageEnhance.Color(image)
    saturated_image = enhancer.enhance(2.0)  # Increase saturation by a factor of 2
    saturated_image.save(f"{output_folder}/saturated.png")

    # Decrease color saturation (desaturated image)
    desaturated_image = enhancer.enhance(0.5)  # Decrease saturation by a factor of 0.5
    desaturated_image.save(f"{output_folder}/desaturated.png")

    # Apply sepia tone
    sepia_image = ImageOps.colorize(grayscale_image, '#704214', '#C0C080')
    sepia_image.save(f"{output_folder}/sepia.png")

    # Invert colors
    inverted_image = ImageOps.invert(image.convert("RGB"))
    inverted_image.save(f"{output_folder}/inverted.png")

    print("Color transformations applied and images saved.")

# Define the paths
input_image_path = "/home/jasvir/Music/Fanu/abc.jpeg"  # Update with your input image path
output_folder = "/home/jasvir/Music/Fanu/Transformed_Images"  # Update with your desired output folder

# Ensure the output folder exists
import os
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Call the function to apply color transformations
apply_color_transformations(input_image_path, output_folder)
