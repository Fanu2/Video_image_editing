import os
from moviepy.editor import ImageSequenceClip, concatenate_videoclips, AudioFileClip

def create_movie_from_images(image_folder, audio_file, output_video, duration=60):
    # Get all image files in the folder
    image_files = sorted([os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))])

    # Calculate duration for each image based on total duration and number of images
    num_images = len(image_files)
    image_duration = duration / num_images

    # Create clips from images with calculated duration
    clips = [ImageSequenceClip([image], fps=24).set_duration(image_duration) for image in image_files]

    # Concatenate all image clips into a single video clip
    final_clip = concatenate_videoclips(clips)

    # Add background music
    if audio_file:
        audio_clip = AudioFileClip(audio_file)
        audio_clip = audio_clip.volumex(0.5)  # Adjust volume if needed
        final_clip = final_clip.set_audio(audio_clip)

    # Write the final video file
    final_clip.write_videofile(output_video, codec='libx264', fps=24)

# Define paths
image_folder = "/home/jasvir/Documents/Slide show6/"
audio_file = "/home/jasvir/Documents/Slide show6/trend.mp3"
output_video = "/home/jasvir/Documents/movie_from_images_60s.mp4"

# Create the 60-second movie from images with effects and music
create_movie_from_images(image_folder, audio_file, output_video, duration=60)
