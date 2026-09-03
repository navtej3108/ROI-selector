# ROI Selector for Planogram Images

## Project Background

This project was developed during my internship from **June 2024 to August 2024**.

The purpose of the project was to create a simple computer-vision utility for working with **planogram images**. A user can load a planogram picture, select the different shelf/region areas using the mouse, provide a name and code for each selected region, and finally export all the coordinates to an Excel (`.xlsx`) file.

This project gave me practical experience with Python, OpenCV, image processing, ROI selection, data handling, and Excel file generation. It also helped me build the foundation for working on several similar Python and computer-vision projects.

> **Note:** This is an internship-era project developed in 2024 and is being published to document my early practical work and learning journey.

---

## What Is a Planogram?

A **planogram** is a visual representation of how products or shelves are arranged in a store.

For this project, the planogram image is used as the input. The user selects the different shelf/region areas that need to be identified.

For example:

```text
Planogram Image
      │
      ├── Shelf 1
      ├── Shelf 2
      ├── Shelf 3
      └── Shelf 4
```

The application allows each selected area to be associated with a name and code.

---

## What Does This Project Do?

The application follows this workflow:

```text
Planogram Image
       ↓
Load Image
       ↓
Display Image
       ↓
Select a Shelf / Region using Mouse
       ↓
Enter ROI Name
       ↓
Enter ROI Code
       ↓
Crop Selected Region
       ↓
Display Selected Region
       ↓
Select Next Shelf / Region
       ↓
Repeat until finished
       ↓
Export all coordinates to Excel
```

The important point is that the program **does not automatically detect the shelves**.

Instead, the user manually selects each shelf/region using OpenCV's ROI selection tool.

---

## How the Program Works

### 1. Load the Planogram

The program loads the planogram image using OpenCV:

```python
cv2.imread(image_path, cv2.IMREAD_COLOR)
```

The image is loaded into memory as an OpenCV image.

### 2. Display the Image

The planogram is displayed in a resizable/fullscreen OpenCV window.

```python
cv2.imshow()
```

The user can then select a region directly on the image.

### 3. Select a Shelf / ROI

The program uses:

```python
cv2.selectROI()
```

The user draws a rectangle around the shelf or region they want to identify.

OpenCV returns the rectangle as:

```text
(x, y, width, height)
```

Where:

- `x` = X coordinate of the top-left corner
- `y` = Y coordinate of the top-left corner
- `width` = width of the selected region
- `height` = height of the selected region

### 4. Enter Name and Code

After selecting an ROI, the program asks:

```text
Enter a name for ROI 1:
Enter the code for ROI 1:
```

For example:

```text
Name: Shelf 1
Code: S001
```

The coordinates, name, and code are stored for later export.

### 5. Crop the Selected Region

The selected area is cropped from the original planogram:

```python
cropped_image = image[y:y+h, x:x+w]
```

The cropped region is then displayed using Matplotlib.

This allows the user to visually check the selected area.

### 6. Select More Shelves

After one ROI is processed, the program returns to the original planogram and allows another region to be selected.

This continues until the user finishes selecting regions.

The selection process can therefore look like:

```text
ROI 1 → Name + Code
        ↓
ROI 2 → Name + Code
        ↓
ROI 3 → Name + Code
        ↓
ROI 4 → Name + Code
        ↓
Finish
```

### 7. Export to Excel

When the user finishes selecting regions, the program creates an Excel file:

```text
coordinates123.xlsx
```

The program uses Pandas to create the table and `to_excel()` to write the data.

---

## Excel Output

For every selected ROI, the program records four corner coordinates:

- Top-left
- Top-right
- Bottom-left
- Bottom-right

The Excel file contains the following columns:

| Column | Description |
|---|---|
| ROI | ROI number |
| Name | Name provided by the user |
| Code | Code provided by the user |
| Coordinate | Corner of the selected region |
| X | X coordinate |
| Y | Y coordinate |

For example:

```text
ROI     Name       Code    Coordinate       X       Y
ROI 1   Shelf 1    S001    Top-left        120     250
ROI 1   Shelf 1    S001    Top-right       500     250
ROI 1   Shelf 1    S001    Bottom-left     120     400
ROI 1   Shelf 1    S001    Bottom-right    500     400
```

This means each rectangular ROI produces **four rows** in the Excel file.

---

## Technologies Used

- **Python**
- **OpenCV** — image loading, display, ROI selection, and image cropping
- **NumPy** — numerical/image-array operations
- **Pandas** — organizing ROI data and creating the Excel dataset
- **Matplotlib** — displaying the cropped ROI
- **openpyxl** — Excel `.xlsx` file support used by Pandas

---

## Project Structure

