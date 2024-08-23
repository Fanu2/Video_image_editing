from moviepy.editor import VideoFileClip, clips_array

def create_video_collage(video_paths, output_path, rows, cols):
    clips = [VideoFileClip(path) for path in video_paths]
    collage = clips_array([clips[i:i+cols] for i in range(0, len(clips), cols)])
    collage.write_videofile(output_path)

# Example usage
create_video_collage(['video1.mp4', 'video2.mp4', 'video3.mp4', 'video4.mp4'], 'collage.mp4', 2, 2)
