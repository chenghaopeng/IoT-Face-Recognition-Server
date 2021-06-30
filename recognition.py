import os
import face_recognition

FACE_PATH = 'faces'
ALLOW_EXT = ['jpg', 'jpeg', 'png']

def get_encoding(img):
    return face_recognition.face_encodings(face_recognition.load_image_file(img))[0]

known_faces = []
known_infos = []

def load_faces():
    global known_faces
    global known_infos
    known_faces = []
    known_infos = []
    for img in os.listdir(FACE_PATH):
        if img.lower().split('.')[1] in ALLOW_EXT:
            img_path = os.path.join(FACE_PATH, img)
            try:
                face = get_encoding(img_path)
                id, name = img.split('.')[0].split('-')
            except:
                continue
            known_faces.append(face)
            known_infos.append({'id': id, 'name': name})

def recognite(img):
    try:
        face = get_encoding(img)
        result = face_recognition.compare_faces(known_faces, face, tolerance=0.5)
        print(result, flush=True)
        for i in range(len(known_faces)):
            if result[i]:
                return known_infos[i]
    except:
        pass
    return {'id': -1, 'name': '未知'}

load_faces()
print(known_faces, flush=True)
print(known_infos, flush=True)
