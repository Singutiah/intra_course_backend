from django.forms import model_to_dict
from rest_framework import serializers

from .models import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"
        #fields = ["id", "course_code", "name", "years", "sem_count", "category"]

    # def update(self, instance, validated_data):
    #     instance.course_code = validated_data.get("course_code", instance.course_code)
    #     instance.name = validated_data.get("name", instance.name)
    #     instance.years = validated_data.get("years", instance.years)
    #     instance.sem_count = validated_data.get("sem_count", instance.sem_count)
    #
    #     instance.save()
    #     return instance



