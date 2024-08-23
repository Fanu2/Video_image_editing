import os
import cv2
import numpy as np
from moviepy.editor import ImageSequenceClip


def resize_and_pad_image(image_path, target_size):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Unable to read image: {image_path}")

    # Resize while maintaining the aspect ratio
    h, w = image.shape[:2]
    target_w, target_h = target_size

    scale = min(target_w / w, target_h / h)
    resized_w = int(w * scale)
    resized_h = int(h * scale)

    resized_image = cv2.resize(image, (resized_w, resized_h), interpolation=cv2.INTER_LANCZOS4)

    # Pad the resized image to fit the target size
    padded_image = cv2.copyMakeBorder(
        resized_image,
        (target_h - resized_h) // 2,
        (target_h - resized_h + 1) // 2,
        (target_w - resized_w) // 2,
        (target_w - resized_w + 1) // 2,
        cv2.BORDER_CONSTANT,
        value=[0, 0, 0]
    )

    return padded_image


def create_movie(image_folder, output_video, duration=60, fps=24):
    # Define target size for all images
    target_size = (1080, 1920)

    # Get a list of all image files in the folder
    image_files = sorted(os.listdir(image_folder))

    # Resize and pad all images to the target size
    images = []
    for file_name in image_files:
        if file_name.endswith(('.png', '.jpg', '.jpeg', '.gif')):
            file_path = os.path.join(image_folder, file_name)
            padded_image = resize_and_pad_image(file_path, target_size)
            images.append(padded_image)

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
