from django.db.models import Prefetch, Subquery, OuterRef
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import status

from .models import Transfer
from .serializers import TransferSerializer
from .decorators import validate_transfer_data

# Create your views here.
import sys


import base64
import os
from django.core.files.base import ContentFile

sys.path.append("..")

from chatbot.models import Responses, Patterns
from chatbot.models import Weight, Tags
from chatbot.serializers import WeightSerializer, ResponsesSerializer, PatternsSerializer
from courses.models import Course
from courses.serializers import CourseSerializer
from chatbot.serializers import TagsSerializer
from chatbot.views import _get_tags_by_category
from django.contrib.auth.models import User

class ListCreateTransferView(generics.ListCreateAPIView):
    """
    GET Chats/
    POST Chats/
    """
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @validate_transfer_data
    def post(self, request, *args, **kwargs):
        print(request.data)
        base64_data = request.data["certificate"]
        header, encoded = base64_data.split(',', 1)

        # Decode the base64 content
        decoded_pdf = base64.b64decode(encoded)


        a_tag = Transfer.objects.create(
            user=request.user,
            status=request.data["status"],
            reason=request.data["reason"],
            year=request.data["year"],
            date=request.data["date"],
            course=Course.objects.get(id=request.data["course"]),
            certificate= ContentFile(decoded_pdf, name="certificate.pdf")
        )


        return Response(
            data=TransferSerializer(a_tag).data,
            status=status.HTTP_201_CREATED
        )
    
    def get(self, request, *args, **kwargs):
        trasfers = self.get_queryset()
        serializer = self.get_serializer(trasfers, many=True)

        res=[]
        print((request.user.is_staff))

        # Add additional info to the response
        for transfer in serializer.data:
            crse=CourseSerializer(Course.objects.get(id=transfer["course"])).data
            full_path = transfer["certificate"]
            _user = User.objects.get(id=transfer["user"]).username
            dt={
                "course_data": crse,
                **transfer,
                "certificate": full_path,
                _user: _user
            }
            res.append(dt)
            

        print(res)
        return Response(data=res, status=status.HTTP_200_OK)


class ListCreateMyTransferView(generics.ListCreateAPIView):
    """
    GET Chats/
    POST Chats/
    """
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @validate_transfer_data
    def post(self, request, *args, **kwargs):
        print(request.data)
        base64_data = request.data["certificate"]
        header, encoded = base64_data.split(',', 1)

        # Decode the base64 content
        decoded_pdf = base64.b64decode(encoded)

        a_tag = Transfer.objects.create(
            user=request.user,
            status=request.data["status"],
            reason=request.data["reason"],
            year=request.data["year"],
            date=request.data["date"],
            course=Course.objects.get(id=request.data["course"]),
            certificate=ContentFile(decoded_pdf, name="certificate.pdf")
        )


        return Response(
            data=TransferSerializer(a_tag).data,
            status=status.HTTP_201_CREATED
        )
    
    def get(self, request, *args, **kwargs):
        trasfers = self.get_queryset()
        serializer = self.get_serializer(trasfers, many=True)


        res=[]
        print((request.user.is_staff))

        # Add additional info to the response
        for transfer in serializer.data:
            full_path = transfer["certificate"]
            crse=CourseSerializer(Course.objects.get(id=transfer["course"])).data

            dt={
                "course_data": crse,
                **transfer,
                "certificate": full_path
            }
            res.append(dt)
            for_user=[i for i in res if i["user"]==request.user.id]
            print(for_user)
            

        print(res)
        return Response(data=for_user, status=status.HTTP_200_OK)



class ListCreateRejectTransferView(generics.ListCreateAPIView):
    """
    GET Chats/
    POST Chats/
    """
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @validate_transfer_data
    def post(self, request, *args, **kwargs):
        print(request.user)
        print(request.data)
        transfer_request = Transfer.objects.get(id=request.data["id"])
        transfer_request.status="Rejected"
        transfer_request.save()



        return Response(
            data=TransferSerializer(transfer_request).data,
            status=status.HTTP_202_ACCEPTED
        )
    
    def get(self, request, *args, **kwargs):
        trasfers = self.get_queryset()
        serializer = self.get_serializer(trasfers, many=True)

        res=[]
        print((request.user.is_staff))

        # Add additional info to the response
        for transfer in serializer.data:
            crse=CourseSerializer(Course.objects.get(id=transfer["course"])).data
            dt={
                "course_data": crse,
                **transfer
            }
            res.append(dt)
            for_user=[i for i in res if i["user"]==request.user.id]
            print(for_user)
            

        print(res)
        return Response(data=for_user, status=status.HTTP_200_OK)



class ListCreateApproveTransferView(generics.ListCreateAPIView):
    """
    GET Chats/
    POST Chats/
    """
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @validate_transfer_data
    def post(self, request, *args, **kwargs):
        print(request.user)
        print(request.data)
        transfer_request = Transfer.objects.get(id=request.data["id"])
        transfer_request.status="approved"
        transfer_request.save()



        return Response(
            data=TransferSerializer(transfer_request).data,
            status=status.HTTP_202_ACCEPTED
        )
    
    def get(self, request, *args, **kwargs):
        trasfers = self.get_queryset()
        serializer = self.get_serializer(trasfers, many=True)

        res=[]
        print((request.user.is_staff))

        # Add additional info to the response
        for transfer in serializer.data:
            crse=CourseSerializer(Course.objects.get(id=transfer["course"])).data
            dt={
                "course_data": crse,
                **transfer
            }
            res.append(dt)
            for_user=[i for i in res if i["user"]==request.user.id]
            print(for_user)
            

        print(res)
        return Response(data=for_user, status=status.HTTP_200_OK)








class TransferDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET Chats/:id/
    PUT Chats/:id/
    DELETE Chats/:id/
    """
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            a_transfer = self.queryset.get(pk=kwargs["pk"])
            return Response(TransferSerializer(a_transfer).data)
        except Transfer.DoesNotExist:
            return Response(
                data={
                    "message": "Transfer with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    @validate_transfer_data
    def put(self, request, *args, **kwargs):
        try:
            a_tag = self.queryset.get(pk=kwargs["pk"])
            serializer = TransferSerializer()
            updated_transfer = serializer.update(a_tag, request.data)
            return Response(TransferSerializer(updated_transfer).data)
        except Transfer.DoesNotExist:
            return Response(
                data={
                    "message": "Transfer with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            a_transfer = self.queryset.get(pk=kwargs["pk"])
            a_transfer.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Transfer.DoesNotExist:
            return Response(
                data={
                    "message": "Transfer with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )



