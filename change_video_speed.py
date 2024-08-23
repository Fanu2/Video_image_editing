from moviepy.editor import VideoFileClip

def change_speed(input_path, output_path, speed_factor):
    video = VideoFileClip(input_path)
    video_speed = video.fx(lambda clip: clip.speedx(speed_factor))
    video_speed.write_videofile(output_path)

# Example usage
change_speed('input.mp4', 'output_fast.mp4', 2.0)
