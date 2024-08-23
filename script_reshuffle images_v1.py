import os
import random
import shutil


def reshuffle_images(directory):
    # Get a list of all files in the directory
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    # Shuffle the list of files
    random.shuffle(files)

    # Create a temporary directory to hold shuffled files
    temp_dir = os.path.join(directory, 'temp')
    os.makedirs(temp_dir, exist_ok=True)

    # Rename files in the shuffled order and move them to the temporary directory
    for idx, filename in enumerate(files):
        src_path = os.path.join(directory, filename)
        dst_path = os.path.join(temp_dir, f"img_{idx:04d}{os.path.splitext(filename)[1]}")
        shutil.move(src_path, dst_path)

    # Move the shuffled files back to the original directory
    for filename in os.listdir(temp_dir):
        src_path = os.path.join(temp_dir, filename)
        dst_path = os.path.join(directory, filename)
        shutil.move(src_path, dst_path)

    # Remove the temporary directory
    os.rmdir(temp_dir)


directory = '/home/jasvir/Documents/Slide show3/framed_images/'
reshuffle_images(directory)
