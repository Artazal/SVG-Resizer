# SVG Resizer

Simple desktop tool to resize SVG files to a target width while preserving aspect ratio.

## Features

- Resize one or multiple SVG files at once  
- Drag & drop support  
- Automatic aspect ratio calculation  
- Input validation (min/max width)  
- Error handling with user-friendly messages  
- Saves resized files next to originals  

## How it works

1. Add SVG files (button or drag & drop)  
2. Enter target width in pixels  
3. Click Resize  
4. Resized files will be saved next to the originals  

## Tech Stack

- Python  
- Tkinter (GUI)  
- tkinterdnd2 (drag & drop)  
- xml.etree.ElementTree (SVG parsing)

## Limitations

- SVG files must contain a viewBox attribute  
- Very large sizes (>50000 px) are restricted  

## Example

Input:  
logo.svg

Output:  
logo_7000.svg

## Screenshot

<img width="770" height="531" alt="Screenshot 2026-04-12 at 7 51 20 PM" src="https://github.com/user-attachments/assets/d13cbc8e-b003-46e5-8e1a-cbcebc9cef47" />
<img width="776" height="533" alt="Screenshot 2026-04-12 at 7 51 36 PM" src="https://github.com/user-attachments/assets/05904b48-6728-427b-a203-d3dbd779e260" />

## Requirements

- Python 3.10+
- tkinter
- tkinterdnd2

## Installation

```bash
pip install tkinterdnd2
python gui_universal.py

## Author

Egor
