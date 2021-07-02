from recognition import *
from flask import Flask, request, make_response, send_from_directory
import os
from util import *
from config import *
import requests
import multiprocessing as mp
import shutil
import base64
from PIL import Image
import json
import logging

log = logging.getLogger('werkzeug')
log.disabled = not DEBUG

app = Flask('iot')
image_queue = mp.Queue()
result_queue = mp.Queue()

if os.path.exists(TEMP_PATH):
    shutil.rmtree(TEMP_PATH)
os.mkdir(TEMP_PATH)

@app.route('/', methods=['GET'])
@app.route('/<string:file>', methods=['GET'])
def index(file=None):
    if file == 'image.jpg':
        return make_response(send_from_directory('./tmp', 'image.jpg'))
    return app.send_static_file(file if file else 'index.html')

@app.route('/upload', methods=['POST'])
def upload():
    data = request.get_json()
    try:
        image = data.get('image')
        filename = random_alpha_string() + '.jpg'
        img_path = './tmp/' + filename
        with open(img_path, 'wb') as f:
            f.write(base64.b64decode(image))
        im = Image.open(img_path)
        k = 0.5
        x, y = im.size
        out = im.resize((int(x * k), int(y * k)), Image.ANTIALIAS)
        out.save(img_path, quality=100)
        image_queue.put(img_path)
        return {'success': True}
    except:
        return {'success': False}

def image_recognite(image_queue: mp.Queue, result_queue: mp.Queue):
    while True:
        if image_queue.empty(): continue
        img_path = image_queue.get()
        res = recognite(img_path)
        os.remove(img_path)
        for p in res:
            result_queue.put(p['id'])
        print_flush(res)

def result_upload(result_queue: mp.Queue):
    nobody = True
    nobody_count = 0
    while True:
        if result_queue.empty(): continue
        id = result_queue.get()
        if int(id) == 0:
            if nobody:
                pass
            else:
                nobody_count += 1
                print_flush(f'nobody count = {nobody_count}')
                if nobody_count == 5:
                    print_flush(f'set nobody')
                    nobody = True
                    nobody_count = 0
                else:
                    print_flush(f'ignore')
                    continue
        else:
            nobody = False
            nobody_count = 0
        print_flush(f'upload result id: {id}')
        data = {'device': 'atlas200dk', 'readings': [{'name': 'facial_identification', 'value': id}]}
        try:
            res = requests.post(EDGEX_URL, data=json.dumps(data), timeout=2000, headers={'content-type': 'application/json'})
        except:
            print_flush('result upload error!!!')

if __name__ == '__main__':
    processes = [
        mp.Process(target=image_recognite, args=(image_queue, result_queue)),
        mp.Process(target=result_upload, args=(result_queue,))
    ]
    for process in processes:
        process.start()
    app.run(host='0.0.0.0', port=5000, debug=DEBUG)
