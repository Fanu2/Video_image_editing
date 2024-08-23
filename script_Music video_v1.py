import os
import subprocess

# Define paths
image_folder = '/home/jasvir/Documents/Today/'
output_video = '/home/jasvir/Documents/Today/movie.mp4'
final_output_video = '/home/jasvir/Documents/Today/movie_with_music.mp4'
background_music = '/home/jasvir/Documents/Today/abc.mp3'

# Check if the image folder exists
if not os.path.exists(image_folder):
    print(f"Image folder {image_folder} does not exist.")
    exit(1)

# List all jpg images in the folder
images = sorted([img for img in os.listdir(image_folder) if img.endswith('.jpg')])

# Ensure there are images to create a video
if not images:
    print("No jpg images found in the specified folder.")
    exit(1)

# Ensure images are named sequentially
for i, img in enumerate(images):
    os.rename(os.path.join(image_folder, img), os.path.join(image_folder, f"{i + 1}.jpg"))

# Calculate frame rate based on the total number of images
num_images = len(images)
duration_per_image = 5  # Adjust as needed, in seconds
total_duration = num_images * duration_per_image
frame_rate = num_images / total_duration

# Step 1: Create video from images using ffmpeg command
ffmpeg_cmd = (
    f"ffmpeg -y -framerate {frame_rate} -pattern_type glob -i '{image_folder}/*.jpg' "
    f"-c:v libx264 -pix_fmt yuv420p {output_video}"
)
subprocess.run(ffmpeg_cmd, shell=True, check=True)

# Step 2: Convert background music to match video duration
ffmpeg_cmd = (
    f"ffmpeg -y -i {background_music} -t {total_duration} "
    f"-acodec copy {os.path.join(image_folder, 'background_music.mp3')}"
)
subprocess.run(ffmpeg_cmd, shell=True, check=True)

# Step 3: Combine video with background music
ffmpeg_cmd = (
    f"ffmpeg -y -i {output_video} -i {os.path.join(image_folder, 'background_music.mp3')} "
    f"-c:v copy -c:a aac -strict experimental {final_output_video}"
)
subprocess.run(ffmpeg_cmd, shell=True, check=True)

# Clean up temporary files
os.remove(output_video)
os.remove(os.path.join(image_folder, 'background_music.mp3'))

print("Movie created successfully with background music!")
