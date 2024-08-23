import bpy
import os

# Define the path to the folder containing your images
image_folder = "/home/jasvir/Documents/Slide show6/"
image_files = sorted([f for f in os.listdir(image_folder) if f.endswith('.png')])

# Create a new Grease Pencil object
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.gpencil_add(location=(0, 0, 0))
gpencil = bpy.context.object

# Switch to the Draw mode
bpy.context.view_layer.objects.active = gpencil
bpy.ops.object.mode_set(mode='DRAW_GPENCIL')

# Get the Grease Pencil data
gp_data = gpencil.data
gp_layer = gp_data.layers.new(name="Animation Layer", set_active=True)
gp_frame = gp_layer.frames.new(0)

# Define frame duration (you can change this as needed)
frame_duration = 5

# Loop through the images and create keyframes
for idx, image_file in enumerate(image_files):
    image_path = os.path.join(image_folder, image_file)

    # Create a new stroke in the current frame
    stroke = gp_frame.strokes.new()
    stroke.display_mode = '3DSPACE'
    stroke.points.add(4)

    # Set the stroke points
    stroke.points[0].co = (-1, -1, 0)
    stroke.points[1].co = (1, -1, 0)
    stroke.points[2].co = (1, 1, 0)
    stroke.points[3].co = (-1, 1, 0)

    # Set the frame image texture
    image = bpy.data.images.load(image_path)
    gpencil.data.materials.append(bpy.data.materials.new(name="Material"))
    gpencil.data.materials[-1].use_nodes = True
    gpencil.data.materials[-1].node_tree.nodes.new('ShaderNodeTexImage')
    gpencil.data.materials[-1].node_tree.nodes[-1].image = image

    # Set keyframe for the stroke
    gp_frame = gp_layer.frames.new((idx + 1) * frame_duration)

print("Animation created successfully!")
