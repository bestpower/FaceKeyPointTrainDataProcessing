from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
#os.environ['CUDA_VISIBLE_DEVICES'] = '0'
#print('pid: {}     GPU: {}'.format(os.getpid(), os.environ['CUDA_VISIBLE_DEVICES']))
import tensorflow as tf
import numpy as np
import cv2
from mtcnn.detect_face import MTCNN

def main(img_path):
    image_size = 112
    lite_filename = 'deploy/landmarks68/pfld_landmarks.tflite'
    # load TFLite model and allocate tensors
    interpreter = tf.contrib.lite.Interpreter(model_path=lite_filename)
    interpreter.allocate_tensors()

    # get input and output tensors.
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    
    with tf.Graph().as_default():
        with tf.Session() as sess:
            mtcnn = MTCNN()
            image = cv2.imread(img_path)
            height, width,_ =image.shape
            boxes , landmarks_mtcnn= mtcnn.predict(image)

    if len(landmarks_mtcnn) > 0:
        landmarks_mtcnn = np.asarray(landmarks_mtcnn).reshape(len(boxes), 10)
    
    for box in boxes:
        score = box[4]
        x1, y1, x2, y2 = (box[:4]+0.5).astype(np.int32)

        # mtcnn boundding box fine adjustment
        dta_y = (min(landmarks_mtcnn[0][5], landmarks_mtcnn[0][6]) - y1) / 2.6
        y1 = int(y1 + dta_y)
        y2 = int(y2 + dta_y/2)

        w = x2 - x1 + 1
        h = y2 - y1 + 1

        size = int(max([w, h])*1.05)
        cx = x1 + w//2
        cy = y1 + h//2
        x1 = cx - size//2
        x2 = x1 + size
        y1 = cy - size//2
        y2 = y1 + size

        dx = max(0, -x1)
        dy = max(0, -y1)
        x1 = max(0, x1)
        y1 = max(0, y1)

        edx = max(0, x2 - width)
        edy = max(0, y2 - height)
        x2 = min(width, x2)
        y2 = min(height, y2)

        cropped = image[y1:y2, x1:x2]
        if (dx > 0 or dy > 0 or edx > 0 or edy > 0):
            cropped = cv2.copyMakeBorder(cropped, dy, edy, dx, edx, cv2.BORDER_CONSTANT, 0)
        cropped = cv2.resize(cropped, (image_size, image_size))

        input = cv2.resize(cropped, (image_size, image_size))
        input = cv2.cvtColor(input, cv2.COLOR_BGR2RGB)
        input = input.astype(np.float32)/256.0
        input = np.expand_dims(input, 0)

        interpreter.set_tensor(input_details[0]['index'], input)

        interpreter.invoke()
        pre_landmarks = interpreter.get_tensor(output_details[0]['index'])
        pre_landmark = pre_landmarks[0]
        pre_landmark = pre_landmark.reshape(-1, 2) * [size, size]
        return pre_landmark.astype(np.float32), x1, y1

        # idx = 0
        # font = cv2.FONT_HERSHEY_SIMPLEX
        # for (x, y) in pre_landmark.astype(np.int32):
        #     cv2.circle(image, (x1 + x, y1 + y), 2, (0, 255, 0), thickness=-1)
        #     cv2.putText(image, str(idx+1), (x1 + x, y1 + y), font, 0.4, (0, 0, 255), 1, cv2.LINE_AA)
        #     idx = idx + 1
    
    # cv2.imshow('0', image)
    # cv2.waitKey(0)

# if __name__ == '__main__':
#     main()
