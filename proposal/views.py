from datetime import datetime

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.parsers import FileUploadParser, MultiPartParser
from .models import ProposalModel, CourseModel, ProjectAttachment
from .serializers import ProposalSerializer, CourseSerializer, CreateProposalSerializer, \
    ProposalSubmissionListSerializer, ProposalSubmissionCreateSerializer, ProposalSubmissionDetailsSerializer, \
    ProjectAttachmentSerializer
from .models import ProposalSubmission, ProjectMember
from django.core.files.storage import default_storage


# Create and Retrieve course list
class CourseListApiView(generics.ListCreateAPIView):
    model = CourseModel

    def get_queryset(self):
        return CourseModel.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CourseSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


# Update and get details of courses
class CourseDetailsApiView(generics.RetrieveUpdateAPIView):
    model = CourseModel

    def get_queryset(self):
        return CourseModel.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return CourseSerializer
        return CourseSerializer


# Create and get list of proposal events created by teachers
class ProposalListApiView(generics.ListCreateAPIView):
    model = ProposalModel
    queryset = ProposalModel.objects.all()

    def get_queryset(self):
        return ProposalModel.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateProposalSerializer
        return ProposalSerializer


# Update or get details of proposal event created by teacher
class ProposalUpdateApiView(generics.RetrieveUpdateAPIView):
    model = ProposalModel

    def get_queryset(self):
        return ProposalModel.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProposalSerializer
        return ProposalSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ProposalSubmissionView(APIView):
    model = ProposalSubmission

    def get_queryset(self):
        return ProposalSubmission.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProposalSubmissionCreateSerializer
        return ProposalSubmissionDetailsSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get(self, request):
        proposal_id = request.query_params.get("proposal_id", None)
        submission_id = request.query_params.get("submission_id", None)
        is_teacher = request.user.type == "T"
        if proposal_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={"message": "Please add proposal id query parameter"})
        #if submission_id is None:

        submission = ProposalSubmission.objects.get(proposal_id=proposal_id)
        serializer = ProposalSubmissionDetailsSerializer(submission)
        return Response(status=200,data=serializer.data)

    # user trying to create a submission draft
    def post(self, request):
        serializer = ProposalSubmissionCreateSerializer(data=request.data)
        if serializer.is_valid():
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    # def get(self, request, pk):
    #     proposal = ProposalSubmission.objects.get(proposal_id=pk)
    #     serializer = ProposalTeamSerializer(proposal)
    #     return Response(
    #         data=serializer.data,
    #         status=status.HTTP_200_OK
    #
    #     )
    #
    # def post(self, request, pk):
    #     if request.user.type != 'S':
    #         return Response(
    #             data={
    #                 "message": "Only students can register for projects"
    #             },
    #             status=status.HTTP_400_BAD_REQUEST
    #         )
    #     try:
    #         existing = ProjectMember.objects.get(user=request.user)
    #         return Response(
    #             data={
    #                 "message": "You are already in a team\nLeave the team to create your own team."
    #             },
    #             status=status.HTTP_400_BAD_REQUEST
    #         )
    #     except ProjectMember.DoesNotExist:
    #         team = ProposalSubmission.objects.create(proposal_id=pk)
    #         s_model = ProjectMember.objects.create(user=request.user, team_id=team.id, is_leader=True)
    #         try:
    #             team_serialize = ProposalTeamSerializer(data=team)
    #             member_serialize = ProposalTeamMemberSerializer(data=s_model)
    #             team_serialize.is_valid()
    #             member_serialize.is_valid()
    #             return Response(
    #                 data={
    #                     "team": team_serialize.data,
    #                     "leader": member_serialize.data
    #                 },
    #                 status=status.HTTP_201_CREATED
    #             )
    #         except Exception:
    #             team.delete()
    #             s_model.delete()
    #             return Response(
    #                 data={
    #                     "message": "Error creating team."
    #                 },
    #                 status=status.HTTP_409_CONFLICT
    #             )


class ProposalAttachmentUploadView(APIView):
    parser_classes = (MultiPartParser,)

    def get_attachement_or_none(self, pk):
        try:
            return ProjectAttachment.objects.get(submission=pk)
        except ProposalSubmission.DoesNotExist:
            return None

    def get_submission_or_none(self, pk):
        try:
            return ProposalSubmission.objects.get(pk=pk)
        except ProposalSubmission.DoesNotExist:
            return None

    def post(self, request, pk, format="png"):
        if 'file' not in request.FILES:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "Please attach a file"})
        submission = self.get_submission_or_none(pk)
        if submission is None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "Proposal submission id is not valid"})
        if submission.proposal.submission_deadline > datetime.now():
            return Response(status=status.HTTP_403_FORBIDDEN,
                            data={"message": "This proposal submission deadline is over"})

        attachment = self.get_attachement_or_none(pk)
        up_file = request.FILES['file']

        attachment_file_loc = ('media/proposal/attachments/file_%d.%s' % (pk, format))
        default_storage.save(attachment_file_loc, up_file)
        if attachment is not None:
            attachment.path = attachment_file_loc
            attachment.save()
        else:
            attachment = ProjectAttachment.objects.create(path=attachment_file_loc, submission=pk,
                                                          uploaded_by=request.user.id)
        # destination = open(attachment_file_loc, 'wb+')
        # for chunk in up_file.chunks():
        #     destination.write(chunk)
        # destination.close()
        serializer = ProjectAttachmentSerializer(attachment)
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)
