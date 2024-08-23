def generate_html_with_svg(input_svg_path, output_html_path):
    # Read the SVG content
    with open(input_svg_path, 'r') as file:
        svg_content = file.read()

    # Define the HTML content with animations
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Rotating and Scaling SVG Example</title>
        <style>
            @keyframes rotateElement {{
                0% {{ transform: rotate(0deg); }}
                100% {{ transform: rotate(360deg); }}
            }}

            @keyframes scaleElement {{
                0% {{ transform: scale(1); }}
                50% {{ transform: scale(1.5); }}
                100% {{ transform: scale(1); }}
            }}

            #animatedElement {{
                animation: rotateElement 5s linear infinite, scaleElement 5s ease-in-out infinite;
            }}
        </style>
    </head>
    <body>
        <h1>Rotating and Scaling SVG Example</h1>
        {svg_content}
        <script>
            // Additional interactivity can be added here
        </script>
    </body>
    </html>
    """

    # Write the HTML content to the output file
    with open(output_html_path, 'w') as file:
        file.write(html_content)

    print(f"HTML file with rotating and scaling SVG has been generated: {output_html_path}")


# Example usage
input_svg_path = '/home/jasvir/Music/Jacinta2/image2.svg'
output_html_path = '/home/jasvir/Music/Jacinta2/rotating_scaling_image2.html'

# Replace ID in SVG content with animatedElement for the first element to apply animation
with open(input_svg_path, 'r') as file:
    svg_content = file.read()
svg_content = svg_content.replace('<svg', '<svg id="animatedElement"')
with open(input_svg_path, 'w') as file:
    file.write(svg_content)

generate_html_with_svg(input_svg_path, output_html_path)
