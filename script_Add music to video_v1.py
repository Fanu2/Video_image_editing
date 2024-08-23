import os
import subprocess

# Define paths
video_file = "/media/jasvir/My Passport/media/mp4/20221009_163800.mp4"
music_file = "/media/jasvir/My Passport/media/m4a/Dhool Sammi-Aashiq jatt-VOL-1-EMI-OLD STUDIO PK.m4a"
output_folder = "/home/jasvir/Documents/Output/"
output_file = os.path.join(output_folder, "output_video.mp4")

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# ffmpeg command to add music to the video
ffmpeg_cmd = (
    f"ffmpeg -i {video_file} -i {music_file} "
    "-c:v copy -c:a aac -strict experimental "
    f"{output_file}"
)

# Run ffmpeg command
try:
    subprocess.run(ffmpeg_cmd, shell=True, check=True)
    print(f"Video with music added successfully at: {output_file}")
except subprocess.CalledProcessError as e:
    print(f"Error: {e}")
