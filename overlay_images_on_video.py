from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip

def overlay_image_on_video(video_path, image_path, output_path):
    video = VideoFileClip(video_path)
    image = ImageClip(image_path).set_duration(video.duration).set_position('center')
    video_with_overlay = CompositeVideoClip([video, image])
    video_with_overlay.write_videofile(output_path)

# Example usage
overlay_image_on_video('input.mp4', 'overlay.png', 'output_overlay.mp4')
