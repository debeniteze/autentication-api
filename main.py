import os
import upload_file_storage
import send_message
from datetime import datetime
from google.cloud import vision
from base_vision import VisionAI
from fastapi import FastAPI
app = FastAPI()

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'fir-eps32-img-e1bd170cc844.json'

@app.get("/autentication-process-api")
def gvisionAPIProcess(string64file: str):
       
    def prepare_image_local(path):
        try:
            content = path
            print(content)
            image = vision.Image(content=content)
            return image
        except Exception as e:
            print(e)
            return
        
    #Se guarda la foto en storage
    print('paso 1')
    filename = "imagen.jpg"
    base64_img = upload_file_storage.decode_base64_to_image(string64file)
    upload_file_storage.upload_image_to_storage(base64_img, filename)    
        
    #trae la foto de storage    
    firebase_image_path = 'gs://fir-eps32-img.appspot.com/' + filename
    print(firebase_image_path)
    base64_image = upload_file_storage.get_image_base64_from_firebase(firebase_image_path)    

    
    image = prepare_image_local(base64_image)     
    client = vision.ImageAnnotatorClient()
    va = VisionAI(client, image)
    faces = va.face_detection()

    fecha_hora_actual = datetime.now()
    fecha_hora_formateada = fecha_hora_actual.strftime("%d/%m/%Y %H:%M:%S")

    if faces is not None:
        message = f"Se ha registrado un ingreso exitoso, el dia: {fecha_hora_formateada}"
        send_message.send_message(message)
        
        for face in faces:
            info = {
                "confianza": face.detection_confidence,
                "sonrisa": face.joy_likelihood,
                "cantidadRostros": len(faces)
            }
            break
        return info
    else:
            message = f"Se ha registrado un ingreso no exitoso, el dia: {fecha_hora_formateada}"
            send_message.send_message(message)
            info = {
                "error": "No se encontro un rostro en la imagen",
                "cantidadRostros": 0
            }
            return info
        
            
