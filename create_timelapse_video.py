from moviepy.editor import ImageSequenceClip

def create_timelapse(images_folder, output_path, fps):
    import os
    images = [os.path.join(images_folder, img) for img in sorted(os.listdir(images_folder))]
    clip = ImageSequenceClip(images, fps=fps)
    clip.write_videofile(output_path)

# Example usage
create_timelapse('images/', 'timelapse.mp4', 24)
