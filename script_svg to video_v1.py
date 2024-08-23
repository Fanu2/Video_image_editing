import os
from moviepy.editor import ImageSequenceClip

def create_svg_video(input_folder, output_folder, output_video_name):
    # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # List SVG files in input folder
    svg_files = [f for f in os.listdir(input_folder) if f.endswith('.svg')]
    svg_files.sort()  # Ensure files are in order if necessary

    # Create list of file paths for ImageSequenceClip
    clip_files = [os.path.join(input_folder, svg_file) for svg_file in svg_files]

    # Load SVG files as ImageSequenceClip
    clip = ImageSequenceClip(clip_files, fps=30)  # Adjust fps as needed

    # Set video resolution to HD landscape (1920x1080)
    clip = clip.resize(width=1920, height=1080)

    # Define output video path
    output_video_path = os.path.join(output_folder, output_video_name)

    # Write video file
    clip.write_videofile(output_video_path, codec='libx264', fps=30)  # Adjust codec if needed

# Example usage
input_folder = '/home/jasvir/Documents/Jas/svg/'
output_folder = '/home/jasvir/Documents/Jas/svg_videos/'
output_video_name = 'output_video.mp4'

create_svg_video(input_folder, output_folder, output_video_name)
