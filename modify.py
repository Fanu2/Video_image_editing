import os
import re

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Regex to find output_folder assignment with hardcoded path
    pattern = r'(output_folder\s*=\s*)([\'"].*?[\'"])'

    if re.search(pattern, content):
        print(f"Modifying {filepath}")

        # Replace hardcoded path with Streamlit text input
        replacement = (
            "import streamlit as st\n\n"
            "output_folder = st.text_input('Select output folder (enter path):', value='output')\n"
            "import os\n"
            "if not os.path.exists(output_folder):\n"
            "    os.makedirs(output_folder)\n"
        )

        # Remove the hardcoded output_folder line
        content = re.sub(pattern, '', content)

        # Prepend the new code at the top
        content = replacement + content

        with open(filepath, 'w') as f:
            f.write(content)

def main():
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".py"):
                process_file(os.path.join(root, file))

if __name__ == "__main__":
    main()
