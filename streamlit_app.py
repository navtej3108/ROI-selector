import streamlit as st
import cv2
import numpy as np
import pandas as pd
from PIL import Image
from streamlit_drawable_canvas import st_canvas

# Function to save coordinates and names to an Excel file
def save_to_excel(data, filename='coordinates.xlsx'):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)

def main():
    st.title("ROI Selector")

    # Upload image file
    uploaded_file = st.file_uploader("Choose an image file", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        # Convert the uploaded file to an OpenCV image
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, 1)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Display the image with rectangles
        st.image(img_rgb, channels="RGB")

        # Initialize session state for storing rectangles
        if 'rects' not in st.session_state:
            st.session_state['rects'] = []

        # Create a canvas for drawing rectangles
        st.write("Draw rectangles on the image to select ROIs.")
        canvas_result = st_canvas(
            fill_color="rgba(255, 0, 0, 0.3)",  # Color for rectangles
            stroke_width=2,
            stroke_color="#0000FF",
            background_image=Image.fromarray(img_rgb),
            update_streamlit=True,
            height=img_rgb.shape[0],
            width=img_rgb.shape[1],
            drawing_mode="rect",
            key="canvas"
        )

        # Capture drawn rectangles from canvas
        if canvas_result.json_data is not None:
            for obj in canvas_result.json_data["objects"]:
                if obj["type"] == "rect":
                    left = obj["left"]
                    top = obj["top"]
                    width = obj["width"]
                    height = obj["height"]
                    roi = (left, top, width, height)
                    if roi not in st.session_state['rects']:
                        st.session_state['rects'].append(roi)

        # Display the coordinates of the drawn rectangles
        for rect in st.session_state['rects']:
            st.write(f"Coordinates: ({rect[0]}, {rect[1]}, {rect[2]}, {rect[3]})")

        # Save ROI data to an Excel file
        if st.button("Save ROIs to Excel"):
            roi_data = [
                {"ROI": f"ROI {i+1}", "X": rect[0], "Y": rect[1], "Width": rect[2], "Height": rect[3]}
                for i, rect in enumerate(st.session_state['rects'])
            ]
            save_to_excel(roi_data)
            st.success("ROI data saved to Excel!")

if __name__ == "__main__":
    main()
