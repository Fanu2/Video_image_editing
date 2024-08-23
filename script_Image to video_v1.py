import os
from moviepy.editor import ImageSequenceClip
from PIL import Image
import numpy as np

def resize_image(image_path, target_size):
    image = Image.open(image_path)
    resized_image = image.resize(target_size, Image.LANCZOS)
    return resized_image.convert('RGB')  # Ensure all images are converted to RGB format

def create_movie_from_images(input_folder, output_video, fps=24, target_size=(1920, 1080)):
    # Get all image files in the input folder (sorted by filename)
    image_files = sorted([f for f in os.listdir(input_folder) if f.endswith('.png')])

    # Get dimensions of the first image
    first_image_path = os.path.join(input_folder, image_files[0])
    first_image = Image.open(first_image_path)
    width, height = first_image.size

    # Resize all images to match dimensions of the first image
    images = []
    for file_name in image_files:
        file_path = os.path.join(input_folder, file_name)
        resized_image = resize_image(file_path, (width, height))
        np_image = np.array(resized_image)
        images.append(np_image)

    # Create a video clip from the images
    if images:
        video_clip = ImageSequenceClip(images, fps=fps)
        video_clip.write_videofile(output_video, codec='libx264')

# Define paths
input_folder = '/home/jasvir/Music/png'
output_video = '/home/jasvir/Music/png/output_video.mp4'

# Create the movie from PNG images
create_movie_from_images(input_folder, output_video)