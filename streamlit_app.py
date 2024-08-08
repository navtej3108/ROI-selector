import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import io
import cv2
from streamlit_drawable_canvas import st_canvas

def save_coordinates_to_excel(all_coordinates):
    data = {
        'ROI': [],
        'Name': [],
        'Code': [],
        'Top-Left X': [],
        'Top-Left Y': [],
        'Bottom-Right X': [],
        'Bottom-Right Y': []
    }
    
    for i, (coordinates, name, code) in enumerate(all_coordinates):
        x, y, w, h = coordinates
        roi_label = f'ROI {i+1}'
        
        data['ROI'].append(roi_label)
        data['Name'].append(name)
        data['Code'].append(code)
        data['Top-Left X'].append(x)
        data['Top-Left Y'].append(y)
        data['Bottom-Right X'].append(x + w)
        data['Bottom-Right Y'].append(y + h)
    
    df = pd.DataFrame(data)
    
    # Save to an in-memory buffer
    buffer = io.BytesIO()
    df.to_excel(buffer, index=False)
    buffer.seek(0)
    
    return buffer

def main():
    st.title("ROI Selector with Drawable Canvas")

    uploaded_file = st.file_uploader("Choose an image file", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        # Read the image
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, 1)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Convert to PIL Image
        img_pil = Image.fromarray(img_rgb)
        
        # Get image dimensions
        img_width, img_height = img_pil.size
        
        st.write("Image loaded successfully.")
        
        # Display the image
        st.image(img_pil, caption='Uploaded Image', use_column_width=True)

        # Create a canvas
        canvas_result = st_canvas(
            fill_color="rgba(255, 0, 0, 0.3)", 
            stroke_width=2,
            stroke_color="#0000FF",
            background_image=img_pil,
            update_streamlit=True,
            height=img_height,
            width=img_width,
            drawing_mode="rect",
            key="canvas"
        )

        if 'rects' not in st.session_state:
            st.session_state['rects'] = []
            st.session_state['roi_names'] = []
            st.session_state['roi_codes'] = []

        if canvas_result.json_data is not None:
            new_rects = []
            for obj in canvas_result.json_data["objects"]:
                if obj["type"] == "rect":
                    left = obj["left"]
                    top = obj["top"]
                    width = obj["width"]
                    height = obj["height"]
                    new_rects.append((left, top, width, height))
            st.session_state['rects'] = new_rects

        if len(st.session_state['rects']) > 0:
            if len(st.session_state['roi_names']) < len(st.session_state['rects']):
                st.session_state['roi_names'].extend([""] * (len(st.session_state['rects']) - len(st.session_state['roi_names'])))
            if len(st.session_state['roi_codes']) < len(st.session_state['rects']):
                st.session_state['roi_codes'].extend([""] * (len(st.session_state['rects']) - len(st.session_state['roi_codes'])))
                
            for i, rect in enumerate(st.session_state['rects']):
                x, y, w, h = rect
                
                with st.form(key=f'roi_form_{i}'):
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        name = st.text_input(f"ROI {i+1} Name", value=st.session_state['roi_names'][i])
                    with col2:
                        code = st.text_input(f"ROI {i+1} Code", value=st.session_state['roi_codes'][i])
                    submit_button = st.form_submit_button("Update ROI")

                    if submit_button:
                        st.session_state['roi_names'][i] = name
                        st.session_state['roi_codes'][i] = code

            if st.button("Save ROIs to Excel"):
                roi_data = [
                    (rect, st.session_state['roi_names'][i], st.session_state['roi_codes'][i])
                    for i, rect in enumerate(st.session_state['rects'])
                    if st.session_state['roi_names'][i] and st.session_state['roi_codes'][i]
                ]
                if roi_data:
                    buffer = save_coordinates_to_excel(roi_data)
                    st.download_button(
                        label="Download Excel file",
                        data=buffer,
                        file_name="ROI-coordinates.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                else:
                    st.warning("No valid ROIs to save.")

if __name__ == "__main__":
    main()
