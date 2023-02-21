from datetime import datetime
from flask import Flask, request
import os
import time
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './audio_uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'wav'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
   print('Request for index page received')
   return {"status": "ok", "message": "Hello World!"}


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