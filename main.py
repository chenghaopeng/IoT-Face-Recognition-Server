from recognition import *
from flask import Flask, request
import os

app = Flask('iot')

@app.route('/', methods=['GET'])
@app.route('/<string:file>', methods=['GET'])
def index(file=None):
    return app.send_static_file(file if file else 'index.html')

@app.route('/upload', methods=['POST'])
def upload():
    image = request.files.get('image')
    img_path = './tmp/' + image.filename
    image.save(img_path)
    res = recognite(img_path)
    os.remove(img_path)
    return res
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
