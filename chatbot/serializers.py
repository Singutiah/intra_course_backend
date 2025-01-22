from django.forms import model_to_dict
from rest_framework import serializers

from .models import Chats, TrainingData, Tags, Patterns, Responses, Weight

import sys
sys.path.append("..")

from courses.serializers import CourseSerializer



class ChatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chats
        # fields = "__all__"
        fields = ("name", "response")

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.response = validated_data.get("response", instance.response)
        instance.save()
        return instance





class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        # fields = "__all__"
        fields = ["id", "name"]


    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.save()
        return instance


class PatternsSerializer(serializers.ModelSerializer):
    tag = serializers.ReadOnlyField()

    class Meta:
        model = Patterns
        fields = ["id", "name", "tag"]

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.tag = validated_data.get("tag", instance.tag)
        instance.save()
        return instance





class ResponsesSerializer(serializers.ModelSerializer):
    tag = serializers.ReadOnlyField()

    class Meta:
        model = Responses
        tag = TagsSerializer()
        fields = ["id", "name", "tag"]

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.tag = validated_data.get("tag", instance.tag)

        instance.save()
        return instance


class TrainingDataSerializer(serializers.Serializer):
    tags = TagsSerializer()
    patterns = PatternsSerializer(many=True)
    responses = ResponsesSerializer(many=True)

    def create(self, validated_data):
        tags_data = validated_data.pop('tags')
        patterns_data = validated_data.pop('patterns')
        responses_data = validated_data.pop('responses')

        tag_instance = Tags.objects.create(**tags_data)
        tag_dict = TagsSerializer(tag_instance).data

        pattern_instances = [Patterns.objects.create(tag=tag_instance, **pattern_data) for pattern_data in
                             patterns_data]
        response_instances = [Responses.objects.create(tag=tag_instance, **response_data) for response_data in
                              responses_data]

        pattern_serializer = PatternsSerializer(pattern_instances, many=True)
        response_serializer = ResponsesSerializer(response_instances, many=True)

        return {
            'tags': tag_dict,
            'patterns': pattern_serializer.data,
            'responses': response_serializer.data
        }

    def update(self, instance, validated_data):
        tags_data = validated_data.get('Tag')
        patterns_data = validated_data.get('Patterns')
        responses_data = validated_data.get('Responses')

        print(tags_data)
        print(patterns_data)
        print(responses_data)
        tag_instance = Tags.objects.get(id=tags_data["id"])
        tag_item = Tags.objects.get(id=tags_data["id"])
        if tags_data:
            try:
                tag_instance = Tags.objects.get(id=tags_data["id"])
                tag_instance.name = tags_data['name']
                tag_instance.save()
            except Tags.DoesNotExist:
                data = {
                    "id": int(tags_data["id"]),
                    "name": tags_data["name"]
                }
                tag_instance = Tags.objects.create(**data)



        if patterns_data:
            for pattern_data in patterns_data:
                try:
                    pattern_instance = Patterns.objects.get(id=pattern_data['id'])
                    pattern_instance.name = pattern_data['name']
                    pattern_instance.save()
                except Patterns.DoesNotExist:
                    # pattern_instance = Patterns.objects.create(**pattern_data)
                    data = {
                        "id": int(pattern_data["id"]),
                        "name": pattern_data["name"],
                        "tag": tag_item,
                    }
                    pattern_instance = Patterns.objects.create(**data)
        if responses_data:
            for response_data in responses_data:
                try:
                    response_instance = Responses.objects.get(id=response_data['id'])
                    response_instance.name = response_data['name']
                    response_instance.save()
                except Responses.DoesNotExist:
                    data = {
                        "id": int(response_data["id"]),
                        "name": response_data["name"],
                        "tag": tag_item,
                    }
                    response_instance = Responses.objects.create(**data)

        return instance



class WeightSerializer(serializers.ModelSerializer):
    # response = serializers.ReadOnlyField()

    class Meta:
        model = Weight
        response = ResponsesSerializer()
        course = CourseSerializer()
        fields = ["id", "value", "course", "response"]

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.tag = validated_data.get("response", instance.response)
        instance.save()
        return instance



