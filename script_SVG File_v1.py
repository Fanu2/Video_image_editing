from svgwrite import Drawing, rgb

def create_poem_svg(poem_text, output_file):
    # Create SVG drawing
    dwg = Drawing(output_file, profile='tiny')

    # Add poem text
    dwg.add(dwg.text(poem_text,
                     insert=(10, 20),
                     fill=rgb(0, 0, 0),
                     font_size="14px",
                     font_family="Arial"))

    # Save SVG file
    dwg.save()

# Define poem text
poem = """
In Rosa's light, the world does gleam,
A vision fair, a cherished dream.
Her smile, a beacon in the night,
Guides my heart to pure delight.
"""

# Output file path
output_svg = '/home/jasvir/Music/Jacinta2/RomanticPoem.svg'

# Create SVG file with the poem
create_poem_svg(poem, output_svg)

print(f"Poem exported to: {output_svg}")
