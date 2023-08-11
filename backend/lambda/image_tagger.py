import os
import boto3
import base64
import json

client = boto3.client('rekognition')

def handler(event, context):
    image_data = event['body']
    
    # Decode the base64 string
    source_bytes = base64.b64decode(image_data)

    detect_objects = client.detect_labels(Image={'Bytes': source_bytes})
    labels = [i["Name"] for i in detect_objects["Labels"]]

    # TODO Hay que hacer que la función refine_data funcione. Haz una stack tuya, recuerda cambiar la URL del frontend hacia el que sea tu backend
    # TODO empaquetar la función lambda para que puedas utilizar el api de OPEN AI
    def refine_data(list_items):
        print(list_items)

    refine_data(labels)

    return {
        'statusCode': 200,
        'body': json.dumps(labels)
    }
