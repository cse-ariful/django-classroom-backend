import json

import requests
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import FcmToken

fcm_server_key = "AAAAftwDweo:APA91bEHFWRwCajDKuUL8kcq31_05w7A6ZJZB_g1gDnW_-2uQo4sTyp_8L" \
                 "-NxWtxVXQCCnekGrl5fytqmOPRtJgki7aixcmQnRHMd7dg8XiokkOaQcG5rv01sf4nINp192FTfXVacmEH "
fcm_url = "https://fcm.googleapis.com/fcm/send"


def send_notification(title, message, topic=None, user=None):
    try:
        print("sending notification")
        headers_content = {
            'Content-Type': 'application/json',
            'Authorization': 'key=' + fcm_server_key
        }
        body_content = {
            "notification": {
                "title": title,
                "body": message
            }
        }
        if topic is not None:
            body_content.update({'to': "/topics/" + topic})
        elif user is not None:
            try:
                token_obj = FcmToken.objects.get(user=user)
                body_content.update({'to': token_obj.token})
            except FcmToken.DoesNotExist:
                return -1
        # print(body_content)
        fcm_response = requests.post(url=fcm_url, headers=headers_content, data=json.dumps(body_content))
        return fcm_response.status_code
        # print("response ", fcm_response.status_code)
        # print(fcm_response.reason, fcm_response.content)
    except Exception as err:
        print("notification send exception", err)


class FcmTokenUpdateView(APIView):
    def put(self, request):
        if 'token' not in request.data:
            return Response(
                data={
                    "message": "Token sent is None deleted"
                },
                status=status.HTTP_200_OK
            )
        token = request.data['token']
        try:
            existing = FcmToken.objects.get(user=request.user)
            existing.token = token
            existing.save()
            return Response(
                data={
                    "message": "Token updated"
                }
            )
        except FcmToken.DoesNotExist:
            FcmToken.objects.create(user=request.user, token=token)
            return Response(
                data={
                    "message": "Token created"
                }
            )
