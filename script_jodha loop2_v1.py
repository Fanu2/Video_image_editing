from moviepy.editor import ImageSequenceClip
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def add_text_to_image(image_path, text):
    # Open image using PIL
    img = Image.open(image_path)

    # Initialize drawing context
    draw = ImageDraw.Draw(img)

    # Define font and size
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # Adjust the font path as needed
    font = ImageFont.truetype(font_path, size=70)

    # Calculate text size and position
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
    text_x = (img.width - text_width) // 2
    text_y = img.height - text_height - 20  # Adjust vertical position

    # Add text to image
    draw.text((text_x, text_y), text, font=font, fill='white')

    # Convert PIL image to numpy array
    img_array = np.array(img)

    return img_array

def resize_image(img_array, target_size=(1920, 1080)):
    # Resize image to target size
    img_resized = Image.fromarray(img_array).resize(target_size)
    return np.array(img_resized)

def create_animation(input_folder, output_video):
    # Get list of image files in input_folder
    file_list = sorted(os.listdir(input_folder))

    # Initialize an array to store video clips
    clips = []

    # Load each image and add TextClip
    for filename in file_list:
        if filename.endswith(".jpg") or filename.endswith(".png"):  # Adjust based on your image format
            image_path = os.path.join(input_folder, filename)
            img_with_text = add_text_to_image(image_path, "Love u Jodha")
            img_resized = resize_image(img_with_text)  # Resize image
            clips.append(img_resized)

    # Create a video clip from the images
    video_clip = ImageSequenceClip(clips, fps=24)

    # Calculate duration based on number of frames (each frame contributes 1/24 second)
    duration = len(clips) / 24  # Assuming 24 frames per second

    # Set the duration of the video clip explicitly
    video_clip = video_clip.set_duration(duration)

    # Loop the video clip
    looped_clip = video_clip.loop()

    # Write the video to a file
    looped_clip.write_videofile(output_video, codec='libx264', fps=24, threads=4)

    print(f"Animation saved as {output_video}")

# Example usage
input_folder = "/home/jasvir/Documents/Princess Jodha/Jodha9/"
output_video = "/home/jasvir/Documents/Princess Jodha/Jodha9/video.mp4"
create_animation(input_folder, output_video)
