from datetime import datetime
from flask import Flask, request
import os
app = Flask(__name__)


@app.route('/')
def index():
   print('Request for index page received')
   return {"status": "ok", "message": "Hello World!"}


@app.route('/audio-upload', methods=['POST'])
def audio_upload():
    print('Request for audio upload received', request.content_type)
    if request.content_type == 'audio/wav':
        # Get the raw .wav file data from the request body
        file_data = request.data

        # Save the .wav file to disk
        with open('audio.wav', 'wb') as f:
            f.write(file_data)

        return 'Audio uploaded successfully', 200
    else:
        return 'Unsupported media type', 415


if __name__ == '__main__':
   app.run(debug=True)