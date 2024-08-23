from moviepy.editor import VideoFileClip

def resize_video(input_path, output_path, new_size):
    video = VideoFileClip(input_path)
    video_resized = video.resize(new_size)
    video_resized.write_videofile(output_path)

# Example usage
resize_video('input.mp4', 'output_resized.mp4', (640, 480))
