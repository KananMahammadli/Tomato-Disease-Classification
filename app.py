import os
import base64

from functools import wraps
from dotenv import load_dotenv
from prediction import model_predict
#from waitress import serve

import logger

# Flask utils
from flask import Flask, request, render_template, abort, jsonify
from flask_cors import CORS

# authenticating with api key
def get_env_value(env_var_name):
    env_path = os.path.join('.', '.env')
    load_dotenv(dotenv_path=env_path)
    return os.getenv(env_var_name)

# getting api key from environment
API_KEY = get_env_value('API_KEY')

def require_apikey(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):

        if request.headers.get('key') and request.headers.get('key') == API_KEY:
            return view_function(*args, **kwargs)
        else:
            abort(401)

    return decorated_function

def create_error_response(message, status_code=400):
    resp = jsonify(error=message)
    resp.status_code = status_code
    return resp

# Define a flask app
app = Flask(__name__, template_folder='./templates', static_folder='./static')
CORS(app)

# create a logger
log = logger.setup_applevel_logger()


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')

@app.route('/about', methods=['GET'])
def about():
    # About page
    return render_template('about.html')


@app.route('/predict', methods=['POST'])
def upload():
    log.debug("\nDebug Started...!")
    try:
        if request.method != 'POST':
            log.debug("Request method should be POST, but received {}.".format(request.method))
            log.debug("\nDebug finished...!")
            return create_error_response('bad request [No POST Request]', status_code=403)

        # Get the image from post request as binary and convert bytes data into PIL image object
        img_bytes = request.files['file'].read()
            
        # Make prediction
        preds = model_predict(img_bytes)
        log.debug("\nDebug finished...!")
        return preds
            
    except Exception as e:
        log.debug(e)
        log.debug("\nDebug finished...!")
        return {'label':"Couldn't make prediction with given image", 'confidence score': "None"}
    

# this route is for desktop app
# when this route receive a request with correct api_key, it returns a response with predicted label and confidence score
@app.route('/predict_request', methods=['POST'])
@require_apikey
def get_disease():
    log.debug('\nDebug Started...')
    try:
        # request json format should be: {"image":image_file}
        # image_file should be encoded base64 image as plain text (encoded into utf-8)
        if not request.json: 
            log.debug('request is not in json format')
            log.debug('\nDebug Finished...!')
            return create_error_response('bad request [No json]', status_code=403)

        elif 'image' not in request.json:
            log.debug("'image' key is not in the request.")
            log.debug('\nDebug Finished...!')
            return create_error_response('bad request [NO image key]', status_code=403)

        else:
            # get the base64 encoded string
            im_b64 = request.json['image']

            # convert it into bytes  
            img_bytes = base64.b64decode(im_b64.encode('utf-8'))

            # Make prediction
            preds = model_predict(img_bytes)

            # decoding            
            resp = jsonify(preds)
            resp.status_code = 200
            log.debug('\nDebug Finished...!')
            return resp

    except Exception as e:
        log.debug(e)
        log.debug('\nDebug Finished...!')
        return {'label':"Couldn't make prediction with given image", 'confidence score': "None"}


if __name__ == '__main__':
    #serve(app, host='0.0.0.0', port=int(os.environ.get("PORT", "8080")))
    app.run(host='0.0.0.0', port=8080)