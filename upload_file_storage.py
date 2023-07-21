import os
import firebase_admin
import base64
from firebase_admin import credentials
from firebase_admin import storage


cred = credentials.Certificate('secret_firebase_storage.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'fir-eps32-img.appspot.com'
})


def decode_base64_to_image(base64_string):
    image_data = base64_string.split(",")[1]
    binary_data = base64.b64decode(image_data)
    print("Decodifico la foto")
    return binary_data

def upload_image_to_storage(image_binary_data, file_name):
    bucket = storage.bucket()
    blob = bucket.blob(file_name)
    blob.upload_from_string(image_binary_data, content_type="image/jpeg")
    
def get_image_base64_from_firebase(image_path):
        bucket = firebase_admin.storage.bucket()

        # Parsea la URL de la imagen para obtener el nombre del bucket y el objeto
        bucket_name, object_name = image_path.replace('gs://', '').split('/', 1)

        # Obtiene el objeto Blob que representa la imagen
        blob = bucket.blob(object_name)

        # Descarga los bytes de la imagen
        image_bytes = blob.download_as_bytes()
        print('Termino')
        return image_bytes
