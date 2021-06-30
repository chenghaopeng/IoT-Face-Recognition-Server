import os
import face_recognition
from PIL import Image, ImageDraw
import numpy as np

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
    result = []
    image = face_recognition.load_image_file(img)
    locations = face_recognition.face_locations(image)
    face = face_recognition.face_encodings(image, locations)
    pil_image = Image.fromarray(image)
    draw = ImageDraw.Draw(pil_image)
    for (top, right, bottom, left), face_encoding in zip(locations, face):
        matches = face_recognition.compare_faces(known_faces, face_encoding, tolerance=0.5)
        name = 'unknown'
        face_distances = face_recognition.face_distance(known_faces, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            result.append(known_infos[best_match_index])
            name = known_infos[best_match_index]['id']
        draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))
        _, text_height = draw.textsize(name)
        draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
        draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))
    pil_image.save('./static/image.jpg')
    return result

load_faces()
print(known_faces, flush=True)
print(known_infos, flush=True)
