from recognition import *
from flask import Flask, request
import os
from util import *

app = Flask('iot')

@app.route('/', methods=['GET'])
@app.route('/<string:file>', methods=['GET'])
def index(file=None):
    return app.send_static_file(file if file else 'index.html')

@app.route('/upload', methods=['POST'])
def upload():
    image = request.files.get('image')
    ext = image.filename.rsplit('.', 1)
    filename = random_alpha_string()
    if len(ext) > 1:
        filename += '.' + ext[-1]
    img_path = './tmp/' + filename
    image.save(img_path)
    res = recognite(img_path)
    os.remove(img_path)
    return str(res)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
