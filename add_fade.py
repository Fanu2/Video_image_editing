from moviepy.editor import VideoFileClip
from moviepy.video.fx import fadein, fadeout

def add_fade(video_path, output_path, fade_duration):
    video = VideoFileClip(video_path)
    video_fade = fadein(fadeout(video, fade_duration), fade_duration)
    video_fade.write_videofile(output_path)

# Example usage
add_fade('input.mp4', 'output_fade.mp4', 2)
