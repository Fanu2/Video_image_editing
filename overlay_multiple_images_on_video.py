from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip

def overlay_images_on_video(video_path, image_paths, output_path):
    video = VideoFileClip(video_path)
    images = [ImageClip(image).set_duration(video.duration).set_position('center').resize(video.size) for image in image_paths]
    video_with_images = CompositeVideoClip([video] + images)
    video_with_images.write_videofile(output_path)

# Example usage
overlay_images_on_video('input.mp4', ['image1.png', 'image2.png'], 'output_with_images.mp4')
