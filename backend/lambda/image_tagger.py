import os
import boto3
import base64
import json
import openai

openai.api_key = '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'
client = boto3.client('rekognition')

def refine_data(tag_list):
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You exclusively return a list of words. You are a image tag enhancer. Your job consists in refining the tags a computer vision system returns. All the images tha computer vision system was fed consist on photos from a chain of hotels spread all over Mexico. Your main focus is always to rewrite tags thinking of the hotel. Also you will have to return said list of words in mexican spanish."},
        {"role": "user", "content": f"{tag_list}  Be specific. Don't use words as cutlery or spoon. Rather if you see spoon try to infer soup."}
        ])

    return completion.choices[0].message.get("content")

def handler(event, context):
    image_data = event['body']
    
    # Decode the base64 string
    source_bytes = base64.b64decode(image_data)

    detect_objects = client.detect_labels(Image={'Bytes': source_bytes})
    labels = [i["Name"] for i in detect_objects["Labels"]]

    refined_labels = refine_data(labels)

    return {
        'statusCode': 200,
        'body': json.dumps(refined_labels)
    }
