import os
import subprocess

# Path to your virtual environment
venv_path = "/home/jasvir/PycharmProjects/VideoImageProcessing/venv"

# Check if requirements.txt exists
requirements_file = os.path.join(os.path.dirname(__file__), 'requirements.txt')
if os.path.exists(requirements_file):
    # Install dependencies from requirements.txt
    subprocess.check_call([os.path.join(venv_path, 'bin', 'pip'), 'install', '-r', 'requirements.txt'])
else:
    print("requirements.txt file not found. Skipping dependency installation.")

# Your existing script continues here...

from moviepy.editor import ImageClip, CompositeVideoClip
from PIL import Image
import numpy as np

# Path to the image directory
image_dir = "/home/jasvir/Pictures/Jodha/"
output_path = os.path.join(image_dir, "rotating_central_image.mp4")

# Load the central image (1.png)
central_image_path = os.path.join(image_dir, "1.png")
central_image = Image.open(central_image_path)
central_image_size = central_image.size

# Load the rotating images (2.png to 7.png)
rotating_images_paths = [os.path.join(image_dir, f"{i}.png") for i in range(2, 8)]
rotating_images = [Image.open(img_path) for img_path in rotating_images_paths]

# Create a video clip for the central image
central_clip = ImageClip(central_image_path).set_duration(10)  # 10 seconds duration
clips = [central_clip.set_pos('center')]

# Parameters for rotation
num_images = len(rotating_images)
radius = 300  # Radius of the circular path
angle_increment = 360 / num_images
frame_rate = 24  # Frame rate of the video
duration = 10  # Duration of the video in seconds
num_frames = duration * frame_rate

# Create video clips for rotating images
for i, img in enumerate(rotating_images):
    img_clip = ImageClip(rotating_images_paths[i]).set_duration(duration)
    frames = []

    for t in range(num_frames):
        angle = (t * 360 / num_frames + i * angle_increment) % 360
        radians = np.deg2rad(angle)
        x = central_image_size[0] / 2 + radius * np.cos(radians) - img.width / 2
        y = central_image_size[1] / 2 + radius * np.sin(radians) - img.height / 2
        frames.append(img_clip.set_position((x, y)).get_frame(t / frame_rate))

    img_clip = ImageClip(np.array(frames)).set_duration(duration)
    clips.append(img_clip)

# Composite the video clips
final_clip = CompositeVideoClip(clips, size=central_image_size).set_duration(duration)
final_clip.write_videofile(output_path, fps=frame_rate)

print("Video created successfully!")
