# Tango Puzzle Solver

This project detects and solves 6x6 Tango puzzles from images of LinkedIn Tango. It uses OpenCV for visual processing and constraint-based logic to deduce valid solutions based on cell contents and relationship markers.

## Features

- Detects "C" and "M" markers using color recognition.
- Identifies "equals" (=) and "excludes" (X) constraints between adjacent cells via template matching.
- Enforces no-three-in-a-row and balancing constraints for valid logical deduction.
- Overlays the final solution onto the original puzzle image.

## Files

- `main.py`: Main script to process the puzzle image, run the solver, and print the solution.
- `read_board.py`: Handles image parsing, color and symbol detection, and constraint extraction.
- `tango_algo.py`: Contains the logic solver implementing constraint propagation and backtracking.
- `overlay_solution.py`: Writes the solution on top of the puzzle image for visualization.
- `puzzle.png`: Input image containing the puzzle to solve.
- `detections.png`: Debug image showing detected symbols and constraints.
- `filled.png`: Final output image with the solution filled in.
- `x_template.png`: Template for detecting the "X" constraint.
- `equals_template.png`: Template for detecting the "=" constraint.

## Requirements

Make sure you have the following installed:

- Python 3.x
- OpenCV (`opencv-python`)
- NumPy (`numpy`)

## Example

Below is a sample pipeline from raw puzzle to solution:

![puzzle](https://github.com/user-attachments/assets/97a4bc93-9e05-4bd3-b895-f4d110cf98ea)
![detections](https://github.com/user-attachments/assets/fc41f94a-1cf7-4a08-9e5e-5f4d9ea8bde4)
![filled](https://github.com/user-attachments/assets/63e9f58e-e90f-4659-818c-dcdaa558b608)