```text
ROI-selector/
│
├── main.py
├── requirements.txt
└── README.md
```

### `main.py`

Contains the complete ROI-selection application.

It handles:

- loading the planogram
- displaying the image
- selecting ROIs
- requesting ROI names
- requesting ROI codes
- cropping selected regions
- calculating corner coordinates
- exporting the results to Excel

### `requirements.txt`

Contains the Python packages required to run the project.

### `README.md`

Contains the project documentation and setup instructions.

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/navtej3108/ROI-selector.git
```

Then enter the project directory:

```bash
cd ROI-selector
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install the requirements

```bash
pip install -r requirements.txt
```

---

## Running the Project

The image path is currently specified inside `main.py`:

```python
image_path = '/Users/Kumar/Downloads/53 Kamanahalli Store).jpg'
```

Before running the program, change this path to the location of your planogram image.

Then run:

```bash
python main.py
```

---

## How to Use

### Step 1 — Provide a Planogram Image

Set the `image_path` in `main.py` to your planogram image.

### Step 2 — Run the Program

```bash
python main.py
```

An OpenCV window containing the planogram will appear.

### Step 3 — Select a Shelf

Use the mouse to draw a rectangle around the shelf/region you want to record.

Confirm the selection using the OpenCV ROI-selection interface.

### Step 4 — Enter the Details

The terminal will ask for:

```text
Enter a name for ROI 1:
Enter the code for ROI 1:
```

Enter the appropriate shelf/region information.

### Step 5 — Review the Selected Region

The program crops the selected region and displays it using Matplotlib.

### Step 6 — Continue Selecting

The original planogram is displayed again, allowing you to select another shelf.

Repeat the process for all required shelves.

### Step 7 — Finish

When you finish selecting regions, exit the ROI-selection process by making an empty/invalid selection.

The program then generates:

```text
coordinates123.xlsx
```

---

## Coordinate Calculation

OpenCV provides each ROI as:

```text
(x, y, width, height)
```

The program converts this into four corner coordinates.

```text
Top-left:
(x, y)

Top-right:
(x + width, y)

Bottom-left:
(x, y + height)

Bottom-right:
(x + width, y + height)
```

This makes the output useful for later image-processing tasks where a program needs to know the exact boundaries of each shelf.

---

## Example Workflow

Imagine a planogram containing three shelves:

```text
+--------------------------------------+
|              PLANOGRAM               |
|                                      |
|   +--------------------------+       |
|   |        Shelf 1            |       |
|   +--------------------------+       |
|                                      |
|   +--------------------------+       |
|   |        Shelf 2            |       |
|   +--------------------------+       |
|                                      |
|   +--------------------------+       |
|   |        Shelf 3            |       |
|   +--------------------------+       |
+--------------------------------------+
```

The user selects each shelf and enters:

```text
Shelf 1 → S001
Shelf 2 → S002
Shelf 3 → S003
```

The program then stores the coordinates of all three shelves in the Excel file.

---

## Why This Is Useful

The main purpose of the project is to convert **visual shelf locations in a planogram into structured coordinate data**.

Instead of manually writing down pixel coordinates, the user can select each shelf with the mouse.

The resulting Excel file can then be used by other applications or computer-vision workflows that need to know:

```text
Which shelf?
      +
Where is it located?
      +
What are its coordinates?
```

---

## Learning Outcomes

During this internship project, I gained practical experience with:

- Python programming
- OpenCV
- Image loading and processing
- Interactive ROI selection
- Image cropping
- Coordinate systems
- Working with NumPy arrays
- Pandas DataFrames
- Excel file generation
- Combining multiple Python libraries into one workflow
- Building a practical computer-vision utility

This project helped me understand how image-processing tasks can be converted into structured data and gave me a foundation for working on several similar projects afterward.

---

## Limitations

The current version has a few limitations:

- The image path is currently hard-coded in the Python file.
- ROIs are selected manually.
- Only rectangular ROIs are supported.
- The program does not automatically identify shelves.
- The output filename is currently fixed as `coordinates123.xlsx`.
- The ROI data is not stored in a database.

---

## Future Improvements

Possible improvements include:

- Adding a file picker instead of a hard-coded image path
- Allowing the user to choose the output Excel filename
- Supporting polygonal ROIs
- Adding the ability to edit or delete selected ROIs
- Displaying all selected ROIs on the original planogram
- Automatically detecting shelves
- Adding a graphical user interface
- Supporting multiple planogram images
- Saving ROI configurations for later use

---

## Author

**Navtej Pawan**

BTech Computer Science and Information Technology

**Internship Project — June 2024 to August 2024**

This repository documents an internship-era project that formed part of my early practical experience with Python, computer vision, image processing, and data export workflows.
DME (1).md…]()

