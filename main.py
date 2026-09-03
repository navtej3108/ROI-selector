import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def load_image(image_path):
    return cv2.imread(image_path, cv2.IMREAD_COLOR)

def display_image(image, title, fullscreen=False):
    cv2.namedWindow(title, cv2.WINDOW_NORMAL)
    if fullscreen:
        cv2.setWindowProperty(title, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow(title, image)

def crop_image(image, roi):
    x, y, w, h = roi
    cropped_image = image[y:y+h, x:x+w]
    return cropped_image, (x, y, w, h)

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
    image_path = '/Users/Kumar/Downloads/53 Kamanahalli Store).jpg'   # Image Path
    image = load_image(image_path)
    
    all_coordinates = []
    roi_counter = 1

    while True:
        display_image(image, 'Select ROI', fullscreen=True)
        
        roi = cv2.selectROI("Select ROI", image, fromCenter=False, showCrosshair=True)
        cv2.destroyAllWindows()
        
        if roi != (0, 0, 0, 0):  # Check if ROI is valid
            name = input(f"Enter a name for ROI {roi_counter}: ")
            code = input(f"Enter the code for ROI {roi_counter}: ")
            
            # Crop the image and get the coordinates of the ROI
            cropped_image, coordinates = crop_image(image, roi)
            
            # Append the coordinates, name, and code to the list
            all_coordinates.append((coordinates, name, code))
            
            # Display the cropped image
            plt.figure(figsize=(12, 9))
            plt.imshow(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))
            plt.title(f'Cropped Image: {name} ({code})')
            plt.axis('on')  # Show axis to see coordinates
            plt.show()
            
            roi_counter += 1
        else:
            break
    
    # Save the coordinates of all cropped areas to an Excel file with the set_name
    save_coordinates_to_excel(all_coordinates, 'coordinates123.xlsx')    

if __name__ == "__main__":
    main()