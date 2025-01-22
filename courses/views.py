from django.db.models import Prefetch, Subquery, OuterRef
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import status

from .models import Course
from .serializers import CourseSerializer
from .decorators import validate_course_data

# Create your views here.


class ListCreateCheckNameView(generics.ListCreateAPIView):
    """
        GET Chats/
        POST Chats/
        """

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (permissions.IsAuthenticated,)


    def post(self, request, *args, **kwargs):
        # tag_instance = Chats.objects.get()
        # a_pattern = ChatsSerializer.objects.create(
        #     name=request.data["name"]
        # )
        # Test the chatbot
        res=Course.objects.filter(TAXPAYERPIN=request.data["TAXPAYERPIN"])
        course = res.first()

        s = CourseSerializer(course)
        return Response(
            data=s.data,
            status=status.HTTP_201_CREATED
        )

class ListCreateCourseView(generics.ListCreateAPIView):
    """
    GET Chats/
    POST Chats/
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @validate_course_data
    def post(self, request, *args, **kwargs):
        a_tag = Course.objects.create(
            course_code=request.data["course_code"],
            name=request.data["name"],
            years=request.data["years"],
            sem_count=request.data["sem_count"],
            category=request.data["category"],

        )
        return Response(
            data=CourseSerializer(a_tag).data,
            status=status.HTTP_201_CREATED
        )



class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET Chats/:id/
    PUT Chats/:id/
    DELETE Chats/:id/
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            a_course = self.queryset.get(pk=kwargs["pk"])
            return Response(CourseSerializer(a_course).data)
        except Course.DoesNotExist:
            return Response(
                data={
                    "message": "Course with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    @validate_course_data
    def put(self, request, *args, **kwargs):
        try:
            a_tag = self.queryset.get(pk=kwargs["pk"])
            serializer = CourseSerializer()
            updated_course = serializer.update(a_tag, request.data)
            return Response(CourseSerializer(updated_course).data)
        except Course.DoesNotExist:
            return Response(
                data={
                    "message": "Course with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            a_course = self.queryset.get(pk=kwargs["pk"])
            a_course.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Course.DoesNotExist:
            return Response(
                data={
                    "message": "Course with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )