from moviepy.editor import VideoFileClip
from PIL import Image

def extract_frames(video_path, output_folder):
    video = VideoFileClip(video_path)
    for i, frame in enumerate(video.iter_frames()):
        frame_image = Image.fromarray(frame)
        frame_image.save(f"{output_folder}/frame_{i:04d}.png")

# Example usage
extract_frames('input.mp4', 'frames')
