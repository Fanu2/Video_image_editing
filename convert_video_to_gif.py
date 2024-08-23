from moviepy.editor import VideoFileClip

def convert_video_to_gif(video_path, output_path):
    video = VideoFileClip(video_path)
    video = video.subclip(0, 10)  # Convert only the first 10 seconds
    video.write_gif(output_path)

# Example usage
convert_video_to_gif('input.mp4', 'output.gif')
