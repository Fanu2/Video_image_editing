import os
import cv2
import numpy as np
from moviepy.editor import ImageSequenceClip, AudioFileClip


def resize_image(image_path, target_size):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Unable to read image: {image_path}")
    resized_image = cv2.resize(image, target_size, interpolation=cv2.INTER_LANCZOS4)
    return resized_image


def create_video_with_music(image_folder, audio_file, output_video, fps=24):
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

    # Create a video clip from the numpy arrays
    video_clip = ImageSequenceClip(images, fps=fps)

    # Load the audio file
    audio_clip = AudioFileClip(audio_file)

    # Set the audio to the video clip
    video_clip = video_clip.set_audio(audio_clip)

    # Write the final video file
    video_clip.write_videofile(output_video, codec='libx264')


# Define the paths
image_folder = "/home/jasvir/Documents/Slide show6/"
audio_file = "/home/jasvir/Documents/Slide show6/trend.mp3"
output_video = "/home/jasvir/Documents/animation_with_music.mp4"

# Call the function
create_video_with_music(image_folder, audio_file, output_video, fps=24)
