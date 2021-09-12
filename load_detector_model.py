import tensorflow as tf

__detector = None

def load_detector_model():

    global __detector
    if not __detector:
        __detector = tf.saved_model.load('./efficientdet_d0_1')
        
    return __detector