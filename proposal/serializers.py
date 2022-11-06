from rest_framework import serializers

from account.models import User
from account.serializers import ProfileSerializer, UserSerializer, UserSerializerMin
from .models import CourseModel, ProposalModel, ProjectMember, ProposalSubmission, ProjectAttachment
from account.serializers import StudentSerializer


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseModel
        fields = '__all__'
        read_only_fields = ('created_by',)


class ProposalSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)

    class Meta:
        model = ProposalModel
        fields = (
            "id",
            "title",
            "semester",
            'description',
            'max_member',
            'submission_deadline',
            "created_at",
            "modified_at",
            "course"
        )

    def to_representation(self, instance):
        self.fields['course'] = CourseSerializer(read_only=True)
        return super(ProposalSerializer, self).to_representation(instance)


class CreateProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProposalModel
        fields = (
            'title',
            "semester",
            'description',
            'max_member',
            "created_at",
            "modified_at",
            "course"
        )


class ProposalSubmissionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProposalSubmission
        fields = (
            'proposal',
            'preferred_supervisors',
            'project_name',
            'notes'
        )


class ProposalSubmissionListSerializer(serializers.ModelSerializer):
    created_by = UserSerializerMin(many=False)

    class Meta:
        model = ProposalSubmission
        fields = (
            'id',
            'proposal',
            'preferred_supervisors',
            'project_name',
            'notes',
            'status',
            'created_by',
            'created_at',
            'modified_at'
        )


class ProposalTeamMemberSerializer(serializers.ModelSerializer):
    user = UserSerializerMin()

    class Meta:
        model = ProjectMember
        fields = "__all__"


class ProjectMemberSerializer(serializers.ModelSerializer):
    user = UserSerializerMin()

    class Meta:
        model = ProjectMember
        fields = "__all__"


class ProposalSubmissionDetailsSerializer(serializers.ModelSerializer):
    created_by = UserSerializerMin(many=False)
    members = serializers.SerializerMethodField()

    class Meta:
        model = ProposalSubmission
        fields = (
            'id',
            'proposal',
            'preferred_supervisors',
            'project_name',
            'notes',
            'status',
            'created_by',
            'created_at',
            'modified_at',
            'members'
        )

    def get_members(self, obj):
        products = ProjectMember.objects.filter(proposal_submission=obj.pk)
        response = ProjectMemberSerializer(products, many=True).data
        return response


class ProposalTeamSerializer(serializers.ModelSerializer):
    proposal = ProposalSerializer()
    members = serializers.SerializerMethodField()

    class Meta:
        model = ProposalSubmission
        fields = (
            'proposal',
            'preferred_supervisors',
            'project_name',
            'status'
        )


class ProjectAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectAttachment
        fields = "__all__"
