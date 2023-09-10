import tensorflow as tf
import tensorflow_hub as hub
import cv2
import numpy as np
import os

# Specify the model URL for the desired object detection model
model_url = "https://tfhub.dev/google/openimages_v4/ssd/mobilenet_v2/1"

# Load the model from TensorFlow Hub
detector = hub.load(model_url).signatures['default']

inputPath = "C:\\Users\\Aum\\CodeForGood\\test_images\\"
outputPath = "C:\\Users\\Aum\\CodeForGood\\output_images\\"

def detectAndCountVehicles(filename):
    img = cv2.imread(inputPath + filename)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.astype(np.float32) / 255.0  # Normalize the input image to float32 [0, 1]
    img = np.expand_dims(img, axis=0)

    # Perform object detection using the loaded model
    detections = detector(tf.convert_to_tensor(img))

    # Initialize vehicle count
    vehicle_count = 0

    # Check if 'detection_classes' key is present in the detections dictionary
    if 'detection_classes' in detections:
        classes = detections['detection_classes'][0].numpy().astype(int)
        scores = detections['detection_scores'][0].numpy()
        for i in range(len(classes)):
            if scores[i] > 0.5:  # Adjust the confidence threshold as needed
                if classes[i] == 3:  # Class label for "car"
                    vehicle_count += 1
                    ymin, xmin, ymax, xmax = detections['detection_boxes'][0][i].numpy()
                    left = int(xmin * img.shape[2])
                    top = int(ymin * img.shape[1])
                    right = int(xmax * img.shape[2])
                    bottom = int(ymax * img.shape[1])
                    cv2.rectangle(img[0], (left, top), (right, bottom), (0, 255, 0), 2)

    outputFilename = outputPath + "output_" + filename
    cv2.imwrite(outputFilename, cv2.cvtColor(img[0], cv2.COLOR_RGB2BGR))
    print('Output image stored at:', outputFilename)
    print('Number of vehicles detected:', vehicle_count)

for filename in os.listdir(inputPath):
    if filename.lower().endswith((".png", ".jpg", ".jpeg")):
        detectAndCountVehicles(filename)
