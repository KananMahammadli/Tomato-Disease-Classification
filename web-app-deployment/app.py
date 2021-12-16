from __future__ import division, print_function
import os
import numpy as np
import tensorflow as tf

# Flask utils
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename

# Define a flask app
app = Flask(__name__)


# Load your trained model
MODEL_PATH = 'model/model_tomato.h5'
model = tf.keras.models.load_model(MODEL_PATH)


def model_predict(img_path, model):
    img = tf.keras.preprocessing.image.load_img(img_path, target_size=(64, 64))

    # Preprocessing the image
    img = tf.keras.preprocessing.image.img_to_array(img) / 255
    x = np.expand_dims(img, axis=0)

    preds = model.predict(x)
    return preds

def decoder(labels):
    pred = np.argmax(labels, axis=1)[0]
    dic = {0:'Bacterial_spot', 1:'Early_blight', 2:'Late_blight', 3:'Leaf_Mold', 4:'Septoria_leaf_spot', 5:'Spider_mites Two-spotted_spider_mite',
          6:'Target_Spot', 7:'Tomato_Yellow_Leaf_Curl_Virus', 8:'Tomato_mosaic_virus', 9:'healthy'}

    return dic[pred]


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path, model)

        # decoding
        pred_class = decoder(preds)              
        return pred_class

    return None


if __name__ == '__main__':
    app.run(debug=True)

