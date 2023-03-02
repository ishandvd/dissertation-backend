from datetime import datetime
from flask import Flask, request, jsonify
import os
import time
from werkzeug.utils import secure_filename
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import sys
sys.path.append("./models/NMF")
from nmf_main import NmfDrum


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
    print(f"{bcolors.OKGREEN}attempting to store backing track{bcolors.ENDC}")
    print(request.files['backing_track'])
    file = request.files['backing_track']
    if file and allowed_file(file.filename):
        filename = time.strftime("%Y%m%d-%H%M%S") + secure_filename(file.filename) 
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return {"status": "ok", "message": f"Successfully uploaded {filename}"}, 200
    else:
        return {"status": "error", "message": "Error uploading file"}, 400


@app.route('/audio-upload', methods=['POST'])
def audio_upload():
    print('Request for audio upload received', request.content_type)
    if request.method == 'POST':
        # check if the post request has the file part
        print(request.files['wavfile'])
        file = request.files['wavfile']
        if file and allowed_file(file.filename):
            filename = time.strftime("%Y%m%d-%H%M%S") + secure_filename(file.filename) 
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return {"status": "ok", "message": "Hello World!"}, 200

if __name__ == '__main__':
   app.run(debug=True)