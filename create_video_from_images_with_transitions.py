from moviepy.editor import ImageSequenceClip, concatenate_videoclips
from moviepy.video.fx import fadein, fadeout

def create_video_from_images_with_transitions(image_folder, output_path, fps, transition_duration):
    import os
    images = [os.path.join(image_folder, img) for img in sorted(os.listdir(image_folder))]
    clips = [fadein(fadeout(ImageSequenceClip([img], fps=fps), transition_duration), transition_duration) for img in images]
    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile(output_path)

# Example usage
create_video_from_images_with_transitions('images/', 'video_with_transitions.mp4', 1, 2)
