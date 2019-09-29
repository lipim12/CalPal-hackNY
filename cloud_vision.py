import json
import base64
from google.cloud import vision
import decimal

def vision_pubsub(image_string):
    """
    Args:
         image_string (string): base64 image from the frontend

    """
    frontend_image = base64.b64decode(image_string)

    client = vision.ImageAnnotatorClient()
    image = vision.types.Image(content=frontend_image)

    response = client.label_detection(image=image)

    labels = response.label_annotations
    return labels[0].description
