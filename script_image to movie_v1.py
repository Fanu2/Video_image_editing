import os
from moviepy.editor import ImageSequenceClip
from PIL import Image
import numpy as np


def resize_and_pad_image(image_path, target_size):
    image = Image.open(image_path)
    image.thumbnail(target_size, Image.LANCZOS)
    background = Image.new('RGB', target_size, (0, 0, 0))  # Black background
    offset = ((target_size[0] - image.width) // 2, (target_size[1] - image.height) // 2)
    background.paste(image, offset)
    return background


def create_movie_from_images(input_folder, output_video, fps=30, target_size=(1920, 1080), duration=60):
    # Get all image files in the input folder (sorted by filename)
    image_files = sorted([f for f in os.listdir(input_folder) if f.endswith(('.png', '.jpg', '.jpeg'))])

    images = []
    for file_name in image_files:
        file_path = os.path.join(input_folder, file_name)
        try:
            resized_image = resize_and_pad_image(file_path, target_size)
            # Convert PIL image to numpy array
            np_image = np.array(resized_image)
            images.append(np_image)
        except Exception as e:
            print(f"Failed to process {file_name}: {e}")

    if len(images) == 0:
        print("No valid images found in the input folder.")
        return

    # Each image duration is equal to the total duration divided by the number of images
    image_duration = duration / len(images)

    # Create the video clip
    video_clip = ImageSequenceClip(images, fps=fps)

    # Set the duration for each image
    video_clip = video_clip.set_duration(image_duration)

    video_clip.write_videofile(output_video, fps=fps, codec='libx264')


# Define paths
input_folder = '/home/jasvir/Music/Jacinta2'
output_video = '/home/jasvir/Music/Jacinta2/output_movie.mp4'

# Create the movie from images
create_movie_from_images(input_folder, output_video)
