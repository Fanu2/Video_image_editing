import os
from moviepy.editor import ImageClip, concatenate_videoclips
from PIL import Image
import numpy as np


def resize_image(image_path, target_size):
    image = Image.open(image_path)
    # Convert image to RGB if it's not already in RGB mode
    if image.mode != 'RGB':
        image = image.convert('RGB')
    resized_image = image.resize(target_size, Image.LANCZOS)
    return resized_image


def create_slow_slide_show(input_folder, output_video, duration_per_image=5, target_size=(1024, 1024)):
    # Get all image files in the input folder (sorted by filename)
    image_files = sorted([f for f in os.listdir(input_folder) if f.endswith(('.png', '.jpg', '.jpeg'))])

    clips = []
    for file_name in image_files:
        file_path = os.path.join(input_folder, file_name)
        try:
            # Resize image to target size
            resized_image = resize_image(file_path, target_size)

            # Convert PIL image to numpy array
            np_image = np.array(resized_image)

            # Create ImageClip from numpy array
            clip = ImageClip(np_image, duration=duration_per_image)
            clips.append(clip)
        except Exception as e:
            print(f"Failed to process {file_name}: {e}")

    if len(clips) == 0:
        print("No valid images found in the input folder.")
        return

    # Concatenate all clips into a single video clip
    final_clip = concatenate_videoclips(clips)

    # Write the video file
    final_clip.write_videofile(output_video, codec='libx264', fps=24)


# Define paths
input_folder = '/home/jasvir/Music/Jacinta2'
output_video = '/home/jasvir/Music/Jacinta2/output_slow_slide_show.mp4'

# Create the slow slide show with resized images
create_slow_slide_show(input_folder, output_video)
