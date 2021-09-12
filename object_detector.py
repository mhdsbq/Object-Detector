import tensorflow as tf
import PIL
import numpy as np
from load_detector_model import load_detector_model


# The COCO dataset classes;  which the model is trained on.
CLASSES_90 = ["background", "person", "bicycle", "car", "motorcycle",
            "airplane", "bus", "train", "truck", "boat", "traffic light", "fire hydrant",
            "unknown", "stop sign", "parking meter", "bench", "bird", "cat", "dog", "horse",
            "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "unknown", "backpack",
            "umbrella", "unknown", "unknown", "handbag", "tie", "suitcase", "frisbee", "skis",
            "snowboard", "sports ball", "kite", "baseball bat", "baseball glove", "skateboard",
            "surfboard", "tennis racket", "bottle", "unknown", "wine glass", "cup", "fork", "knife",
            "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli", "carrot", "hot dog",
            "pizza", "donut", "cake", "chair", "couch", "potted plant", "bed", "unknown", "dining table",
            "unknown", "unknown", "toilet", "unknown", "tv", "laptop", "mouse", "remote", "keyboard",
            "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator", "unknown",
            "book", "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush"]


def object_detector(detector, img_location: str, num_detection=5 ) -> list:
    """
    input an image as './path/to/image.jpg' and returns detected objects with it's detection scores.
    optional argument: num_detection - 'n' most probable detections will be returned,default=5.
    """
    img = PIL.Image.open(img_location)
    img = np.array(img)
    img = tf.expand_dims(img, axis=0)
    result = detector(img)

    ret = []

    for i in range(num_detection):
        detection_class_number = int(result['detection_classes'].numpy()[0][i])
        detection_class_name = CLASSES_90[detection_class_number]

        detection_score = result['detection_scores'].numpy()[0][i]
        rounded_detection_score = round(float(detection_score), 2)

        # Append as a tuple
        ret.append( (detection_class_name, rounded_detection_score) )

    return ret

if __name__ == "__main__":
    detector = load_detector_model()
    print(object_detector(detector, './assets/car.jpeg'))

    # output -> [('car', 0.94), ('truck', 0.14), ('person', 0.1), ('person', 0.09), ('person', 0.08)]
