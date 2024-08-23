from moviepy.editor import VideoFileClip

def adjust_volume(video_path, output_path, volume_factor):
    video = VideoFileClip(video_path)
    video_with_volume = video.volumex(volume_factor)
    video_with_volume.write_videofile(output_path)

# Example usage
adjust_volume('input.mp4', 'output_louder.mp4', 2.0)
