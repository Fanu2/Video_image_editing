import os
import cv2
import numpy as np
from moviepy.editor import ImageSequenceClip


def resize_image(image_path, target_size):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Unable to read image: {image_path}")
    resized_image = cv2.resize(image, target_size, interpolation=cv2.INTER_LANCZOS4)
    return resized_image


def create_movie(image_folder, output_video, duration=60, fps=24):
    # Define target size for all images
    target_size = (800, 600)

    # Get a list of all image files in the folder
    image_files = sorted(os.listdir(image_folder))

    # Resize all images to the target size
    images = []
    for file_name in image_files:
        if file_name.endswith(('.png', '.jpg', '.jpeg', '.gif')):
            file_path = os.path.join(image_folder, file_name)
            resized_image = resize_image(file_path, target_size)
            images.append(resized_image)

    # Calculate the number of frames needed for the desired duration
    total_frames = int(duration * fps)
    images = images[:total_frames]  # Trim images if more than needed

    # Create a video clip from the numpy arrays
    video_clip = ImageSequenceClip(images, fps=fps)

    # Write the final video file
    video_clip.write_videofile(output_video, codec='libx264')


# Define the paths
image_folder = "/home/jasvir/Music/Data/"
output_video = "/home/jasvir/Music/Data/animation_60_seconds.mp4"

# Call the function to create a 60-second video
create_movie(image_folder, output_video, duration=60, fps=24)
