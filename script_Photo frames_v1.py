import os
from moviepy.editor import VideoClip, ImageClip, concatenate_videoclips
from PIL import Image
import numpy as np


def resize_image(image_path, target_size):
    image = Image.open(image_path)
    if image.mode != 'RGB':
        image = image.convert('RGB')
    resized_image = image.resize(target_size, Image.LANCZOS)
    return resized_image


def apply_effect(image, effect):
    # Apply effects to the image
    if effect == 'original':
        return image
    elif effect == 'sepia':
        return image.sepia()
    elif effect == 'grayscale':
        return image.convert('L').convert('RGB')
    elif effect == 'invert':
        return Image.fromarray(np.invert(np.array(image)))
    elif effect == 'rotate':
        return image.rotate(45)
    elif effect == 'blur':
        return image.filter(ImageFilter.BLUR)
    elif effect == 'sharpen':
        return image.filter(ImageFilter.SHARPEN)
    # Add more effects as needed


def create_video_frame(image_path, effect, duration=5, target_size=(1024, 1024)):
    # Resize image
    resized_image = resize_image(image_path, target_size)

    # Apply effect
    processed_image = apply_effect(resized_image, effect)

    # Convert processed image to numpy array
    np_image = np.array(processed_image)

    # Create ImageClip from numpy array
    clip = ImageClip(np_image, duration=duration)

    return clip


def create_video_from_images(input_folder, output_video, effects=None, duration_per_image=5):
    # Get all image files in the input folder (sorted by filename)
    image_files = sorted([f for f in os.listdir(input_folder) if f.endswith(('.png', '.jpg', '.jpeg'))])

    clips = []
    for i, file_name in enumerate(image_files[:20]):  # Limit to first 20 images
        file_path = os.path.join(input_folder, file_name)
        try:
            # Apply effect
            effect = effects[i % len(effects)] if effects else 'original'

            # Create video frame for the image with effect
            clip = create_video_frame(file_path, effect, duration=duration_per_image)
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
output_video = '/home/jasvir/Music/Jacinta2/output_effects_video.mp4'

# Effects to apply (add more effects as needed)
effects = ['original', 'sepia', 'grayscale', 'invert', 'rotate', 'blur', 'sharpen']

# Create the video with different effects applied to images
create_video_from_images(input_folder, output_video, effects=effects)
