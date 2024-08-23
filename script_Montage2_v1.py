from PIL import Image
import os
import subprocess


def resize_images(input_dir, output_dir, size=(800, 800)):
    """
    Resize images in the input directory and save them to the output directory.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    files_resized = 0
    for file_name in os.listdir(input_dir):
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            with Image.open(os.path.join(input_dir, file_name)) as img:
                img = img.resize(size, Image.ANTIALIAS)
                img.save(os.path.join(output_dir, file_name))
                files_resized += 1

    if files_resized == 0:
        print(f"No images found in {input_dir}.")
        exit(1)

    print(f"Resizing complete. {files_resized} files saved to {output_dir}.")


def create_montage(input_dir, output_file, tile='x1', frame=10, geometry='+5+5'):
    """
    Create a montage of images from the input directory and save it to the output file.
    """
    command = [
        'montage',
        os.path.join(input_dir, '*.png'),
        os.path.join(input_dir, '*.jpg'),
        '-tile', tile,
        '-frame', str(frame),
        '-geometry', geometry,
        output_file
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Montage created successfully and saved to {output_file}.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while creating the montage: {e}")
        exit(1)


def main():
    input_dir = '/home/jasvir/Documents/Jass/'
    resized_dir = '/home/jasvir/Documents/Jass/resized/'
    output_file = '/home/jasvir/Documents/Jass/frame_with_border.jpg'

    print("Starting image resizing...")
    resize_images(input_dir, resized_dir)

    print("Creating image montage...")
    create_montage(resized_dir, output_file)


if __name__ == "__main__":
    main()
