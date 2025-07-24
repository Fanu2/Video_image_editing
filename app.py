import streamlit as st
import os
import importlib.util

st.set_page_config(page_title="Run Scripts", layout="centered")
st.title("🧪 Video/Image Editing Script Runner")

# Folder where your scripts are located
SCRIPTS_DIR = "."

# Get list of .py scripts (excluding app.py itself)
scripts = [f for f in os.listdir(SCRIPTS_DIR) if f.endswith(".py") and f != "app.py"]

if not scripts:
    st.warning("No Python scripts found.")
    st.stop()

selected_script = st.selectbox("📜 Select a script to run", scripts)

if st.button("▶️ Run Selected Script"):
    script_path = os.path.join(SCRIPTS_DIR, selected_script)

    spec = importlib.util.spec_from_file_location("module.name", script_path)
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
        st.success(f"✅ `{selected_script}` executed successfully.")
    except Exception as e:
        st.error(f"❌ Error running `{selected_script}`:\n\n{e}")
