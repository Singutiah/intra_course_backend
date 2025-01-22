from django.db import models

import sys
sys.path.append("..")

from courses.models import Course
class Chats(models.Model):
    # chat
    name = models.CharField(max_length=255, null=False)
    # name of artist or group/band
    response = models.CharField(max_length=255, null=False)

    def __str__(self):
        return "{} - {}".format(self.name, self.response)


class TrainingData(models.Model):
    # chat
    title = models.CharField(max_length=255, null=False)
    # name of artist or group/band
    artist = models.CharField(max_length=255, null=False)

    def __str__(self):
        return "{} - {}".format(self.title, self.artist)


class Tags(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Patterns(models.Model):
    # Tag
    name = models.CharField(max_length=255)
    tag = models.ForeignKey(Tags, on_delete=models.CASCADE)

    def __str__(self):
        return "{} ({})".format(self.name, self.tag)

    def tag_name(self):
        return self.tag.name

    def tag_id(self):
        return self.tag.id


class Responses(models.Model):
    # Tag
    name = models.CharField(max_length=255)
    tag = models.ForeignKey(Tags, on_delete=models.CASCADE)

    def __str__(self):
        return "{} ({})".format(self.name, self.tag)

    def tag_name(self):
        return self.tag.name

    def tag_id(self):
        return self.tag.id


class Weight(models.Model):
    # Tag
    value = models.FloatField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    response = models.ForeignKey(Responses, on_delete=models.CASCADE)

    def __str__(self):
        return "{} . {} . {}".format(self.course, self.value, self.response)

    def response_name(self):
        return self.response.name

    def response_id(self):
        return self.response.id








