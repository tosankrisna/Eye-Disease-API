import os
import numpy as np
import tensorflow as tf
import keras.utils as image

from flask import jsonify, request
from app import app, project_dir
from .models import EyeDisease, db

model = tf.keras.models.load_model('model.h5')

@app.route('/')
def index():
    return 'Welcome to Eye Disease Detection API'

@app.route('/predict', methods=['POST'])
def predict():
    img = request.files["image"]
    img_url = project_dir + os.path.join(app.config['UPLOAD_FOLDER'], img.filename)
    img.save(img_url)

    img_size = (150, 150)
    img_test = image.load_img(img_url, target_size = img_size)
    img_test = image.img_to_array(img_test)
    img_test = np.expand_dims(img_test, axis=0)

    prediction = model.predict(img_test)

    if prediction[0][0] > 0.5:
        prediction_name = 'Normal'
        prediction_img = img_url
        prediction_desc = 'Mata dalam keadaan sehat, selalu jaga mata dengan makan makanan bergizi.'
    else:
        prediction_name = 'Katarak'
        prediction_img = img_url
        prediction_desc = 'Mata terdeteksi penyakit katarak, hubungi pelayanan medis untuk pengecekan lebih lanjut.'

    eye_disease = EyeDisease(name=prediction_name, img_url=prediction_img, desc=prediction_desc)
    db.session.add(eye_disease)
    db.session.commit()

    return jsonify({
        'message': 'success',
        'result': {
            'name': prediction_name,
            'img_url': prediction_img,
            'desc' : prediction_desc
        }
    })

@app.route('/diseases')
def disease():
    diseases = EyeDisease.query.all()
    
    return jsonify({
        'message': 'success',
        'result': [disease.to_json() for disease in diseases]
    })