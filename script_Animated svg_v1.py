# Required Libraries
import os

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
        <title>Animated SVG Example</title>
        <style>
            /* Example CSS animations */
            @keyframes moveElement {{
                0% {{ transform: translate(0, 0); }}
                50% {{ transform: translate(100px, 0); }}
                100% {{ transform: translate(0, 0); }}
            }}

            @keyframes changeColor {{
                0% {{ fill: blue; }}
                50% {{ fill: red; }}
                100% {{ fill: blue; }}
            }}

            /* Apply animations to the SVG elements */
            #animatedElement {{
                animation: moveElement 5s infinite, changeColor 5s infinite;
            }}
        </style>
    </head>
    <body>
        <h1>Animated SVG Example</h1>
        {svg_content}
        <script>
            // Example JavaScript animations
            document.getElementById('animatedElement').addEventListener('click', function() {{
                this.setAttribute('r', Math.random() * 50);
            }});
        </script>
    </body>
    </html>
    """

    # Write the HTML content to the output file
    with open(output_html_path, 'w') as file:
        file.write(html_content)

    print(f"HTML file with animated SVG has been generated: {output_html_path}")

# Example usage
input_svg_path = '/home/jasvir/Music/Jacinta2/image2.svg'
output_html_path = '/home/jasvir/Music/Jacinta2/animated_image2.html'

# Replace ID in SVG content with animatedElement for the first element to apply animation
with open(input_svg_path, 'r') as file:
    svg_content = file.read()
svg_content = svg_content.replace('<svg', '<svg id="animatedElement"')
with open(input_svg_path, 'w') as file:
    file.write(svg_content)

generate_html_with_svg(input_svg_path, output_html_path)
