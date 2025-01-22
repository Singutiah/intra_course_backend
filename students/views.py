from django.db.models import Prefetch, Subquery, OuterRef
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import status

from .models import Student, StudentCourse
from .serializers import StudentSerializer, StudentCourseSerializer
from .decorators import validate_student_data, validate_subject_data, validate_student_subject_data, \
    validate_student_weight_data, validate_student_weight_data

# Create your views here.
import sys
from django.contrib.auth.models import User

sys.path.append("..")

from chatbot.models import Responses, Patterns
from chatbot.models import Weight, Tags
from chatbot.serializers import WeightSerializer, ResponsesSerializer, PatternsSerializer
from courses.models import Course
from courses.serializers import CourseSerializer
from chatbot.serializers import TagsSerializer
from chatbot.views import _get_tags_by_category

class ListCreateStudentView(generics.ListCreateAPIView):
    """
    GET Chats/
    POST Chats/
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @validate_student_data
    def post(self, request, *args, **kwargs):
        a_tag = Student.objects.create(
            index=request.data["index"],
            lastname=request.data["lastname"],
            firstname=request.data["firstname"],
            middlename=request.data["middlename"],
            password=request.data["password"],
            # school=request.data["school"],
            email=request.data["email"],
        )

        return Response(
            data=StudentSerializer(a_tag).data,
            status=status.HTTP_201_CREATED
        )
    
    def get(self, request, *args, **kwargs):
        students = self.get_queryset()
        serializer = self.get_serializer(students, many=True)

        res=[]
        print((request.user.is_staff))

        # Add additional info to the response
        for student in serializer.data:
            crse=CourseSerializer(Course.objects.get(id=student["course"])).data
            usr=User.objects.get(id=student["user"])
            dt={
                "course_data": crse,
                "user_data": usr.username,
                **student
            }
            res.append(dt)
            

        print(res)
        return Response(data=res, status=status.HTTP_200_OK)


class ListCreateStudentLoginView(generics.ListCreateAPIView):
    """
    GET Chats/
    POST Chats/
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @validate_student_data
    def post(self, request, *args, **kwargs):
        _pass = request.data["password"]
        mail = request.data["email"]
        try:
            a_student = Student.objects.filter(email=mail)

            # print(a_student.filter(lambda a:a.password==_pass))
            auth = False
            single_student = {}

            for i in a_student:
                # print(StudentSerializer(i).data)
                if StudentSerializer(i).data["password"] == _pass:
                    auth = True
                    single_student = StudentSerializer(i).data
            if auth:
                return Response(
                    data=single_student,
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    data={},
                    status=status.HTTP_401_UNAUTHORIZED
                )

        except Student.DoesNotExist:
            return Response(
                data={},
                status=status.HTTP_401_UNAUTHORIZED
            )


class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET Chats/:id/
    PUT Chats/:id/
    DELETE Chats/:id/
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            a_student = self.queryset.get(pk=kwargs["pk"])
            return Response(StudentSerializer(a_student).data)
        except Student.DoesNotExist:
            return Response(
                data={
                    "message": "Student with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    @validate_student_data
    def put(self, request, *args, **kwargs):
        try:
            a_tag = self.queryset.get(pk=kwargs["pk"])
            serializer = StudentSerializer()
            updated_student = serializer.update(a_tag, request.data)
            return Response(StudentSerializer(updated_student).data)
        except Student.DoesNotExist:
            return Response(
                data={
                    "message": "Student with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            a_student = self.queryset.get(pk=kwargs["pk"])
            a_student.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Student.DoesNotExist:
            return Response(
                data={
                    "message": "Student with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )




class ListCreateStudentCourseView(generics.ListCreateAPIView):
    """
    GET Chats/
    POST Chats/
    """
    queryset = StudentCourse.objects.all()
    serializer_class = StudentCourseSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @validate_student_subject_data
    def post(self, request, *args, **kwargs):
        students_data = request.data
        temp = []
        for student_data in students_data:
            temp.append(
                StudentCourseSerializer(StudentCourse.objects.create(
                    user=Student.objects.get(id=student_data["user"]),
                    subject=StudentCourse.objects.get(id=student_data["subject"]),
                    grade=student_data["grade"]
                )).data)
        # a_tag = StudentSubject.objects.create(
        #     user=request.data["user"],
        #     subject=request.data["subject"],
        #     grade=request.data["grade"],
        # )

        return Response(
            data=temp,
            status=status.HTTP_201_CREATED
        )


class StudentCourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET Chats/:id/
    PUT Chats/:id/
    DELETE Chats/:id/
    """
    queryset = StudentCourse.objects.all()
    serializer_class = StudentCourseSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            a_student_subject = self.queryset.filter(user=Student.objects.get(id=kwargs["pk"]))

            #return Response([{'id': item['id'], 'grade': item['grade'],
            #                  'subject': StudentCourseSerializer(Subject.objects.get(id=item['subject'])).data} for item in
            #                 StudentSubjectSerializer(a_student_subject, many=True).data])
        except StudentSubject.DoesNotExist:
            return Response(
                data={
                    "message": "StudentSubject with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    @validate_student_subject_data
    def put(self, request, *args, **kwargs):
        try:
            a_tag = self.queryset.get(pk=kwargs["pk"])
            serializer = StudentSubjectSerializer()
            updated_student_subject = serializer.update(a_tag, request.data)
            return Response(StudentSubjectSerializer(updated_student_subject).data)
        except StudentSubject.DoesNotExist:
            return Response(
                data={
                    "message": "StudentSubject with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            a_student_subject = self.queryset.get(pk=kwargs["pk"])
            a_student_subject.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except StudentSubject.DoesNotExist:
            return Response(
                data={
                    "message": "StudentSubject with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )




