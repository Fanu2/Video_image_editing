from moviepy.editor import VideoFileClip

def resize_video(input_path, output_path, size):
    video = VideoFileClip(input_path)
    resized_video = video.resize(size)
    resized_video.write_videofile(output_path)

# Example usage
resize_video('input.mp4', 'output_resized.mp4', (640, 480))