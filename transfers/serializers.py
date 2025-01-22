from django.forms import model_to_dict
from rest_framework import serializers

from .models import Transfer

import sys
sys.path.append("..")

from chatbot.serializers import ResponsesSerializer
from courses.serializers import CourseSerializer


class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = "__all__"
        image = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)
        # certificate = serializers.FileField(max_length=None, use_url=True, allow_null=True, required=False)
        # fields = ["id", "index", "lastname", "firstname", "middlename", "password", "course", "email"]

    def update(self, instance, validated_data):
        instance.course = validated_data.get("course", instance.course)
        instance.images = validated_data.get("images", instance.images)

        instance.save()
        return instance

