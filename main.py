from recognition import *
from flask import Flask, request
import os
from util import *
from config import *
import requests
import multiprocessing as mp

app = Flask('iot')
image_queue = mp.Queue()
result_queue = mp.Queue()

@app.route('/', methods=['GET'])
@app.route('/<string:file>', methods=['GET'])
def index(file=None):
    return app.send_static_file(file if file else 'index.html')

@app.route('/upload', methods=['POST'])
def upload():
    try:
        image = request.files.get('image')
        ext = image.filename.rsplit('.', 1)
        filename = random_alpha_string()
        if len(ext) > 1:
            filename += '.' + ext[-1]
        img_path = './tmp/' + filename
        image.save(img_path)
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
    while True:
        if result_queue.empty(): continue
        id = result_queue.get()
        data = {'Int64': id}
        try:
            res = requests.put(EDGEX_URL, data=data, timeout=2000)
            print_flush(res.status_code)
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
