from moviepy.editor import VideoFileClip
from moviepy.video.fx import colorx

def apply_sepia_filter(video_path, output_path, intensity):
    video = VideoFileClip(video_path)
    sepia_video = colorx(video, intensity)
    sepia_video.write_videofile(output_path)

# Example usage
apply_sepia_filter('input.mp4', 'output_sepia.mp4', 1.5)
