from django.db.models import Prefetch, Subquery, OuterRef
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import status

from .chat_nlp import chatbot
from .decorators import validate_request_data, validate_intent_data, validate_weight_data
from .models import Chats, TrainingData, Tags, Patterns, Responses, Weight
from .serializers import ChatsSerializer, TrainingDataSerializer, TagsSerializer, PatternsSerializer, \
    ResponsesSerializer, WeightSerializer

import sys
sys.path.append("..")

from courses.models import Course
from students.models import Student
from courses.serializers import CourseSerializer
from students.serializers import StudentSerializer



def _get_tags_by_category(course_category):
    all_category_courses = Course.objects.filter(category=course_category)
    cw = []
    for course in all_category_courses:
        # c.append(courseSerializer(course).data)
        course_weights = Weight.objects.filter(course=course)
        # print('course_weights', course_weights)
        cw.extend(WeightSerializer(course_weights, many=True).data)

    all_weight_responses = set([item.get('response') for item in cw if item.get('value')>7])
    # print("all_weight_responses", all_weight_responses)
    my_tags = [TagsSerializer(Tags.objects.get(id=Responses.objects.get(id=i).tag.id)).data for i in all_weight_responses]
    return (my_tags)

def get_tags_by_category(course_category):
    all_category_courses = Course.objects.filter(category=course_category)
    # print("all_category_courses", all_category_courses)
    cw = []
    for course in all_category_courses:
        # c.append(courseSerializer(course).data)
        print("course", course)
        course_weights = Weight.objects.filter(course=course)
        print('course_weights', course_weights)
        cw.extend(WeightSerializer(course_weights, many=True).data)

    # print("weights belonging to this category", cw)
    all_weight_responses = set([item.get('response') for item in cw if item.get('value') > 6])
    # print("all_weight_responses", all_weight_responses)
    my_tags = [TagsSerializer(Tags.objects.get(id=Responses.objects.get(id=i).tag.id)).data for i in all_weight_responses]
    # print('my_tags', my_tags)
    return (my_tags)
    # responses_object = Responses.objects.get(id=weight_response)
    #
    # print(responses_object)
    # temp.append(TagsSerializer(ResponsesSerializer(responses_object).data['tag']).data)
    # course_object = course.objects.get(id=weight_course)
    # course_data = CourseSerializer(course_object).data
    # print("course_data", course_data)
    # course_category = course_data["category"]
    #
    # all_category_courses = course.objects.filter(category=course_category)
    # c = []
    # for course in all_category_courses:
    #     c.append(courseSerializer(course).data)
    #     _weights = Weight.objects.filter(course=course)
    # print("courses in category", c)
class ListCreateAskView(generics.ListCreateAPIView):
    """
        GET Chats/
        POST Chats/
        """

    queryset = Chats.objects.all()
    serializer_class = ChatsSerializer
    permission_classes = (permissions.IsAuthenticated,)


    def post(self, request, *args, **kwargs):
        # tag_instance = Chats.objects.get()
        # a_pattern = ChatsSerializer.objects.create(
        #     name=request.data["name"]
        # )
        # Test the chatbot

        tags = Tags.objects.prefetch_related(
            Prefetch('patterns_set', queryset=Patterns.objects.annotate(
                pattern_name=Subquery(Patterns.objects.filter(id=OuterRef('id')).values('name')))),
            Prefetch('responses_set', queryset=Responses.objects.annotate(
                response_name=Subquery(Responses.objects.filter(id=OuterRef('id')).values('name')))),
        )

        intents = {}
        for tag in tags:
            patterns = [pattern.name for pattern in tag.patterns_set.all()]
            responses = [response.name for response in tag.responses_set.all()]


            # serialized_tags.append({
            #     'tags': {"name": tag.name, "id": tag.id},
            #     'patterns': patterns,
            #     'responses': responses,
            # })
            intents[f"{tag.name}"] = {
                'patterns': patterns,
                'responses': responses,
            }

        # print(intents)



        # return serialized_tags

        # serializer_class = TrainingDataSerializer
        # Define a few sample inputs and responses
        # intents = {
        #     "greet": {
        #         "patterns": ["hello", "hi", "hey"],
        #         "responses": ["Hello!", "Hi there!", "Hey!"]
        #     },
        #     "goodbye": {
        #         "patterns": ["bye", "goodbye", "see you later"],
        #         "responses": ["Goodbye!", "See you later!", "Bye!"]
        #     },
        #     "airport": {
        #         "patterns": ["airport", "flight", "airline"],
        #         "responses": ["I'm sorry, I can't help with that."]
        #     }
        # }
        quiz = str(request.data["name"]).replace("?", "")
        res = (chatbot(intents, quiz))
        return Response(
            data=res,
            status=status.HTTP_201_CREATED
        )
