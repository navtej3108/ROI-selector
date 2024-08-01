import streamlit as st
import cv2
import numpy as np
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt

# Function to load the image using PIL and convert it to RGB format
def load_image(image_file):
    img = Image.open(image_file)
    img = np.array(img)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img_rgb

# Function to crop the image based on ROI
def crop_image(image, roi):
    x, y, w, h = roi
    cropped_image = image[y:y+h, x:x+w]
    return cropped_image

# Function to save coordinates and names to an Excel file
def save_coordinates_to_excel(all_coordinates, filename):
    data = {
        'ROI': [],
        'Name': [],
        'Code': [],
        'Coordinate': [],
        'X': [],
        'Y': []
    }
    for i, (coordinates, name, code) in enumerate(all_coordinates):
        roi_label = f'ROI {i+1}'
        data['ROI'].extend([roi_label] * 4)
        data['Name'].extend([name] * 4)
        data['Code'].extend([code] * 4)
        data['Coordinate'].extend(['Top-left', 'Top-right', 'Bottom-left', 'Bottom-right'])
        data['X'].extend([coordinates[0], coordinates[0] + coordinates[2], coordinates[0], coordinates[0] + coordinates[2]])
        data['Y'].extend([coordinates[1], coordinates[1], coordinates[1] + coordinates[3], coordinates[1] + coordinates[3]])
    
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)

def main():
    st.title("ROI Selector")

    # Upload image file
    uploaded_file = st.file_uploader("Choose an image file", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        # Load and display the image
        img_rgb = load_image(uploaded_file)
        st.image(img_rgb, channels="RGB", caption="Uploaded Image")

        # Initialize variables
        if 'rects' not in st.session_state:
            st.session_state['rects'] = []
        
        # ROI Selection
        st.write("Enter the coordinates and details for ROIs.")

        # User input for drawing rectangles
        with st.form(key='roi_form'):
            x = st.number_input("X coordinate", min_value=0, max_value=img_rgb.shape[1], value=0)
            y = st.number_input("Y coordinate", min_value=0, max_value=img_rgb.shape[0], value=0)
            w = st.number_input("Width", min_value=0, max_value=img_rgb.shape[1] - x, value=100)
            h = st.number_input("Height", min_value=0, max_value=img_rgb.shape[0] - y, value=100)
            roi_name = st.text_input("ROI Name")
            roi_code = st.text_input("ROI Code")

            # Submit button for adding the ROI
            if st.form_submit_button("Add ROI"):
                st.session_state['rects'].append((x, y, w, h, roi_name, roi_code))

        # Draw rectangles on the image
        img_with_rects = img_rgb.copy()
        for rect in st.session_state['rects']:
            cv2.rectangle(img_with_rects, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 255, 0), 2)
            st.write(f"ROI Name: {rect[4]}, Code: {rect[5]}, Coordinates: ({rect[0]}, {rect[1]}, {rect[2]}, {rect[3]})")

        # Display image with drawn rectangles
        st.image(img_with_rects, channels="RGB", caption="Image with ROIs")

        # Save ROI data to Excel
        if st.button("Save ROIs to Excel"):
            roi_data = [
                {"ROI": f"ROI {i+1}", "Name": rect[4], "Code": rect[5], "X": rect[0], "Y": rect[1], "Width": rect[2], "Height": rect[3]}
                for i, rect in enumerate(st.session_state['rects'])
            ]
            save_coordinates_to_excel(roi_data, 'ROI-coordinates.xlsx')
            st.success("ROI data saved to Excel!")

if __name__ == "__main__":
    main()
