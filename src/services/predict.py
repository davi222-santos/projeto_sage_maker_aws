import tensorflow as tf
from tensorflow import keras

from utils.predictUtils import functions


def predictFunc(inputs):
    new_model = tf.keras.models.load_model('src/resources/model.h5')
    predictions = new_model.predict([inputs])
    max_index=functions.find_max_index(list(predictions[0]))
    return max_index




