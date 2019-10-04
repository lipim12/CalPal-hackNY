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
    objects = client.object_localization(image=image).localized_object_annotations

#     labels = response.label_annotations
    return objects[0].name
