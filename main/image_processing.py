import numpy as np
import cv2
import colorsys

import os


def process(img):
    curr_dir = os.getcwd()

    net = cv2.dnn.readNet(os.path.join(curr_dir, 'main', 'config', 'yolov3.weights'), os.path.join(curr_dir, 'main', 'config', 'yolov3.cfg'))

    classes = []

    with open(os.path.join(curr_dir, 'main', 'config', 'coco.names'), 'r', encoding='utf-8') as f:
        classes = list(f.read().strip().split('\n'))

    nparr = np.frombuffer(img.read(), np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    h, w, _ = image.shape

    blob = cv2.dnn.blobFromImage(image, 1 / 255, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)

    outs = net.forward(net.getUnconnectedOutLayersNames())

    class_ids = []
    confidences = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.7:
                class_ids.append(class_id)
                confidences.append(confidence)

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pixel_vals = image.reshape((-1, 3))
    pixel_vals = np.float32(pixel_vals)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    _, labels, centers = cv2.kmeans(pixel_vals, 1, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    dominant_color = np.uint8(centers[0])
    hexed = f'#{dominant_color[0]:02x}{dominant_color[1]:02x}{dominant_color[2]:02x}'

    object_names = [classes[class_id] for class_id in class_ids]
    return ' '.join(list(set(object_names))), h, w, hexed