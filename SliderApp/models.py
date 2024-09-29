from django.db import models
import requests

import os
from django_resized import ResizedImageField
from base.base import SerializedModel



def upload_slider(instance, filename):
    return 'image/slider/{filename}'.format(filename=filename)
# def sliderPath(instance, filename):
#     # Perform the API call to upload the image
#     url = "http://schoolproject-env.eba-ah3mewj2.ap-southeast-1.elasticbeanstalk.com/api/file"
#     files = {"file": instance.sliderImage.file}
#     response = requests.post(url, files=files)
#     ret = "null"

#     if response.status_code == 200:
#         api_response = response.json()
#         image_key = api_response.get("key", None)

#         if image_key:
#             # Extract the filename from the image_key
#             filename = os.path.basename(image_key)

#             # Create the directory if it doesn't exist
#             directory = "image/slider/"
#             os.makedirs(directory, exist_ok=True)

#             # Save the image locally using the extracted filename
#             local_image_path = os.path.join(directory, filename)
#             with open(local_image_path, "wb") as f:
#                 f.write(files["file"].read())

#             # Set the image_url field to the image_key value
#             instance.image_url = image_key

#     # If the API call fails or no key is returned, return a default path or handle the error as needed
#     return ret


class SliderModel(models.Model,SerializedModel):
    id = models.AutoField(primary_key=True)
    title= models.CharField(max_length= 300,blank = False)
    # sliderImage= models.ImageField(upload_to=sliderPath, blank=True, null=True)
    # image_first = ResizedImageField(upload_to=upload_to2)

    sliderImage= ResizedImageField(upload_to=upload_slider, blank=True, null=True)
    active= models.CharField(max_length= 300,blank = False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)
    image_url = models.CharField(max_length=300, blank=True, null=True)
    def __str__(self):
        return str(self.title) + str(self.active)

