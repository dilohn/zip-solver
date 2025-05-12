# Zip Solver

This project detects and solves LinkedIn Zip mazes. It uses OpenCV for image processing and Tesseract OCR to read labels from the board.

## Features

- Automatically detects vertical and horizontal walls on a 6x6 grid.
- Uses Tesseract OCR to identify numbered labels.
- Finds a valid path visiting all labels in order.
- Outputs the solution path on the original image.

## Files

- `zip_algo.py`: Main script to read the puzzle image, detect walls and labels, solve the maze, and write the solution image.
- `board_reader.py`: Contains logic for detecting grid walls and extracting label positions using OCR.
- `puzzle_1.png`: Input image of the maze.
- `puzzle_1_detected.png`: Debug image with detected walls and labels.
- `solved.png`: Output image with the solution path overlaid.

## Requirements

Make sure you have the following installed:

- Python 3.x
- OpenCV (`opencv-python`)
- Pillow (`Pillow`)
- pytesseract (`pytesseract`)
- Tesseract OCR engine

You **must** have [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) installed on your system and properly configured. On Ubuntu, install with:

## Example
![puzzle_1](https://github.com/user-attachments/assets/c2d025c1-5f45-4546-894d-d6bcb8e8f319)
![puzzle_1_detected](https://github.com/user-attachments/assets/8c2ec8ae-8e82-4bdd-9a73-1510130bb1d2)
![solved](https://github.com/user-attachments/assets/132db5af-a810-47f0-8210-f738f80dfe58)

