
from flask import render_template,send_file

from flask import Flask, jsonify, request
import json
import requests
from pydub import AudioSegment
from pydub.playback import play
from flask import render_template

app = Flask(__name__)

@app.route("/webhook", methods=["GET"])
def home():
  if request.method == "GET":
        print("verifico1")
        print(request)
        #SI EL TOKEN ES IGUAL AL QUE RECIBIMOS
        print(request.args.get('hub.verify_token'))
        if request.args.get('hub.verify_token') == "gtic12345":
            #ESCRIBIMOS EN EL NAVEGADOR EL VALOR DEL RETO RECIBIDO DESDE FACEBOOK
            print("verifico2")
            return request.args.get('hub.challenge')
        else:
            #SI NO SON IGUALES RETORNAMOS UN MENSAJE DE ERROR
            print("mal")
            return "Error de autentificacion."


#CUANDO RECIBAMOS LAS PETICIONES EN ESTA RUTA
@app.route("/webhook", methods=["POST"])
def webhook_whatsapp():
    
    if request.get_json():
        data=request.get_json()
        if 'entry' in data and len(data['entry']) > 0 and 'changes' in data['entry'][0] and len(data['entry'][0]['changes']) > 0 and 'value' in data['entry'][0]['changes'][0] and 'messages' in data['entry'][0]['changes'][0]['value'] and len(data['entry'][0]['changes'][0]['value']['messages']) > 0 and 'audio' in data['entry'][0]['changes'][0]['value'][0]['messages'][0] :
            #RECIBIMOS TODOS LOS DATOS ENVIADO VIA JSON
            #EXTRAEMOS EL NUMERO DE TELEFONO Y EL MANSAJE
            telefonoCliente=data['entry'][0]['changes'][0]['value']['messages'][0]['from']
            #EXTRAEMOS EL TELEFONO DEL CLIENTE
            # mensaje=data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
            #EXTRAEMOS EL ID DE WHATSAPP DEL ARRAY
            idWA=data['entry'][0]['changes'][0]['value']['messages'][0]['id']
            #EXTRAEMOS EL TIEMPO DE WHATSAPP DEL ARRAY
            timestamp=data['entry'][0]['changes'][0]['value']['messages'][0]['timestamp']
            #ESCRIBIMOS EL NUMERO DE TELEFONO Y EL MENSAJE EN EL ARCHIVO TEXTO
            media_id=data['entry'][0]['changes'][0]['value']['messages'][0]['audio']['id']
            
            # URL de la API de WhatsApp Business
            urlMediaID = "https://graph.facebook.com/v16.0/" + media_id + "/"
            # Parámetros de autenticación
            token = 'EAAIIou6kHEkBAOwVxmZBBqjDiLgcieekDE2IaCQa4xY2aPYsF3ikSec9jbuTZAjL38u6E3IlcZAqWZBItZCZBRUJT1OHgQSn0BBbpKUL5dJzr6G4BKgZBSZBjec0uPMZAZAO3ZAICJ2MVkPbDtkiHB8czLFxXHKVEYN4V7OG21SjiYoS01PjrZBsvvWSGZAJVloGE07kKD1yRuFEmCwZDZD'
            # Headers para la autenticación
            headers = {
                'Authorization': 'Bearer ' + token,
                'Content-Type': 'application/json'
            }

            # Enviar la solicitud POST a la API
            responseMediaID = requests.get(urlMediaID, headers=headers)
            # Verificar el código de respuesta
            if responseMediaID.status_code == 200:
                data=responseMediaID.json()
                urlAudio = data['url']
                name_audio="temp_audio.mp3"
                responseAudio = requests.get(urlAudio, headers=headers)
                with open(name_audio, "wb") as file:
                  file.write(responseAudio.content)
                
                #         audio = AudioSegment.from_ogg(name_audio)

                #         # Exportar como archivo .mp3
                #         new_audio="audio.mp3"
                #         audio.export(new_audio, format='mp3')
            else:
                print('Error al realizar la peticion:')   
        return jsonify({"status": "success"}, 200)
    else:
        return jsonify({"status": "failed"}, 404)

  
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/audio')
def audio():
    # Ruta del archivo de audio
    audio_file = 'temp_audio.mp3'
    return send_file(audio_file)
  
