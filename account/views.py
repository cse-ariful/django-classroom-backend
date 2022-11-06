import json

from django.shortcuts import render

# Create your views here.
import requests
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from google.auth.transport import requests as google_request
from google.oauth2 import id_token
from account.models import User
from fcm.views import send_notification
from .models import Profile
from .serializers import TeacherSerializer, StudentSerializer, UserSerializer, ProfileSerializer
from django.core import serializers


class UserSignupAPiView(APIView):
    def get(self, request):
        try:
            student = Profile.objects.get(pk=request.user.pk)
            serializer = TeacherSerializer(data=student, many=False)
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK
            )
        except Profile.DoesNotExist:
            return Response(
                data={
                    "message": "User not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request):
        request_data = request.data.copy()
        request_data['email'] = request.user.email
        request_data['username'] = request.user.username
        request_data['type'] = 'S'
        user = User.objects.get(username=request.user.username)
        serializer = StudentSerializer(user, data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def post(self, request):
        # user = User.objects.get(username="cse.ariful@gmail.com")
        try:
            user = request.user
            request_data = request.data.copy()
            user_type = request_data['type']
            name = request_data['name']
            id_no = request_data['id_no']
            department = request_data['department']

            if user_type == "T":
                designation = request_data['designation']
                short_name = request_data['short_name']

                if user.profile is None:
                    Profile.objects.create(user=user, designation=designation, short_name=short_name, completed=True)
                else:
                    user.profile.designation = designation
                    user.profile.short_name = short_name
                    user.profile.completed = True
                    user.profile.save()

                user.type = "T"
                user.first_name = name
                user.id_no = id_no
                user.department = department
                user.save()

                profile = Profile.objects.get(user=request.user)
                serializer = ProfileSerializer(profile)
                return Response(
                    data=serializer.data,
                    status=status.HTTP_201_CREATED
                )

            elif user_type == "S":
                pass
            else:
                return Response(
                    data={"message": "No User type provided"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except MultiValueDictKeyError:
            return Response(
                data={"message": "Invalid data"},
                status=status.HTTP_400_BAD_REQUEST
            )


class GoogleLoginView(APIView):
    permission_classes = []

    def get_user_or_none(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None

    def post(self, request):
        if 'id_token' not in request.data:
            return Response(
                data={
                    "message": "id_token is required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            input_token = request.data['id_token']
            print(input_token)
            gmail_details = id_token.verify_oauth2_token(input_token, google_request.Request(),
                                                         "701823630979-0jnfd6uoceult5iqrl5m2ap59tjo6b9m.apps.googleusercontent.com")
            print(gmail_details)
            user = self.get_user_or_none(email=gmail_details['email'])
            if user is None:
                user = User.objects.create_user(email=gmail_details['email'],
                                                username=gmail_details['email'],
                                                first_name=gmail_details['given_name'],
                                                last_name=gmail_details['family_name'],
                                                )
            new_token, created = Token.objects.get_or_create(user=user)
            sent_success = send_notification(title="Login Alert", message="Hey," + user.last_name + " your account "
                                                                          + user.email
                                                                          + " logged in from a new device",
                                             user=user)
            print("notification sent send status", sent_success)
            profile = Profile.objects.get(user=user)
            serializer = ProfileSerializer(profile)
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK
            )
        except ValueError as err:
            print(err)
            return Response(
                data={
                    "message": "Invalid token"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
