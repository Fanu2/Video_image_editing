from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip

def add_logo(video_path, logo_path, output_path):
    video = VideoFileClip(video_path)
    logo = ImageClip(logo_path).set_duration(video.duration).set_position(('right', 'top')).resize(height=50)
    video_with_logo = CompositeVideoClip([video, logo])
    video_with_logo.write_videofile(output_path)

# Example usage
add_logo('input.mp4', 'logo.png', 'output_with_logo.mp4')
