from django.forms import model_to_dict
from rest_framework import serializers

from .models import Student, StudentCourse

import sys
sys.path.append("..")

from chatbot.serializers import ResponsesSerializer
from courses.serializers import CourseSerializer
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"
        # fields = ["id", "index", "lastname", "firstname", "middlename", "password", "course", "email"]

    def update(self, instance, validated_data):
        instance.index = validated_data.get("index", instance.index)
        instance.lastname = validated_data.get("lastname", instance.lastname)
        instance.firstname = validated_data.get("firstname", instance.firstname)
        instance.middlename = validated_data.get("middlename", instance.middlename)
        instance.password = validated_data.get("password", instance.password)
        instance.course = validated_data.get("course", instance.course)
        instance.email = validated_data.get("email", instance.email)

        instance.save()
        return instance


class StudentCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentCourse
        fields = "__all__"
        #fields = ["id", "index", "lastname", "firstname", "middlename", "password", "course", "email"]

    def update(self, instance, validated_data):
        instance.index = validated_data.get("index", instance.index)
        instance.lastname = validated_data.get("lastname", instance.lastname)
        instance.firstname = validated_data.get("firstname", instance.firstname)
        instance.middlename = validated_data.get("middlename", instance.middlename)
        instance.password = validated_data.get("password", instance.password)
        instance.course = validated_data.get("course", instance.course)
        instance.email = validated_data.get("email", instance.email)

        instance.save()
        return instance
