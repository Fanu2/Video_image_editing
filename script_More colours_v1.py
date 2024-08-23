from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import os

def apply_color_transformations(input_image_path, output_folder):
    # Open the original image
    image = Image.open(input_image_path)

    # Create a grayscale version
    grayscale_image = ImageOps.grayscale(image)
    grayscale_image.save(f"{output_folder}/grayscale_{os.path.basename(input_image_path)}")

    # Create color-tinted versions (red, green, blue)
    for color, tint_name in [((255, 0, 0), "red"), ((0, 255, 0), "green"), ((0, 0, 255), "blue")]:
        tinted_image = image.copy()
        color_layer = Image.new('RGB', tinted_image.size, color)
        tinted_image = Image.blend(tinted_image, color_layer, alpha=0.3)  # Adjust alpha to control the tint strength
        tinted_image.save(f"{output_folder}/{tint_name}_tint_{os.path.basename(input_image_path)}")

    # Increase and decrease color saturation
    enhancer = ImageEnhance.Color(image)
    saturated_image = enhancer.enhance(2.0)  # Increase saturation by a factor of 2
    saturated_image.save(f"{output_folder}/saturated_{os.path.basename(input_image_path)}")
    desaturated_image = enhancer.enhance(0.5)  # Decrease saturation by a factor of 0.5
    desaturated_image.save(f"{output_folder}/desaturated_{os.path.basename(input_image_path)}")

    # Apply sepia tone
    sepia_image = ImageOps.colorize(grayscale_image, '#704214', '#C0C080')
    sepia_image.save(f"{output_folder}/sepia_{os.path.basename(input_image_path)}")

    # Invert colors
    inverted_image = ImageOps.invert(image.convert("RGB"))
    inverted_image.save(f"{output_folder}/inverted_{os.path.basename(input_image_path)}")

    # Increase and decrease brightness
    enhancer = ImageEnhance.Brightness(image)
    bright_image = enhancer.enhance(1.5)  # Increase brightness by 50%
    bright_image.save(f"{output_folder}/bright_{os.path.basename(input_image_path)}")
    dark_image = enhancer.enhance(0.5)  # Decrease brightness by 50%
    dark_image.save(f"{output_folder}/dark_{os.path.basename(input_image_path)}")

    # Increase and decrease contrast
    enhancer = ImageEnhance.Contrast(image)
    high_contrast_image = enhancer.enhance(2.0)  # Increase contrast by a factor of 2
    high_contrast_image.save(f"{output_folder}/high_contrast_{os.path.basename(input_image_path)}")
    low_contrast_image = enhancer.enhance(0.5)  # Decrease contrast by a factor of 0.5
    low_contrast_image.save(f"{output_folder}/low_contrast_{os.path.basename(input_image_path)}")

    # Apply edge enhancement filter
    edge_enhanced_image = image.filter(ImageFilter.EDGE_ENHANCE)
    edge_enhanced_image.save(f"{output_folder}/edge_enhanced_{os.path.basename(input_image_path)}")

    # Apply emboss filter
    embossed_image = image.filter(ImageFilter.EMBOSS)
    embossed_image.save(f"{output_folder}/embossed_{os.path.basename(input_image_path)}")

    # Apply blur filter
    blurred_image = image.filter(ImageFilter.BLUR)
    blurred_image.save(f"{output_folder}/blurred_{os.path.basename(input_image_path)}")

    print(f"Color transformations applied and images saved for {os.path.basename(input_image_path)}")

# Define the paths
image_folder = "/home/jasvir/Music/Data4a/"  # Update with your input image folder path
output_folder = "/home/jasvir/Music/Data4a/Transformed_Images"  # Update with your desired output folder

# Ensure the output folder exists
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Process each image in the folder
for file_name in os.listdir(image_folder):
    if file_name.endswith(('.png', '.jpg', '.jpeg')):
        input_image_path = os.path.join(image_folder, file_name)
        apply_color_transformations(input_image_path, output_folder)
