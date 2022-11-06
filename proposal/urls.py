from django.contrib import admin
from django.urls import path, include
from .views import ProposalListApiView, CourseListApiView, ProposalSubmissionView, CourseDetailsApiView, \
    ProposalUpdateApiView, ProposalAttachmentUploadView

urlpatterns = [

    # Course Create or list
    path('v1/courses/', CourseListApiView.as_view()),

    # Course details or update (pk is course id)
    path('v1/courses/<int:pk>', CourseDetailsApiView.as_view()),

    # Proposal List or Create
    path('v1/proposals/', ProposalListApiView.as_view()),

    # Proposal details update (pk is proposal id)
    path('v1/proposals/<int:pk>/', ProposalUpdateApiView.as_view()),

    # get proposal submission for proposal (pk is proposal id)
    path('v1/proposal-submission/', ProposalSubmissionView.as_view()),

    # uploading proposal attachment (pk is proposal submission id)
    path('v1/proposal-submission/attachment/<int:pk>', ProposalAttachmentUploadView.as_view())

]
