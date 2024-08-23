import os
from moviepy.editor import VideoFileClip, concatenate_videoclips

def concatenate_videos(input_folder, output_video):
    # Get all video files in the input folder (sorted by filename)
    video_files = sorted([f for f in os.listdir(input_folder) if f.endswith('.mp4')])

    clips = []
    for file_name in video_files:
        file_path = os.path.join(input_folder, file_name)
        try:
            # Load video file as VideoFileClip
            clip = VideoFileClip(file_path)
            clips.append(clip)
        except Exception as e:
            print(f"Failed to process {file_name}: {e}")

    if len(clips) == 0:
        print("No valid video files found in the input folder.")
        return

    # Concatenate all clips into a single video clip
    final_clip = concatenate_videoclips(clips)

    # Write the concatenated video file
    final_clip.write_videofile(output_video, codec='libx264', fps=24)

# Define paths
input_folder = '/home/jasvir/Music/Jodha1'
output_video = '/home/jasvir/Music/Jodha1/concatenated_video.mp4'

# Concatenate videos in the input folder
concatenate_videos(input_folder, output_video)
