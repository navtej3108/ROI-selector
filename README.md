# ROI Selector

A Streamlit-based computer vision utility for selecting and labeling multiple **Regions of Interest (ROIs)** on an uploaded image and exporting the selected coordinates to an Excel file.

## Project Background

This project was developed during my internship from **June 2024 to August 2024**.

The purpose of the project was to create a simple tool that makes it easier to mark specific regions of an image and associate each selected region with a **name** and **code**. Working on this project gave me practical experience with Python, OpenCV, Streamlit, image processing, and exporting structured data.

This project also helped me build the foundation for working on other Python and computer-vision projects.

> **Note:** This repository represents an internship-era project from 2024 and is being published to document my practical learning and development work.

## What Is an ROI?

ROI stands for **Region of Interest**.

In computer vision, an ROI is a specific part of an image that we want to focus on instead of processing the entire image.

For example, an image of a factory floor could contain several machines. Instead of analyzing the whole image, we can select individual machine areas as ROIs and give them meaningful names or codes.

## What This Project Does

The application provides a graphical interface where a user can:

1. Upload a PNG, JPG, or JPEG image.
2. View the uploaded image.
3. Draw rectangular ROIs directly on the image.
4. Create multiple ROI selections.
5. Enter a name for each ROI.
6. Enter a code for each ROI.
7. Update the ROI information.
8. Export valid ROI selections to an Excel file.
9. Download the generated Excel file.

The exported Excel file contains the ROI number, name, code, and coordinate information.

## How the Application Works

The overall workflow is:

```text
User uploads image
        ↓
Streamlit receives the image
        ↓
OpenCV decodes the image
        ↓
Image converted from BGR → RGB
        ↓
PIL image created
        ↓
Image displayed on drawable canvas
        ↓
User draws rectangular ROIs
        ↓
ROI coordinates extracted
        ↓
User enters ROI name and code
        ↓
Coordinates + metadata stored
        ↓
Pandas creates a table
        ↓
Excel file generated in memory
        ↓
User downloads ROI-coordinates.xlsx
```

## Main Components

### 1. Image Upload

The application uses Streamlit's file uploader to accept:

- PNG
- JPG
- JPEG

The uploaded file is read into memory and converted into an image using OpenCV.

### 2. Image Processing

OpenCV is used to decode the uploaded image and convert its color representation.

The application performs:

```text
Uploaded file
     ↓
NumPy byte array
     ↓
OpenCV image
     ↓
BGR → RGB
     ↓
PIL Image
```

The PIL image is then used as the background of the drawable canvas.

### 3. ROI Selection

The project uses `streamlit-drawable-canvas` to provide an interactive drawing area.

The drawing mode is configured as:

```text
rect
```

This allows the user to draw rectangular regions over the uploaded image.

For every rectangle, the application obtains:

- X coordinate
- Y coordinate
- Width
- Height

These values represent the selected ROI.

### 4. ROI Metadata

Each ROI can be given:

- **Name** — a human-readable identifier
- **Code** — an associated code or identifier

For example:

```text
ROI 1
Name: Machine A
Code: M001
```

The information is maintained using Streamlit's session state so that it can persist while interacting with the application.

### 5. Coordinate Conversion

The application initially receives each rectangle as:

```text
(x, y, width, height)
```

When generating the Excel file, it also calculates the bottom-right coordinates:

```text
Top-Left X     = x
Top-Left Y     = y
Bottom-Right X = x + width
Bottom-Right Y = y + height
```

This makes the exported data easier to use in other image-processing or computer-vision workflows.

## Excel Output

When the user selects **Save ROIs to Excel**, the application creates an Excel-compatible file in memory.

The output contains:

| Column | Description |
|---|---|
| ROI | ROI number |
| Name | User-defined ROI name |
| Code | User-defined ROI code |
| Top-Left X | X coordinate of the ROI's top-left corner |
| Top-Left Y | Y coordinate of the ROI's top-left corner |
| Bottom-Right X | X coordinate of the ROI's bottom-right corner |
| Bottom-Right Y | Y coordinate of the ROI's bottom-right corner |

The generated file is named:

```text
ROI-coordinates.xlsx
```

