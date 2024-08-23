from moviepy.editor import VideoFileClip

def convert_video_format(input_path, output_path):
    clip = VideoFileClip(input_path)
    clip.write_videofile(output_path, codec='libx264')

# Example usage
convert_video_format('input.avi', 'output.mp4')
