from moviepy.editor import VideoFileClip, concatenate_videoclips

def merge_videos(video_paths, output_path):
    clips = [VideoFileClip(path) for path in video_paths]
    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile(output_path)

# Example usage
merge_videos(['video1.mp4', 'video2.mp4'], 'output_merged.mp4')