class ListCreateTrainingDataView(generics.ListCreateAPIView):
    """
    GET Td/
    POST Td/
    """
    def get_queryset(self):
        tags = Tags.objects.prefetch_related(
            Prefetch('patterns_set', queryset=Patterns.objects.annotate(
                pattern_name=Subquery(Patterns.objects.filter(id=OuterRef('id')).values('name')))),
            Prefetch('responses_set', queryset=Responses.objects.annotate(
                response_name=Subquery(Responses.objects.filter(id=OuterRef('id')).values('name')))),
        )

        serialized_tags = []
        for tag in tags:
            patterns = [{'name': pattern.name, 'id': pattern.id} for pattern in
                        tag.patterns_set.all()]
            responses = [{'name': response.name, 'id': response.id} for response in
                         tag.responses_set.all()]
            serialized_tags.append({
                'tags': {"name": tag.name, "id": tag.id},
                'patterns': patterns,
                'responses': responses,
            })

        for i in serialized_tags:
            print(i)

        return serialized_tags

    serializer_class = TrainingDataSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @validate_intent_data
    def post(self, request, *args, **kwargs):
        intents = request.data
        tag = intents["Tag"]
        patterns = intents["Patterns"]
        responses = intents["Responses"]
        inp = {
                'tags': {"name": tag["name"], "id": tag["id"]},
                'patterns': patterns,
                'responses': responses
            }
        s = TrainingDataSerializer(data=inp)
        if s.is_valid():
            s.save()
        return Response(
            data="success",
            status=status.HTTP_201_CREATED
        )




class ListCreateTrainingDataView1(generics.ListCreateAPIView):
    """
    GET Td/
    POST Td/
    """
    def get_queryset(self):
        tags = Tags.objects.prefetch_related(
            Prefetch('patterns_set', queryset=Patterns.objects.annotate(
                pattern_name=Subquery(Patterns.objects.filter(id=OuterRef('id')).values('name')))),
            Prefetch('responses_set', queryset=Responses.objects.annotate(
                response_name=Subquery(Responses.objects.filter(id=OuterRef('id')).values('name')))),
        )

        serialized_tags = []

        for tag in tags:
            patterns = [{'name': pattern.name, 'id': pattern.id} for pattern in
                        tag.patterns_set.all()]
            responses = [{'name': response.name, 'id': response.id} for response in
                         tag.responses_set.all()]
            serialized_tags.append({
                'tags': {"name": tag.name, "id": tag.id},
                'patterns': patterns,
                'responses': responses,
            })

        for i in serialized_tags:
            print(i)

        return serialized_tags

    serializer_class = TrainingDataSerializer
    permission_classes = (permissions.IsAuthenticated,)


    def post(self, request, *args, **kwargs):
        user = request.data['user']
        student_subjects = StudentSubject.objects.filter(user=user)
        student_subjects_data = StudentSubjectSerializer(student_subjects, many=True).data
        # print("my_subjects", student_subjects)

        subject_weights = SubjectWeight.objects.all()
        subject_weights_data = SubjectWeightSerializer(subject_weights, many=True).data

        # print("subject_weights_data", subject_weights_data)
        my_student_subject_weights = []
        for subject in student_subjects_data:
            f = [item for item in subject_weights_data if item.get('subject') == subject.get('subject') and item.get('value')>7]
            # f = subject_weights_data.filter(lambda x: x[subject]==subject[id])
            my_student_subject_weights.extend(f)

        # print("my_student_subject_weights", my_student_subject_weights)

        preferred_courses = set([item.get('course') for item in my_student_subject_weights])

        # print("preferred_courses", preferred_courses)
        preferred_categories = set([Course.objects.get(id=item).category for item in preferred_courses])
        # print("preferred_categories", preferred_categories)
        print(get_tags_by_category("Medicine"))
        my_tags = []
        for cat in preferred_categories:
            my_tags.extend(get_tags_by_category(cat))


        tags = Tags.objects.prefetch_related(
            Prefetch('patterns_set', queryset=Patterns.objects.annotate(
                pattern_name=Subquery(Patterns.objects.filter(id=OuterRef('id')).values('name')))),
            Prefetch('responses_set', queryset=Responses.objects.annotate(
                response_name=Subquery(Responses.objects.filter(id=OuterRef('id')).values('name')))),
        )

        serialized_tags = []


        for tag in tags:
            # [print(x['id']) for x in my_tags]
            _taglist = (list(filter(lambda x: x['id'] == tag.id, my_tags)))
            if len(_taglist):
                patterns = [{'name': pattern.name, 'id': pattern.id} for pattern in
                            tag.patterns_set.all()]
                responses = [{'name': response.name, 'id': response.id} for response in
                             tag.responses_set.all()]
                serialized_tags.append({
                    'tags': {"name": tag.name, "id": tag.id},
                    'patterns': patterns,
                    'responses': responses,
                })

        # print(tags)
        permission_classes = (permissions.IsAuthenticated,)
        return Response(TrainingDataSerializer(serialized_tags, many=True).data)
        # return Response(
        #     data="success",
        #     status=status.HTTP_201_CREATED
        # )

