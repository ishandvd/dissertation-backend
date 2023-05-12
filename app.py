from datetime import datetime
from flask import Flask, request
import os
import time
from werkzeug.utils import secure_filename
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import sys
sys.path.append("./models/NMF")
from nmf_main import nmf_wrapper
import io
sys.path.append("./utils")
import flask_utils

UPLOAD_FOLDER = './audio_uploads'


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app,resources={r"/*":{"origins":"*"}})
ALLOWED_EXTENSIONS = {'wav'}

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
   print('Request for index page received')
   return {"status": "ok", "message": "Hello World!"}

@app.route('/backing-track', methods=['POST'])
def backing():
    print(f"{bcolors.OKGREEN}attempting to transcribe backing track{bcolors.ENDC}")
    try:
        print(request.files['backing_track'])
        file = request.files['backing_track']
        file_obj = io.BytesIO(file.read())
        print(request.files['backing_track'])
        file_user = request.files['user_track']
        file_obj_user = io.BytesIO(file.read())
    except Exception as e:
        print(f"{bcolors.FAIL}error: {e}{bcolors.ENDC}")
        return {"status": "error", "message": "Error opening backing track file"}, 500
    
    try: 
        times_backing, _, _, _, _, _, _= nmf_wrapper(
            filepath_list=file_obj,
            plot_activations_and_peaks=False,
            plot_ground_truth_and_estimates=False,
            use_custom_training=False,
            goal=0.04)
        
        times_user, _, _, _, _, _, _= nmf_wrapper(
            filepath_list=file_obj_user,
            plot_activations_and_peaks=False,
            plot_ground_truth_and_estimates=False,
            use_custom_training=False,
            goal=0.04)
    except Exception as e:
        print(f"{bcolors.FAIL}error: {e}{bcolors.ENDC}")
        return {"status": "error", "message": "Error transcribing backing track"}, 500

    try:
        output = flask_utils.timings_to_json(times_backing, times_user)
        print("OUTPUT: ", output)
    except Exception as e:
        print(f"{bcolors.FAIL}error: {e}{bcolors.ENDC}")
        return {"status": "error", "message": "Error converting timings to JSON"}, 500
    
    return {"status": "ok", "timings": output}, 200

if __name__ == '__main__':
   app.run(debug=True)