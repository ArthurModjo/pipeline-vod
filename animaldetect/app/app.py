import cv2
from ultralytics import YOLO
import argparse
from flask import Flask, Response, render_template, request
import tempfile
import socketio
import os

working_directory = "/processing"

# Define a function to detect animals in a video and write results to a text file
def detect_animals_and_write_to_file(file_path, output_folder):
    if file_path == "camera":
        cap = cv2.VideoCapture(0)
    else:
        cap = cv2.VideoCapture(file_path)

    # Initialize YOLOv8 model (you need to replace this with the actual YOLOv8 model initialization code)
    # Load the YOLOv8 model
    model = YOLO('animal_model.pt')

    output_file_name = os.path.splitext(os.path.basename(file_path))[0] + "_animal.txt"
    output_file_path = os.path.join(output_folder, output_file_name)

    with open(output_file_path, 'w') as output_file:
        detected_animals = set()  # Set to store unique animal names
        while cap.isOpened():
            success, frame = cap.read()

            if success:
                # Run YOLOv8 inference on the frame
                results = model(frame)[0]
                frame_ = results.plot()  # or .render()
                # Check if any animal is detected in the frame
                for key, value in results.names.items():
                    if value in ["bird", "cat", "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe"]:
                        detected_animals.add(value)

                #cv2.imshow("Frame", frame_)
                if cv2.waitKey(1) == 27:  # Exit when ESC key is pressed
                    break
            else:
                break

        # Write the unique animal names to the output file
        output_lines = [animal + '\n' for animal in detected_animals]
        output_file.writelines(output_lines)
    cap.release()
    return output_file_name

if __name__ == '__main__':
    sio = socketio.Client()

    @sio.event
    def connect():
        print('connection established')

    @sio.event
    def identification(data):
        sio.emit('identification', {'response': 'animaldetect'})

    @sio.event
    def your_turn(data):
        file = detect_animals_and_write_to_file(working_directory + '/' + data["video"], working_directory)
        data = {
            "video": data["video"],
            "langue": data["langue"],
            "subtitles": data["subtitles"],
            "animal": file
        }
        sio.emit('animaldetect_done', data)

    @sio.event
    def disconnect():
        print('disconnected from server')

    sio.connect('http://172.20.0.10:5000')
    sio.wait()