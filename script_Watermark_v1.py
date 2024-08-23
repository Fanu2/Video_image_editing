from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip

def add_watermark(video_path, watermark_path, output_path):
    # Load the video
    video = VideoFileClip(video_path)

    # Load the watermark image
    watermark = ImageClip(watermark_path).set_duration(video.duration)

    # Position the watermark at the bottom-right corner with a margin
    watermark = watermark.set_position(("right", "bottom")).resize(height=50)

    # Composite the video with the watermark
    final_video = CompositeVideoClip([video, watermark])

    # Write the output video file
    final_video.write_videofile(output_path, codec="libx264")

# Usage
video_path = "/home/jasvir/Pictures/pic1/Because yoou loved me.mp4"
watermark_path = "/home/jasvir/Pictures/pic1/playful_energetic_logo.png"
output_path = "/home/jasvir/Pictures/pic1/Because_you_loved_me_watermarked.mp4"

add_watermark(video_path, watermark_path, output_path)
