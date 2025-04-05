# This is the entry point. Run this file!

import cv2
import numpy as np
import tensorflow as tf
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
import realTimeSudokuSolver
import time

# Load model once at startup for better efficiency
print("Loading neural network model...")
input_shape = (28, 28, 1)
num_classes = 9
model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3),
                activation='relu',
                input_shape=input_shape))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(num_classes, activation='softmax'))

# Load weights from pre-trained model. This model is trained in digitRecognition.py
try:
    model.load_weights("digitRecognition.h5")
    print("Model loaded successfully!")
except Exception as e:
    print(f"ERROR: Failed to load model: {e}")
    model = None  # Set to None so we can check for this later

def showImage(img, name, width, height):
    new_image = np.copy(img)
    new_image = cv2.resize(new_image, (width, height))
    cv2.imshow(name, new_image)

def main():
    print("=== Snap-n-Solve: Real-Time Sudoku Solver ===")
    print("Starting camera...")
    
    # Check if model loaded successfully
    if model is None:
        print("ERROR: Neural network model could not be loaded. Exiting.")
        return
    
    # Load and set up Camera
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)  # HD Camera
    cap.set(4, 720)
    
    if not cap.isOpened():
        print("ERROR: Could not open camera. Please check your connection.")
        return
    
    print("Camera initialized successfully!")
    
    print("\nInstructions:")
    print("- Hold a Sudoku puzzle in front of the camera")
    print("- The solution will be overlaid on the video")
    print("- The difficulty level will be shown above the puzzle")
    print("- Press 'q' to quit the application")
    print("\nStarting Snap-n-Solve...")
    
    # Initialize FPS calculation variables
    fps_counter = 0
    fps = 0
    prev_time = time.time()
    
    # Let's turn on webcam
    old_sudoku = None
    
    while True:
        ret, frame = cap.read()  # Read the frame
        
        if ret:
            # Calculate FPS
            fps_counter += 1
            current_time = time.time()
            if current_time - prev_time >= 1.0:  # Update FPS every second
                fps = fps_counter
                fps_counter = 0
                prev_time = current_time
            
            # Process frame and solve Sudoku
            sudoku_frame = realTimeSudokuSolver.recognize_and_solve_sudoku(frame, model, old_sudoku)
            
            # Add FPS counter to the frame
            cv2.putText(sudoku_frame, f"FPS: {fps}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            
            # Display the window with the new title
            showImage(sudoku_frame, "Snap-n-Solve", 1066, 600)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):  # Hit q if you want to stop the camera
                print("\nClosing Snap-n-Solve. Thank you for using!")
                break
        else:
            print("ERROR: Could not read frame from camera.")
            break
    
    # Clean up
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()