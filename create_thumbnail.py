from moviepy.editor import VideoFileClip
from PIL import Image

def create_thumbnail(video_path, output_path, time):
    video = VideoFileClip(video_path)
    frame = video.get_frame(time)
    thumbnail = Image.fromarray(frame)
    thumbnail.save(output_path)

# Example usage
create_thumbnail('input.mp4', 'thumbnail.jpg', 10)
