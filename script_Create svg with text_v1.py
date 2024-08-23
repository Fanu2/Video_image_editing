import svgwrite

def create_svg_with_text(output_file, text, font_family="Arial", font_size=40, text_color="black"):
    # Create a new SVG drawing
    dwg = svgwrite.Drawing(filename=output_file, size=("300px", "100px"))

    # Define a text style
    style = f"font-family: {font_family}; font-size: {font_size}px; fill: {text_color};"

    # Add text to the SVG drawing
    dwg.add(dwg.text(text, insert=(20, 50), style=style))

    # Save the SVG file
    dwg.save()

# Example usage
output_file = "love_u_jodha.svg"
text = "Love u Jodha"
create_svg_with_text(output_file, text)
print(f"SVG image '{output_file}' created successfully.")
