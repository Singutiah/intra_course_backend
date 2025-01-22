from django.db import models
from django.contrib.auth.models import User
from chatbot.models import Responses
import os
from courses.models import Course


def upload_to_images(instance, filename):
    # Define the directory where the image will be uploaded
    upload_directory = "static/images"

    # Get the filename extension from the uploaded file
    # extension = os.path.splitext(filename)[1]

    # Construct the final path using the model's primary key and the filename
    # print(f"instance: {instance.pk}")
    # print(f"extension: {extension}")
    final_filename = f"{filename}"
    return os.path.join(upload_directory, final_filename)


def upload_to_files(instance, filename):
    # Define the directory where the image will be uploaded
    upload_directory = "static/files"

    # Get the filename extension from the uploaded file
    # extension = os.path.splitext(filename)[1]

    # Construct the final path using the model's primary key and the filename
    # print(f"instance: {instance.pk}")
    # print(f"extension: {extension}")
    final_filename = f"{filename}"
    return os.path.join(upload_directory, final_filename)

class Transfer(models.Model):
    # student
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.CharField(max_length=255, null=True)
    year = models.IntegerField(null=True)
    date= models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    certificate = models.FileField(upload_to=upload_to_files, blank=True)

    def __str__(self):
        return "{} - {} - {}".format(self.user, self.course, self.status)
