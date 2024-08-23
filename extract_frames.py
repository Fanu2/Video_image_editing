from moviepy.editor import VideoFileClip
from PIL import Image

def extract_frames(video_path, output_folder, interval):
    clip = VideoFileClip(video_path)
    for i, frame in enumerate(clip.iter_frames(fps=1/interval)):
        image_path = f'{output_folder}/frame_{i}.png'
        frame_image = Image.fromarray(frame)
        frame_image.save(image_path)

# Example usage
extract_frames('input.mp4', 'frames', 1)
