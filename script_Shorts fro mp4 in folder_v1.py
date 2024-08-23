import os
from moviepy.editor import VideoFileClip

# Define the folder containing your MP4 files
input_folder = "/home/jasvir/Pictures/Shorts/"
output_folder = "/home/jasvir/Pictures/Shorts/Processed/"
max_duration = 60  # Maximum duration of YouTube Shorts in seconds

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Process each MP4 file in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith(".mp4"):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, f"short_{filename}")

        # Load the video
        video = VideoFileClip(input_path)

        # Trim the video if it's longer than the maximum duration
        if video.duration > max_duration:
            video = video.subclip(0, max_duration)

        # Save the processed video
        video.write_videofile(output_path, codec='libx264', audio_codec='aac')

        print(f"Processed {filename} into {output_path}")

print("All videos have been processed.")
