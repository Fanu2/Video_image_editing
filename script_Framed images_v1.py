import os
from PIL import Image, ImageOps, ImageDraw


def add_frame(image, frame_type):
    if frame_type == 'simple_border':
        return ImageOps.expand(image, border=30, fill='black')
    elif frame_type == 'rounded_corners':
        radius = 30
        mask = Image.new('L', image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle((0, 0) + image.size, radius, fill=255)
        output = ImageOps.fit(image, mask.size, centering=(0.5, 0.5))
        output.putalpha(mask)
        background = Image.new('RGB', image.size, (255, 255, 255))
        background.paste(output, (0, 0), output)
        return background
    elif frame_type == 'polaroid':
        polaroid = ImageOps.expand(image, border=(30, 30, 30, 90), fill='white')
        draw = ImageDraw.Draw(polaroid)
        draw.rectangle([(10, polaroid.height - 70), (polaroid.width - 10, polaroid.height - 10)], fill='white')
        return polaroid
    elif frame_type == 'shadow_border':
        shadow = ImageOps.expand(image, border=10, fill='gray')
        return ImageOps.expand(shadow, border=20, fill='black')
    else:
        return image


def process_images(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    frame_types = ['simple_border', 'rounded_corners', 'polaroid', 'shadow_border']

    for filename in os.listdir(input_folder):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(input_folder, filename)
            image = Image.open(img_path)

            for frame_type in frame_types:
                framed_image = add_frame(image, frame_type)
                output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_{frame_type}.png")
                framed_image.save(output_path)
                print(f"Saved framed image: {output_path}")


input_folder = '/home/jasvir/Documents/Slide show3/'
output_folder = '/home/jasvir/Documents/Slide show3/framed_images/'

process_images(input_folder, output_folder)
