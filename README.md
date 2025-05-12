# Zip Solver

This project detects and solves LinkedIn Zip mazes. It uses OpenCV for image processing and Tesseract OCR to read labels from the board.

## Features

- Automatically detects vertical and horizontal walls on a 6x6 grid.
- Uses Tesseract OCR to identify numbered labels.
- Finds a valid path visiting all labels in order.
- Outputs the solution path on the original image.

## Files

- zip_algo.py: Main script to read the puzzle image, detect walls and labels, solve the maze, and write the solution image.
- board_reader.py: Contains logic for detecting grid walls and extracting label positions using OCR.
- puzzle_1.png: Input image of the maze.
- puzzle_1_detected.png: Debug image with detected walls and labels.
- solved.png: Output image with the solution path overlaid.

## Requirements

Make sure you have the following installed:

- Python 3.x
- OpenCV (opencv-python)
- Pillow (Pillow)
- pytesseract (pytesseract)
- Tesseract OCR engine

You must have [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) installed on your system and properly configured. On Ubuntu, install with:

## Example
![puzzle_1](https://github.com/user-attachments/assets/d893dcd8-af25-4600-84b6-d0ecbc3199c5)
![puzzle_1_detected](https://github.com/user-attachments/assets/2059aaa3-e184-4be0-9e2b-3825ff5aa1a4)
![solved](https://github.com/user-attachments/assets/31ad674f-271f-4fd0-943d-0bf080468dd1)
