import face_recognition
from flask import Flask

app = Flask('iot')

@app.route('/', methods=['GET'])
def index():
    return 'hello world!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
