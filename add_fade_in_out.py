from moviepy.editor import VideoFileClip
from moviepy.video.fx import fadein, fadeout

def add_fade_in_out(video_path, output_path, fade_duration):
    video = VideoFileClip(video_path)
    video_with_fades = fadein(fadeout(video, fade_duration), fade_duration)
    video_with_fades.write_videofile(output_path)

# Example usage
add_fade_in_out('input.mp4', 'output_fade_in_out.mp4', 3)
