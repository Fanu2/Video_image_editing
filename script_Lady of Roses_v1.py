import svgwrite

def create_svg(text, filename):
    # Create a new drawing object
    dwg = svgwrite.Drawing(filename, profile='tiny')

    # Add the text to the drawing with specific attributes
    dwg.add(dwg.text(text,
                     insert=(10, 60),
                     font_family='DejaVu Sans',
                     font_size=40,
                     fill='purple',
                     font_weight='bold'))

    # Save the SVG file
    dwg.save()

# Usage
create_svg("Jacinta the lady of Roses", "jacinta_lady_of_roses.svg")
