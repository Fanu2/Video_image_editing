from moviepy.editor import VideoFileClip

def video_to_gif(input_path, output_path):
    clip = VideoFileClip(input_path)
    clip.write_gif(output_path)

# Example usage
video_to_gif('input.mp4', 'output.gif')
