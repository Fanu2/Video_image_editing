import subprocess
import os


def create_composite_image(input_dir, output_path, tile_layout="2x2", geometry="+2+2"):
    """
    Create a composite image by combining several separate images.

    :param input_dir: Directory containing the input images.
    :param output_path: Path to save the composite image.
    :param tile_layout: Layout for tiling the images (default is 2x2).
    :param geometry: Space between images (default is +2+2).
    """
    # Get all image files from the directory
    image_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]

    if not image_files:
        raise ValueError("No images found in the specified directory.")

    command = ["montage"] + image_files + ["-tile", tile_layout, "-geometry", geometry, output_path]
    subprocess.run(command)


# Example usage
input_directory = "/home/jasvir/Documents/Jass/"
output_image = os.path.join(input_directory, "composite_image.jpg")
create_composite_image(input_directory, output_image)
