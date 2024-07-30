import streamlit as st
import cv2
import numpy as np
from PIL import Image
import pandas as pd

# Load the image using OpenCV and convert it to RGB format
def load_image(image_path):
    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img_rgb

# Save coordinates and names to an Excel file
def save_to_excel(data, filename='coordinates.xlsx'):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)

def main():
    st.title("ROI Selector")

    # Upload image file
    uploaded_file = st.file_uploader("Choose an image file", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        # Convert the file to an OpenCV image
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, 1)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Display the image with rectangles
        st.image(img_rgb, channels="RGB")

        # Create a list to hold all ROI data
        roi_data = []

        # User input for drawing rectangles
        if 'rects' not in st.session_state:
            st.session_state['rects'] = []

        # Draw rectangles on the image
        col1, col2 = st.columns(2)

        with col1:
            x = st.number_input("X coordinate", min_value=0, max_value=img.shape[1], value=0)
            y = st.number_input("Y coordinate", min_value=0, max_value=img.shape[0], value=0)
            w = st.number_input("Width", min_value=0, max_value=img.shape[1]-x, value=100)
            h = st.number_input("Height", min_value=0, max_value=img.shape[0]-y, value=100)

        with col2:
            roi_name = st.text_input("ROI Name")

            # Button to add the rectangle
            if st.button("Add ROI"):
                st.session_state['rects'].append((x, y, w, h, roi_name))

        # Draw rectangles
        for rect in st.session_state['rects']:
            cv2.rectangle(img_rgb, (int(rect[0]), int(rect[1])), (int(rect[0] + rect[2]), int(rect[1] + rect[3])), (0, 255, 0), 2)
            st.write(f"ROI Name: {rect[4]}, Coordinates: ({rect[0]}, {rect[1]}, {rect[2]}, {rect[3]})")

        # Update image with rectangles
        st.image(img_rgb, channels="RGB")

        # Save ROI data to an Excel file
        if st.button("Save ROIs to Excel"):
            roi_data = [
                {"ROI": f"ROI {i+1}", "Name": rect[4], "X": rect[0], "Y": rect[1], "Width": rect[2], "Height": rect[3]}
                for i, rect in enumerate(st.session_state['rects'])
            ]
            save_to_excel(roi_data)
            st.success("ROI data saved to Excel!")

if __name__ == "__main__":
    main()