The application does not need to save the Excel file permanently on the server before providing it to the user; it creates the file in an in-memory buffer and provides it through Streamlit's download functionality.

## Project Structure

```text
ROI-selector/
│
├── app.py
├── streamlit_app.py
├── requirements.txt
├── packages.txt
└── .devcontainer/
```

### `app.py`

Contains the main ROI-selection application.

It handles:

- image uploading
- image conversion
- interactive rectangle drawing
- ROI name/code input
- coordinate extraction
- Excel generation
- Excel download

### `streamlit_app.py`

Contains a closely related Streamlit implementation of the ROI selector, including image display, drawable ROI selection, ROI metadata, and Excel export.

### `requirements.txt`

Contains the Python packages used by the application, including Streamlit, drawable canvas, OpenCV, Pillow, NumPy, Pandas, and related dependencies.

### `packages.txt`

Contains additional system-level package configuration used by the repository environment.

### `.devcontainer/`

Contains development-container configuration for supported development environments.

## Technologies Used

- **Python**
- **Streamlit**
- **OpenCV**
- **NumPy**
- **Pandas**
- **Pillow**
- **streamlit-drawable-canvas**

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/navtej3108/ROI-selector.git
```

Move into the project directory:

```bash
cd ROI-selector
```

### 2. Create a virtual environment

On Windows:

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

## Running the Application

The main application can be started with:

```bash
streamlit run app.py
```

Streamlit will start a local web application. Open the address shown in the terminal in your browser.

## How to Use

### Step 1 — Upload an Image

Use the **Choose an image file** option and select a PNG, JPG, or JPEG image.

### Step 2 — Select an ROI

Draw a rectangle over the part of the image you want to identify.

You can create multiple rectangular ROIs.

### Step 3 — Add ROI Information

For each ROI, enter:

```text
ROI Name
ROI Code
```

Then select **Update ROI**.

### Step 4 — Export the ROIs

Select:

```text
Save ROIs to Excel
```

The application prepares the selected ROIs and provides a:

```text
Download Excel file
```

button.

The downloaded file contains the ROI coordinates and metadata.

## Example

Suppose an uploaded image contains three areas that need to be identified:

```text
ROI 1 → Machine A → M001
ROI 2 → Machine B → M002
ROI 3 → Entrance  → E001
```

The resulting Excel file can contain:

```text
ROI    Name        Code    Top-Left X    Top-Left Y    Bottom-Right X    Bottom-Right Y
ROI 1  Machine A   M001    ...
ROI 2  Machine B   M002    ...
ROI 3  Entrance    E001    ...
```

This makes the ROI information available in a structured format for later analysis or computer-vision processing.

## Use Cases

The tool can be useful as a preprocessing or annotation utility for projects involving:

- Computer vision
- Image analysis
- Object detection
- Surveillance regions
- Industrial monitoring
- Traffic analysis
- Machine monitoring
- Image-based data collection

The selected coordinates can subsequently be used by another program to process only specific areas of an image.

## Learning Outcomes

During development, I gained practical experience with:

- Building a Python application with Streamlit
- Creating interactive web interfaces
- Uploading and processing images
- OpenCV image decoding and color conversion
- NumPy image arrays
- Interactive ROI selection
- Managing application state with Streamlit
- Extracting geometric coordinates
- Working with Pandas DataFrames
- Generating Excel files programmatically
- Connecting a computer-vision workflow with a user-friendly interface

## Limitations

The current implementation focuses on **rectangular ROIs**.

It does not currently provide specialized tools for:

- Polygonal ROI selection
- Circular ROI selection
- Automatic object detection
- Automatic ROI generation
- Persistent ROI storage in a database

The selected ROI information is exported by the user rather than automatically stored in a database.

## Possible Future Improvements

Possible improvements include:

- Polygon and circle ROI selection
- Editing and deleting individual ROIs
- Saving and loading ROI configurations
- Database support
- Automatic ROI detection
- Image zooming and panning
- ROI validation
- Support for video streams
- Integration with object-detection models
- More detailed annotation formats such as JSON

## Author

**Navtej Pawan**

BTech Computer Science and Information Technology

This repository documents an internship-era project developed during **June 2024 – August 2024** and represents part of my early practical experience with Python, computer vision, and application development.
