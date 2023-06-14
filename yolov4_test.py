import argparse
import time
import glob

import cv2
import numpy as np

import os

#parser = argparse.ArgumentParser()
#parser.add_argument("-i", "--input", type=str, default="", required=True,
	#help="path to input image file")
#parser.add_argument("-o", "--output", type=str, default="",
	#help="path to (optional) output image file. Write only the name, without extension.")
#parser.add_argument("-c", "--confidence", type=float, default=0.5,
	#help="minimum probability to filter weak detections")
#parser.add_argument("-t", "--threshold", type=float, default=0.4,
	#help="threshold for non maxima supression")

#args = parser.parse_args()

#impath = args.input

#print("You are now using {} weights ,{} configs and {} labels.".format(weights, cfg, labels))

#layer = [layer[i[0] - 1] for i in net.getUnconnectedOutLayers()]


def detectObject(image):

    CONFIDENCE_THRESHOLD = 0.2
    NMS_THRESHOLD = 0.2

    weights = 'yolov4-custom_best.weights'
    labels = 'obj.names'
    cfg = 'yolov4-custom.cfg'

    lbls = list()
    with open(labels, "r") as f:
        lbls = [c.strip() for c in f.readlines()]

    COLORS = np.random.randint(0, 255, size=(len(lbls), 3), dtype="uint8")

    net = cv2.dnn.readNetFromDarknet(cfg, weights)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

    layer = net.getLayerNames()
    layer = [layer[i - 1] for i in net.getUnconnectedOutLayers()]

    #### DETEKSI DI BAWAH ####

    #image = cv2.imread(imgpath)
    #assert image is not None, f"Image is none, check file path. Given path is: {imgpath}"

    (H, W) = image.shape[:2]

    blob = cv2.dnn.blobFromImage(image, 1 / 255, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    start_time = time.time()
    layer_outs = net.forward(layer)
    end_time = time.time()

    boxes = list()
    confidences = list()
    class_ids = list()

    for output in layer_outs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > CONFIDENCE_THRESHOLD:
                box = detection[0:4] * np.array([W, H, W, H])
                (center_x, center_y, width, height) = box.astype("int")

                x = int(center_x - (width / 2))
                y = int(center_y - (height / 2))

                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    idxs = cv2.dnn.NMSBoxes(boxes, confidences, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)
    if len(idxs) > 0:
        for i in idxs.flatten():
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])

            color = [int(c) for c in COLORS[class_ids[i]]]
            cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
            #text = "{}: {:.4f}".format(lbls[class_ids[i]], confidences[i])
            #cv2.putText(
            #    image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2
            #)
            #label = "Inference Time: {:.2f} s".format(end_time - start_time)
            #cv2.putText(
            #    image, label, (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2
            #)

    #cv2.imshow(imgpath, image)
    #cv2.waitKey(0)
    folder_hasil = 'C:/Users/oyoni/yolov4test1/YOLO-v3-Object-Detection/hasil deteksi/'
    #cv2.imwrite(os.path.join(folder_hasil, image.rstrip(".jpg")+" "+"hasil"+".jpg"), image)
    #hasil_deteksi=os.path.join(folder_hasil, imgpath.rstrip(".jpg")+" "+"hasil"+".jpg")
    #my_string = os.path.join(folder_hasil, imgpath.rstrip(".jpg")+" "+"hasil"+".jpg")
    #path_string=image.rstrip(".jpg")+" "+"hasil"+".jpg"
    #old_substring = "/"
    #new_substring = "\"

    #split_list = my_string.split(old_substring)
    #new_list = [new_substring if i < len(split_list)-1 else '' for i in range(len(split_list)-1)]
    #new_string = ''.join([split_list[i] + new_list[i] for i in range(len(split_list)-1)] + [split_list[-1]])

    return image
    
#detectObject(impath)