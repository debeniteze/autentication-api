from twilio.rest import Client

def send_message(send_message: str):
# Contenido del mensaje que deseas enviar

    #Configuración de tu cuenta de Twilio
    account_sid = 'AC402c0110e6533197a53a08457da6afb8'
    auth_token = '283664c40ac07a9436dbfd782de0ef6e'
    twilio_phone_number = '+14155238886'

    # Número de teléfono de WhatsApp al que deseas enviar el mensaje
    recipient_phone_number = '+573022618276'
    # Inicialización del cliente de Twilio
    client = Client(account_sid, auth_token)

    # Envío del mensaje
    message = client.messages.create(
        body=send_message,
        from_='whatsapp:' + twilio_phone_number,
        to='whatsapp:' + recipient_phone_number
    )

    print(f'Mensaje enviado. SID: {message.sid}')
