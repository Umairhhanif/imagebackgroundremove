import streamlit as st
import sys
import subprocess

# Function to check and install missing packages
def check_install_packages():
    try:
        import rembg
        import PIL
        import onnxruntime
    except ImportError as e:
        st.error(f"Missing required packages. Error: {str(e)}")
        st.info("Installing missing packages...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'rembg', 'Pillow', 'onnxruntime'])
            st.success("Packages installed successfully! Please restart the application.")
            st.stop()
        except Exception as e:
            st.error(f"Error installing packages: {str(e)}")
            st.stop()

# Check packages before importing
check_install_packages()

# Import required packages after checking
from rembg import remove
from PIL import Image
import io
import numpy as np

# Set page title and layout
st.title("Image Background Removing Tool")
st.write("Upload an image to remove its background instantly!")

# File uploader for image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Read the image using PIL
    input_image = Image.open(uploaded_file)
    
    # Display original image
    st.subheader("Original Image")
    st.image(input_image, use_container_width=True)

    # Process the image to remove background
    st.subheader("Processing...")
    with st.spinner("Removing background..."):
        # Convert image to bytes for rembg
        input_bytes = io.BytesIO()
        input_image.save(input_bytes, format="PNG")
        input_bytes = input_bytes.getvalue()

        # Remove background using rembg
        output_bytes = remove(input_bytes)
        output_image = Image.open(io.BytesIO(output_bytes)).convert("RGBA")

    # Display processed image
    st.subheader("Image with Background Removed")
    st.image(output_image, use_container_width=True)

    # Provide download option
    output_buffer = io.BytesIO()
    output_image.save(output_buffer, format="PNG")
    output_buffer.seek(0)
    st.download_button(
        label="Download Image",
        data=output_buffer,
        file_name="background_removed.png",
        mime="image/png"
    )
else:
    st.write("Please upload an image to get started!")

# Sidebar instructions
st.sidebar.header("How to Use")
st.sidebar.write("""
1. Upload a JPG, JPEG, or PNG image.
2. Wait for the background to be removed automatically.
3. Download the processed image with a transparent background!
""")
st.sidebar.write("Note: Works best with clear subject-background contrast.")