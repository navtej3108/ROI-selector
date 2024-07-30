import streamlit as st
import cv2
import numpy as np
import pandas as pd
from PIL import Image
import tempfile
import os
from streamlit_drawable_canvas import st_canvas

# Function to save coordinates and names to Excel
def save_coordinates_to_excel(all_coordinates, filename):
    data = {
        'ROI': [],
        'Name': [],
        'Coordinate': [],
        'X': [],
        'Y': []
    }
    for i, (coordinates, name) in enumerate(all_coordinates):
        roi_label = f'ROI {i+1}'
        data['ROI'].extend([roi_label] * 4)
        data['Name'].extend([name] * 4)
        data['Coordinate'].extend(['Top-left', 'Top-right', 'Bottom-left', 'Bottom-right'])
        data['X'].extend([coordinates[0], coordinates[0] + coordinates[2], coordinates[0], coordinates[0] + coordinates[2]])
        data['Y'].extend([coordinates[1], coordinates[1], coordinates[1] + coordinates[3], coordinates[1] + coordinates[3]])

    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)

def main():
    st.title("Image ROI Selector")
    st.write("Upload an image, select ROIs, and save coordinates to an Excel file.")
    
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        img = Image.open(uploaded_file)
        img_array = np.array(img)
        st.image(img, caption='Uploaded Image', use_column_width=True)
        
        # Draw ROI rectangles on image
        st.write("Draw rectangles on the image and enter names for each ROI.")
        drawing_mode = st.sidebar.selectbox(
            "Drawing tool:", ("rect", "freedraw")
        )

        # Specify canvas parameters in application
        canvas_result = st_canvas(
            fill_color="rgba(255, 165, 0, 0.3)",  # Orange color for drawing
            stroke_width=2,
            background_color="#eee",
            background_image=Image.open(uploaded_file) if uploaded_file else None,
            update_streamlit=True,
            height=500,
            drawing_mode=drawing_mode,
            point_display_radius=5,
            key="canvas",
        )

        # Save drawn rectangles
        all_coordinates = []
        if canvas_result.json_data is not None:
            for shape in canvas_result.json_data["objects"]:
                if shape["type"] == "rect":
                    left = shape["left"]
                    top = shape["top"]
                    width = shape["width"]
                    height = shape["height"]
                    name = st.text_input(f"Enter a name for ROI at ({left}, {top})")

                    if name:
                        all_coordinates.append(((left, top, width, height), name))
        
        # Save coordinates to Excel
        if st.button("Save to Excel"):
            excel_filename = "coordinates.xlsx"
            save_coordinates_to_excel(all_coordinates, excel_filename)
            st.success(f"Coordinates saved to {excel_filename}")
            with open(excel_filename, 'rb') as f:
                st.download_button('Download Excel file', f, file_name=excel_filename)

if __name__ == "__main__":
    main()