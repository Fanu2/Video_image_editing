from moviepy.editor import ImageSequenceClip

def create_slideshow(image_folder, output_path, fps):
    import os
    images = [os.path.join(image_folder, img) for img in sorted(os.listdir(image_folder))]
    clip = ImageSequenceClip(images, fps=fps)
    clip.write_videofile(output_path)

# Example usage
create_slideshow('images/', 'slideshow.mp4', 1)
