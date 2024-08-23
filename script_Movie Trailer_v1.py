from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip, AudioFileClip
import os

# Path to the directory containing video clips
video_directory = '/home/jasvir/Music/Movie work/Trailer/'
# Path to the directory where the trailer will be saved
output_directory = '/home/jasvir/Music/Movie work/Trailer/'
# Path to the background music file
audio_file_path = '/home/jasvir/Music/Movie work/Trailer/background_music.mp3'

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Load video clips
video_clips = []
for file_name in sorted(os.listdir(video_directory)):
    if file_name.endswith('.mp4'):
        video_file_path = os.path.join(video_directory, file_name)
        video_clips.append(VideoFileClip(video_file_path))

# Concatenate video clips
final_clip = concatenate_videoclips(video_clips)

# Add title text overlay
title = TextClip("Movie Title\nThe Ultimate Trailer", fontsize=70, color='white', bg_color='black', size=final_clip.size)
title = title.set_duration(5).set_position('center')

# Create a composite video with the title overlay
composite = CompositeVideoClip([final_clip, title])

# Load the background music
audio_clip = AudioFileClip(audio_file_path)

# Set audio to the composite video
composite = composite.set_audio(audio_clip)

# Define the output file path
output_file_path = os.path.join(output_directory, 'movie_trailer.mp4')

# Write the result to a file
composite.write_videofile(output_file_path, codec='libx264', audio_codec='aac')

print(f"Movie trailer saved successfully: {output_file_path}")