class ListCreateTagsView(generics.ListCreateAPIView):
    """
    GET Chats/
    POST Chats/
    """
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @validate_request_data
    def post(self, request, *args, **kwargs):
        a_tag = Tags.objects.create(
            name=request.data["name"]
        )
        return Response(
            data=TagsSerializer(a_tag).data,
            status=status.HTTP_201_CREATED
        )


class ListCreatePatternsView(generics.ListCreateAPIView):
    """
    GET Chats/
    POST Chats/
    """

    queryset = Patterns.objects.all().select_related('tag').values('id', 'name', 'tag')
    serializer_class = PatternsSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @validate_request_data
    def post(self, request, *args, **kwargs):
        tag_instance = Tags.objects.get(id=request.data["tag"])
        a_pattern = Patterns.objects.create(
            name=request.data["name"],
            tag=tag_instance
        )
        return Response(
            data=TagsSerializer(a_pattern).data,
            status=status.HTTP_201_CREATED
        )


class ListCreateResponsesView(generics.ListCreateAPIView):
    """
    GET Chats/
    POST Chats/
    """

    queryset = Responses.objects.all().select_related('tag').values('id', 'name', 'tag')
    serializer_class = ResponsesSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @validate_request_data
    def post(self, request, *args, **kwargs):
        tag_instance = Tags.objects.get(id=request.data["tag"])

        a_response = Responses.objects.create(
            name=request.data["name"],
            tag=tag_instance,
        )
        return Response(
            data=TagsSerializer(a_response).data,
            status=status.HTTP_201_CREATED
        )


class ListCreateChatsView(generics.ListCreateAPIView):
    """
    GET Chats/
    POST Chats/
    """
    queryset = Chats.objects.all()
    serializer_class = ChatsSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @validate_request_data
    def post(self, request, *args, **kwargs):
        a_song = Chats.objects.create(
            title=request.data["title"],
            artist=request.data["artist"]
        )
        return Response(
            data=ChatsSerializer(a_song).data,
            status=status.HTTP_201_CREATED
        )


class PatternsDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET Chats/:id/
    PUT Chats/:id/
    DELETE Chats/:id/
    """
    queryset = Patterns.objects.all()
    serializer_class = PatternsSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            a_pattern = self.queryset.get(pk=kwargs["pk"])
            return Response(TagsSerializer(a_pattern).data)
        except Tags.DoesNotExist:
            return Response(
                data={
                    "message": "Pattern with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    @validate_request_data
    def put(self, request, *args, **kwargs):
        try:
            a_pattern = self.queryset.get(pk=kwargs["pk"])
            serializer = TagsSerializer()
            updated_pattern = serializer.update(a_pattern, request.data)
            return Response(PatternsSerializer(updated_pattern).data)
        except Patterns.DoesNotExist:
            return Response(
                data={
                    "message": "Pattern with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            a_pattern = self.queryset.get(pk=kwargs["pk"])
            a_pattern.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Patterns.DoesNotExist:
            return Response(
                data={
                    "message": "Pattern with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )


class TrainingDataDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET Td/:id/
    PUT Td/:id/
    DELETE Td/:id/
    """
    queryset = Tags.objects.all()
    serializer_class = TrainingDataSerializer
    permission_classes = (permissions.IsAuthenticated,)


    def get(self, request, *args, **kwargs):
        try:
            tags = Tags.objects.filter(id=kwargs["pk"]).prefetch_related(
                Prefetch('patterns_set', queryset=Patterns.objects.annotate(
                    pattern_name=Subquery(Patterns.objects.filter(id=OuterRef('id')).values('name')))),
                Prefetch('responses_set', queryset=Responses.objects.annotate(
                    response_name=Subquery(Responses.objects.filter(id=OuterRef('id')).values('name')))),
            )



            serialized_tags = []


            for tag in tags:
                patterns = [{'name': pattern.name, 'id': pattern.id} for pattern in
                            tag.patterns_set.all()]
                responses = [{'name': response.name, 'id': response.id} for response in
                             tag.responses_set.all()]

                serialized_tags.append({
                    'tags': {"name": tag.name, "id": tag.id},
                    'patterns': patterns,
                    'responses': responses,
                })

            permission_classes = (permissions.IsAuthenticated,)
            return Response(TrainingDataSerializer(serialized_tags[0]).data)

        except Tags.DoesNotExist:
            return Response(
                data={
                    "message": "Tag with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )


    @validate_intent_data
    def put(self, request, *args, **kwargs):
        try:
            tag = Tags.objects.prefetch_related(
                Prefetch('patterns_set', queryset=Patterns.objects.annotate(
                    pattern_name=Subquery(Patterns.objects.filter(id=OuterRef('id')).values('name')))),
                Prefetch('responses_set', queryset=Responses.objects.annotate(
                    response_name=Subquery(Responses.objects.filter(id=OuterRef('id')).values('name')))),
            ).get(id=kwargs["pk"])

            serialized_tags = []

            patterns = [{'name': pattern.name, 'id': pattern.id} for pattern in
                        tag.patterns_set.all()]
            responses = [{'name': response.name, 'id': response.id} for response in
                         tag.responses_set.all()]
            serialized_tags.append({
                'tags': {"name": tag.name, "id": tag.id},
                'patterns': patterns,
                'responses': responses,
            })
            serializer = TrainingDataSerializer()
            updated_data = serializer.update(serialized_tags[0], request.data)
            return Response(TrainingDataSerializer(updated_data).data)
        except TrainingData.DoesNotExist:
            return Response(
                data={
                    "message": "Training data with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            a_tag = self.queryset.get(pk=kwargs["pk"])
            a_tag.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Tags.DoesNotExist:
            return Response(
                data={
                    "message": "Tag with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

class ResponsesDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET Chats/:id/
    PUT Chats/:id/
    DELETE Chats/:id/
    """
    queryset = Responses.objects.all()
    serializer_class = ResponsesSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            a_response = self.queryset.get(pk=kwargs["pk"])
            return Response(TagsSerializer(a_response).data)
        except Responses.DoesNotExist:
            return Response(
                data={
                    "message": "Response with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    @validate_request_data
    def put(self, request, *args, **kwargs):
        try:
            a_response = self.queryset.get(pk=kwargs["pk"])
            serializer = ResponsesSerializer()
            updated_response = serializer.update(a_response, request.data)
            return Response(TagsSerializer(updated_response).data)
        except Responses.DoesNotExist:
            return Response(
                data={
                    "message": "Pattern with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            a_response = self.queryset.get(pk=kwargs["pk"])
            a_response.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Responses.DoesNotExist:
            return Response(
                data={
                    "message": "Pattern with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )


class TagsDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET Chats/:id/
    PUT Chats/:id/
    DELETE Chats/:id/
    """
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            a_tag = self.queryset.get(pk=kwargs["pk"])
            return Response(TagsSerializer(a_tag).data)
        except Tags.DoesNotExist:
            return Response(
                data={
                    "message": "Tag with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    @validate_request_data
    def put(self, request, *args, **kwargs):
        try:
            a_tag = self.queryset.get(pk=kwargs["pk"])
            serializer = TagsSerializer()
            updated_song = serializer.update(a_tag, request.data)
            return Response(TagsSerializer(updated_song).data)
        except Tags.DoesNotExist:
            return Response(
                data={
                    "message": "Tag with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            a_tag = self.queryset.get(pk=kwargs["pk"])
            a_tag.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Tags.DoesNotExist:
            return Response(
                data={
                    "message": "Tag with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )


class ChatsDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET Chats/:id/
    PUT Chats/:id/
    DELETE Chats/:id/
    """
    queryset = Chats.objects.all()
    serializer_class = ChatsSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            a_song = self.queryset.get(pk=kwargs["pk"])
            return Response(ChatsSerializer(a_song).data)
        except Chats.DoesNotExist:
            return Response(
                data={
                    "message": "Song with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    @validate_request_data
    def put(self, request, *args, **kwargs):
        try:
            a_song = self.queryset.get(pk=kwargs["pk"])
            serializer = ChatsSerializer()
            updated_song = serializer.update(a_song, request.data)
            return Response(ChatsSerializer(updated_song).data)
        except Chats.DoesNotExist:
            return Response(
                data={
                    "message": "Song with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            a_song = self.queryset.get(pk=kwargs["pk"])
            a_song.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Chats.DoesNotExist:
            return Response(
                data={
                    "message": "Song with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )


class ListCreateWeightView(generics.ListCreateAPIView):
    """
    GET Chats/
    POST Chats/
    """

    queryset = Weight.objects.all()
    serializer_class = WeightSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @validate_request_data
    def post(self, request, *args, **kwargs):
        course_instance = Course.objects.get(id=request.data["course"])
        response_instance = Responses.objects.get(id=request.data["response"])
        a_Weight = Weight.objects.create(
            name=request.data["value"],
            course=course_instance,
            response=response_instance
        )
        return Response(
            data=WeightSerializer(a_Weight).data,
            status=status.HTTP_201_CREATED
        )


class WeightDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET Chats/:id/
    PUT Chats/:id/
    DELETE Chats/:id/
    """
    queryset = Weight.objects.all()
    serializer_class = WeightSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            a_Weight = self.queryset.get(pk=kwargs["pk"])
            return Response(WeightSerializer(a_Weight).data)
        except Tags.DoesNotExist:
            return Response(
                data={
                    "message": "Weight with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    @validate_weight_data
    def put(self, request, *args, **kwargs):
        try:
            a_Weight = self.queryset.get(pk=kwargs["pk"])
            serializer = TagsSerializer()
            updated_Weight = serializer.update(a_Weight, request.data)
            return Response(WeightSerializer(updated_Weight).data)
        except Weight.DoesNotExist:
            return Response(
                data={
                    "message": "Weight with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            a_Weight = self.queryset.get(pk=kwargs["pk"])
            a_Weight.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Weight.DoesNotExist:
            return Response(
                data={
                    "message": "Weight with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )


class WeightReponseDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET Chats/:id/
    PUT Chats/:id/
    DELETE Chats/:id/
    """
    queryset = Weight.objects.all()
    serializer_class = WeightSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            response_instance = Responses.objects.get(id=kwargs["pk"])
            a_Weight = Weight.objects.all()
            temp = []
            r = ResponsesSerializer(response_instance).data

            for i in a_Weight:
                dt = WeightSerializer(i).data
                mv = CourseSerializer(Course.objects.get(id=dt["course"])).data
                if (dt["value"]):
                    temp.append({
                        # "response": r,
                        "course": mv,
                        # "tag": TagsSerializer(Tags.objects.get(id=r["tag"])).data,
                        "id": dt["id"],
                        "value": dt["value"]
                    })

                print(temp)

            return Response(
                data=temp,
                status=status.HTTP_200_OK
            )
        except Tags.DoesNotExist:
            return Response(
                data={
                    "message": "Weight with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    @validate_weight_data
    def put(self, request, *args, **kwargs):
        try:
            a_Weight = self.queryset.get(pk=kwargs["pk"])
            serializer = TagsSerializer()
            updated_Weight = serializer.update(a_Weight, request.data)
            return Response(WeightSerializer(updated_Weight).data)
        except Weight.DoesNotExist:
            return Response(
                data={
                    "message": "Weight with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            a_Weight = self.queryset.get(pk=kwargs["pk"])
            a_Weight.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Weight.DoesNotExist:
            return Response(
                data={
                    "message": "Weight with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )
