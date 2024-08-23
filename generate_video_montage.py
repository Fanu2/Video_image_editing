from moviepy.editor import VideoFileClip, clips_array

def generate_video_montage(video_paths, output_path, rows, cols):
    clips = [VideoFileClip(path) for path in video_paths]
    montage = clips_array([clips[i:i+cols] for i in range(0, len(clips), cols)])
    montage.write_videofile(output_path)

# Example usage
generate_video_montage(['video1.mp4', 'video2.mp4', 'video3.mp4', 'video4.mp4'], 'montage.mp4', 2, 2)
