from moviepy.editor import VideoFileClip

def convert_frame_rate(input_path, output_path, fps):
    video = VideoFileClip(input_path)
    video_fps = video.set_fps(fps)
    video_fps.write_videofile(output_path)

# Example usage
convert_frame_rate('input.mp4', 'output_fps.mp4', 30)
