from moviepy.editor import VideoFileClip

def extract_subclip(input_path, output_path, start_time, end_time):
    video = VideoFileClip(input_path).subclip(start_time, end_time)
    video.write_videofile(output_path)

# Example usage
extract_subclip('input.mp4', 'output_subclip.mp4', 10, 20)
