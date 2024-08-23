from moviepy.editor import VideoFileClip

def convert_video_to_mp4(input_path, output_path):
    video = VideoFileClip(input_path)
    video.write_videofile(output_path, codec='libx264')

# Example usage
convert_video_to_mp4('input.avi', 'output.mp4')
