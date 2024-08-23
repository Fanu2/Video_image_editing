from moviepy.editor import VideoFileClip
from moviepy.video.fx import brightness_contrast

def increase_brightness(input_path, output_path, factor):
    video = VideoFileClip(input_path)
    video_bright = brightness_contrast(video, brightness=factor)
    video_bright.write_videofile(output_path)

# Example usage
increase_brightness('input.mp4', 'output_bright.mp4', 1.5)
