import camera
from time import sleep
import machine
import sys,time
import network
import ufirebase as firebase
from machine import Pin, ADC, PWM
import binascii
import utime
import urequests



print("###################### VARIABLES ######################")
#Pin del led de flash
led = machine.Pin(4, machine.Pin.OUT)
servo= PWM(Pin(15), freq = 50)
foto=1

def url_encode(url):
    encoded_chars = []
    for char in url:
        char_code = ord(char)
        if 48 <= char_code <= 57 or 65 <= char_code <= 90 or 97 <= char_code <= 122 or char in '-._~':
            encoded_chars.append(char)
        else:
            encoded_chars.append('%{:02X}'.format(char_code))
    return ''.join(encoded_chars)

def wlan_connect(ssid,pwd):
    print("###################### INICIO CONEXION WIFi ######################\n")
    wlan = network.WLAN(network.STA_IF)
    if not wlan.active() or not wlan.isconnected():
        wlan.active(True)
        wlan.connect(ssid,pwd)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())
    print("###################### FIN CONEXION WIFi ######################\n")
    
    
def load_camera():
    print("###################### INICIO CARGA CAMARA Y TOMA FOTO ######################\n")

    camera.init(0, format=camera.JPEG, fb_location=camera.PSRAM)       
        #Establece el brillo
    camera.brightness(-1)    
        #Orientacion normal
    camera.flip(0)
        #Orientación normal
    camera.mirror (0)
        #Resolución
    camera.framesize(camera.FRAME_QVGA)
        #contraste
    camera.contrast(2)
        #saturacion
    camera.saturation (-2)      
        #calidad
    camera.quality(10)
        # special effects
    camera.speffect(camera.EFFECT_NONE)
        # white balance
    camera.whitebalance(camera.WB_NONE)
        #Enciende flash
    led.value(1)
    sleep (0.5)
        #Captura la imagen
    img = camera.capture()
        #Apaga flash
    led.value(0)
        #desactivar cámara
    camera.deinit()
    print("###################### FIN CARGA CAMARA Y TOMA FOTO ######################\n")
    return img


def img_to_base64(img):
    print("###################### INICIO IMG A BASE64 ######################\n")
    base64_data = binascii.b2a_base64(bytes(img, 'utf-8'))
    print("###################### FIN IMG A BASE64 ######################\n")
    return base64_data

def request_autentication(name_file):
    print("###################### INICO REQUEST AUTENTICATION API ######################\n")
    
    api_url = 'https://autentication-api-iur2bamwma-uc.a.run.app/autentication-process-api' 
    id_param = f"data:image/jpeg;base64,{name_file}"
    param = url_encode(id_param)
    url_request = f"{api_url}?string64file={param}"
   
    response = urequests.get(url_request)
    if response.status_code == 200:
    # Accede a los datos de respuesta en formato JSON
        data = response.json()
        
        if data["cantidadRostros"] > 0:
           print(data)
           movement_servo()
        else:
            print("Usuario no reconocible o imagen borrosa")
        
    else:
        print('Error en la solicitud:', response.status_code)  
    print("###################### FIN REQUEST AUTENTICATION API ######################\n")    

def map_servo(x):
    print("###################### INICIO SERVO MOTOR ######################\n")
    return int((x - 0) * (125 - 25) / (180 - 0) + 25)
    print("###################### FIN SERVO MOTOR ######################\n")
    
def movement_servo():
    bn=1
    angulos = [0, 90]

    print("###################### INICIO GIRO SERVO MOTOR ######################\n")
    while (bn<2): 
        for i  in angulos:
         m= map_servo(i)
         servo.duty(m)
         print("R:{}, A:{}°".format(m,i))
         sleep(5)
         bn+=1
    print("###################### FIN GIRO SERVO MOTOR ######################\n")     

try:
    wlan_connect('linksys','12345678')
    img = load_camera()
    base64 = img_to_base64(img)
    request_autentication(base64.decode('utf-8'))
   

except Exception as err:
    print ("Error= "+str (err))
    sleep (2)