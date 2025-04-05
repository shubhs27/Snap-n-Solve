# Snap-n-Solve

Snap-n-Solve is a real-time Sudoku puzzle solver that uses computer vision and machine learning to detect, solve, and overlay solutions on Sudoku puzzles captured through your webcam.

## Table of Contents

- [Features](#features)
- [Screenshots](#screenshots)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
  - [1. Sudoku Board Detection](#1-sudoku-board-detection)
  - [2. Digit Recognition](#2-digit-recognition)
  - [3. Puzzle Solving](#3-puzzle-solving)
  - [4. Solution Display](#4-solution-display)
- [Best-First Search Algorithm](#best-first-search-algorithm)
  - [Heap Implementation](#heap-implementation)
  - [How It Works](#how-it-works-1)
- [Project Structure](#project-structure)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)
- [Future Improvements](#future-improvements)
- [Acknowledgements](#acknowledgements)
- [License](#license)

## Features

- **Real-time Sudoku detection** using computer vision techniques
- **Automated digit recognition** with a trained Convolutional Neural Network (CNN)
- **Intelligent puzzle solving** using a Best-First search algorithm
- **Difficulty assessment** of detected puzzles (Easy, Medium, Hard, Expert)
- **Live solution overlay** directly on the webcam feed
- **Performance monitoring** with FPS counter

## Screenshots

<!--
![Sudoku Detection](screenshots/sudoku-detection.png)
*Sudoku grid detection and perspective transformation*

![Digit Recognition](screenshots/digit-recognition.png)
*Detection of digits in the Sudoku grid*

![Solution Overlay](screenshots/solution-overlay.png)
*Real-time overlay of the solution on the puzzle*

![Difficulty Assessment](screenshots/difficulty-assessment.png)
*Puzzle difficulty evaluation and display*
-->

## Requirements

- Python 3.10 or above
- The following Python packages:

```
keras==3.8.0
numpy==1.26.4
opencv-python==4.11.0
scipy==1.15.2
tensorflow==2.16.2
```

## Installation

1. Clone this repository or download the source code
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Make sure all files are in the same directory:
   - `main.py` - The main entry point
   - `RealTimeSudokuSolver.py` - Core processing code
   - `sudokuSolver.py` - Puzzle solving algorithm
   - `sudokuDifficulty.py` - Puzzle difficulty assessment
   - `digitRecognition.h5` - Trained neural network model for digit recognition

## Usage

1. Run the main script:

```bash
python main.py
```

2. Hold a Sudoku puzzle in front of your webcam
3. The application will:
   - Detect the Sudoku grid
   - Recognize the digits
   - Solve the puzzle
   - Display the solution overlaid on the video feed
   - Show the puzzle's difficulty level
4. Press 'q' to quit the application

## How It Works

### 1. Sudoku Board Detection

The application uses OpenCV to:

- Apply adaptive thresholding using cv2.adaptiveThreshold
- Identify contours with cv2.findContours
- Find the largest quadrilateral contour (the Sudoku board)
- Transform the perspective using cv2.warpPerspective to get a top-down view of the board

### 2. Digit Recognition

For each cell in the grid:

- Extract the cell image
- Process and normalize the image using cv2.resize and cv2.threshold
- Use a pre-trained CNN to recognize digits
- Build a numerical representation of the puzzle

### 3. Puzzle Solving

Once the puzzle is represented as a 9x9 grid:

- Verify the puzzle is valid
- Calculate the difficulty level
- Use a Best-First search algorithm to efficiently solve the puzzle
- The algorithm prioritizes cells with the fewest possible values

### 4. Solution Display

The solved values are:

- Rendered on the transformed image using cv2.putText
- Inverse perspective transformed back to the original frame
- Displayed as an overlay on the live camera feed

## Best-First Search Algorithm

### Heap Implementation

Our Sudoku solver uses Python's `heapq` module to implement a min-heap priority queue that significantly optimizes the solving process:

- Empty cells are prioritized by the number of valid digit choices they have (fewer choices = higher priority)
- The `EntryData` class tracks each cell's position and number of valid choices
- Custom comparison methods enable efficient heap operations

### How It Works

1. **Initial Setup**:

   - Calculate valid choices for each empty cell
   - Add all empty cells to the min-heap, ordered by fewest choices

2. **Solving Process**:

   - Always select the cell with fewest options first (from top of heap)
   - Try placing valid digits and update remaining cell priorities
   - Create new heap with recalculated priorities for each branch

3. **Performance Benefits**:
   - Significantly reduces the search space by making optimal choices
   - Minimizes backtracking by selecting constrained cells first
   - Solves even difficult puzzles efficiently by focusing on the most constrained parts first

## Project Structure

- **main.py**: Entry point, webcam handling, and main loop
- **RealTimeSudokuSolver.py**: Image processing, digit recognition, and solution overlay
- **sudokuSolver.py**: Best-First search algorithm implementation
- **sudokuDifficulty.py**: Analysis of puzzle complexity
- **digitRecognition.h5**: Pre-trained CNN model file

## Acknowledgements

- **Anh Minh Tran**: for the original project inspiration and implementation
  - https://github.com/anhminhtran235/real_time_sudoku_solver
- **Chars74K**: dataset for providing the computer font digit samples used in training
  - http://www.ee.surrey.ac.uk/CVSSP/demos/chars74k/
- **Peter Norvig's** efficient constraint satisfaction algorithm:
  - https://github.com/norvig/pytudes/blob/main/ipynb/Sudoku.ipynb
- **Nesh Patel's** articles on Sudoku solving algorithms:
  - Solving Sudoku Part I: https://medium.com/@neshpatel/solving-sudoku-part-i-7c4bb3097aa7
  - Solving Sudoku Part II: https://medium.com/@neshpatel/solving-sudoku-part-ii-9a7019d196a2
- Various tutorials and resources from OpenCV, Stack Overflow, and educational platforms that contributed to the improved implementation

## Customization

- Adjust camera settings in `main.py` if needed
- The neural network model is already trained, but you can retrain it with your own digit samples

## Troubleshooting

- Ensure good lighting conditions for better digit recognition
- Hold the Sudoku puzzle relatively flat to the camera
- If recognition is poor, try to minimize glare and shadows on the puzzle

## Future Improvements

- Support for mobile devices
- Save and load puzzles functionality
- Step-by-step solution visualization
- Enhanced image processing for better recognition in challenging conditions

## License

This project is open-source and available for personal and educational use.
