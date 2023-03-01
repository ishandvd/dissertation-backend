from datetime import datetime
from flask import Flask, request, jsonify
import os
import time
from werkzeug.utils import secure_filename
from flask_socketio import SocketIO, emit
from flask_cors import CORS


UPLOAD_FOLDER = './audio_uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB
CORS(app,resources={r"/*":{"origins":"*"}})
socketio = SocketIO(app,cors_allowed_origins="*",message_queue_max_size=50000000, message_queue_timeout=60)

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


@socketio.on("connect")
def connected():
    """event listener when client connects to the server"""
    print(request.sid)
    print("client has connected")
    emit("connect",{"data":f"id: {request.sid} is connected"})

@socketio.on("disconnect")
def disconnected():
    """event listener when client disconnects to the server"""
    print("user disconnected")
    emit("disconnect",f"user {request.sid} disconnected",broadcast=True)

@socketio.on("backingtrack")
def backing_times(audio):
    print(f"{bcolors.OKGREEN}attempting to store backing track{bcolors.ENDC}")
    filename = time.strftime("%Y%m%d-%H%M%S") + ".wav"
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    with open(file_path, 'wb') as f:
        f.write(audio)
    # chunk_size = 1024  # set chunk size to 1 KB
    # with open(file_path, 'ab') as f:
    #     while True:
    #         chunk = audio.read(chunk_size)
    #         if not chunk:
    #             break
    #         f.write(chunk)
    print("backing track stored")
    emit("backingtrack",f"You just submitted a file properly (hopefully)")

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
   socketio.run(app, debug=True)