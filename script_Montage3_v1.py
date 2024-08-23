import os
import glob
import subprocess
from PIL import Image

def resize_images(input_dir, output_dir, size=(800, 800)):
    """
    Resize all images in the input directory and save them to the output directory.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Get list of all image files in the input directory
    image_files = glob.glob(os.path.join(input_dir, '*.[pj]*[np]*[g]*'))  # Matches png and jpg

    if not image_files:
        print(f"No image files found in {input_dir}.")
        return

    print("Starting image resizing...")
    for img_file in image_files:
        with Image.open(img_file) as img:
            img = img.resize(size, Image.Resampling.LANCZOS)
            file_name = os.path.basename(img_file)
            img.save(os.path.join(output_dir, file_name))

    print(f"Resizing complete. {len(image_files)} files saved to {output_dir}.")

def create_montage(input_dir, output_file, tile='x1', frame=10, geometry='+5+5'):
    """
    Create a montage of images from the input directory and save it to the output file.
    """
    # List all image files in the input directory
    image_files = glob.glob(os.path.join(input_dir, '*.[pj]*[np]*[g]*'))  # Matches png and jpg

    if not image_files:
        print(f"No images found in {input_dir}.")
        return

    # Create the montage command
    command = [
        'montage',
        *image_files,
        '-tile', tile,
        '-frame', str(frame),
        '-geometry', geometry,
        '-limit', 'memory', '4GiB',  # Increased memory limit
        '-limit', 'map', '4GiB',     # Increased map limit
        output_file
    ]

    print(f"Executing command: {' '.join(command)}")  # Print the command for debugging

    try:
        subprocess.run(command, check=True)
        print(f"Montage created successfully and saved to {output_file}.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while creating the montage: {e}")
        exit(1)

def main():
    # Directories
    original_dir = '/home/jasvir/Documents/Jass/'
    resized_dir = '/home/jasvir/Documents/Jass/resized/'
    montage_file = '/home/jasvir/Documents/Jass/frame_with_border.jpg'

    # Resize images
    resize_images(original_dir, resized_dir)

    # Create montage
    create_montage(resized_dir, montage_file)

if __name__ == "__main__":
    main()
