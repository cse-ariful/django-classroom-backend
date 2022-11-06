from django.contrib import admin
from django.urls import path, include
from .views import GoogleLoginView, UserSignupAPiView

urlpatterns = [
    path('v1/login/google/', GoogleLoginView.as_view()),
    path("v1/signup/", UserSignupAPiView.as_view()),
    # path("v1/teacher/signup/", TeacherSignupAPiView.as_view())

]
