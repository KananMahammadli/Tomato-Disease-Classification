import io
import logger
import numpy as np
import tensorflow as tf
from PIL import Image

# Load your trained model
MODEL_PATH = 'model/model_tomato.h5'
model = tf.keras.models.load_model(MODEL_PATH)

# create a logger
log = logger.setup_applevel_logger()

def preprocess(img_bytes):
    # convert bytes data to PIL Image object
    img = Image.open(io.BytesIO(img_bytes))

    # model has been trained with 64x64 images, so we need to resize input image
    img = img.resize((64, 64))
            
    # PIL image object to numpy array with scaling
    img_arr = np.asarray(img) / 255
    return img_arr

def decoder(labels):
    pred = np.argmax(labels, axis=1)[0]
    dic = {
    0:'Bacterial_spot',
    1:'Early_blight',
    2:'Late_blight',
    3:'Leaf_Mold',
    4:'Septoria_leaf_spot',
    5:'Spider_mites Two-spotted_spider_mite',
    6:'Target_Spot',
    7:'Tomato_Yellow_Leaf_Curl_Virus',
    8:'Tomato_mosaic_virus',
    9:'healthy'}

    return {"label":dic[pred], "confidence score": str(round(labels[0][pred]*100)) + "%"}


def model_predict(img_bytes):
    # preprocessing image for prediction
    img_arr = preprocess(img_bytes)

    # make sure image had 3 dimesnions and 3d dimension is 3
    if len(img_arr.shape) != 3:
        log.debug(f'image shape: {img_arr.shape}')
        return {"label": f"Image should be 3d, but received {len(img_arr.shape)}", "confidence score": "None"}

    elif img_arr.shape[2] != 3:
        log.debug(f'image shape: {img_arr.shape}')
        return {"label": f"3rd dimension of image should be 3, but received {img_arr.shape[2]}", "confidence score": "None"}

    img_arr = np.expand_dims(img_arr, axis=0)
    preds = decoder(model.predict(img_arr))
    return preds