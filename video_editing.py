from moviepy.editor import VideoFileClip

def trim_video(input_path, output_path, start_time, end_time):
    clip = VideoFileClip(input_path).subclip(start_time, end_time)
    clip.write_videofile(output_path)

# Example usage
trim_video('input.mp4', 'output_trimmed.mp4', 10, 20)