@app.route('/sendimage')
def sendImage():
    # URL de la API de WhatsApp Business
    url = 'https://graph.facebook.com/v16.0/117162651379322/messages'

    # Parámetros de autenticación
    token = 'EAAIIou6kHEkBAOwVxmZBBqjDiLgcieekDE2IaCQa4xY2aPYsF3ikSec9jbuTZAjL38u6E3IlcZAqWZBItZCZBRUJT1OHgQSn0BBbpKUL5dJzr6G4BKgZBSZBjec0uPMZAZAO3ZAICJ2MVkPbDtkiHB8czLFxXHKVEYN4V7OG21SjiYoS01PjrZBsvvWSGZAJVloGE07kKD1yRuFEmCwZDZD'

    # Datos del mensaje
    telefono_destino = '593939889081'

    # Crear el payload del mensaje
    payload = {
        "messaging_product": "whatsapp",
        "to": telefono_destino,
        "type": "image",
        "image": {
            "link": "https://res.cloudinary.com/dwfhulxhj/image/upload/v1684527286/vz5odsfoq6kc9lagxlhv.jpg"
        }
    }

    # Headers para la autenticación
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }

    # Enviar la solicitud POST a la API
    response = requests.post(url, data=json.dumps(payload), headers=headers)

    # Verificar el código de respuesta
    if response.status_code == 200:
        print('Mensaje enviado exitosamente.')
    else:
        print('Error al enviar el mensaje:', response.text)
    return jsonify({"status": "success"}, 200)  

@app.route('/sendfile')
def sendFile():


    # URL de la API de WhatsApp Business
    url = 'https://graph.facebook.com/v16.0/117162651379322/messages'

    # Parámetros de autenticación
    token = 'EAAIIou6kHEkBAOwVxmZBBqjDiLgcieekDE2IaCQa4xY2aPYsF3ikSec9jbuTZAjL38u6E3IlcZAqWZBItZCZBRUJT1OHgQSn0BBbpKUL5dJzr6G4BKgZBSZBjec0uPMZAZAO3ZAICJ2MVkPbDtkiHB8czLFxXHKVEYN4V7OG21SjiYoS01PjrZBsvvWSGZAJVloGE07kKD1yRuFEmCwZDZD'

    # Datos del mensaje
    telefono_destino = '593939889081'


    # Crear el payload del mensaje
    payload = {
        "messaging_product": "whatsapp",
        "to": telefono_destino,
        "type": "document",
        "document": {
            "link": "https://www.irjmets.com/uploadedfiles/paper/volume2/issue_8_august_2020/3180/1628083124.pdf",
            "caption": "Documento"
        }
    }

    # Headers para la autenticación
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }

    # Enviar la solicitud POST a la API
    response = requests.post(url, data=json.dumps(payload), headers=headers)

    # Verificar el código de respuesta
    if response.status_code == 200:
        print('Mensaje enviado exitosamente.')
    else:
        print('Error al enviar el mensaje:', response.text)

    return jsonify({"status": "success"}, 200)
  
@app.route('/sendaudio')
def sendAudio():


    # URL de la API de WhatsApp Business
    url = 'https://graph.facebook.com/v16.0/117162651379322/messages'

    # Parámetros de autenticación
    token = 'EAAIIou6kHEkBAOwVxmZBBqjDiLgcieekDE2IaCQa4xY2aPYsF3ikSec9jbuTZAjL38u6E3IlcZAqWZBItZCZBRUJT1OHgQSn0BBbpKUL5dJzr6G4BKgZBSZBjec0uPMZAZAO3ZAICJ2MVkPbDtkiHB8czLFxXHKVEYN4V7OG21SjiYoS01PjrZBsvvWSGZAJVloGE07kKD1yRuFEmCwZDZD'

    # Datos del mensaje
    telefono_destino = '593939889081'
    mensaje = 'Hola, este es un mensaje enviado desde Python utilizando la API de WhatsApp'

    # Crear el payload del mensaje
    payload = {
        "messaging_product": "whatsapp",
        "to": '593939889081',
        "type": "image",
        "type": "audio",
        "audio": {
            "link": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
        }
    }

    # Headers para la autenticación
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }

    # Enviar la solicitud POST a la API
    response = requests.post(url, data=json.dumps(payload), headers=headers)

    # Verificar el código de respuesta
    if response.status_code == 200:
        print('Mensaje enviado exitosamente.')
    else:
        print('Error al enviar el mensaje:', response.text)

    return jsonify({"status": "success"}, 200)

#INICIAMSO FLASK
if __name__ == "__main__":
  app.run(debug=True)

