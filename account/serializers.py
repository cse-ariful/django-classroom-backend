from rest_framework import serializers
from .models import Profile, User
from rest_framework.authtoken.models import Token


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'first_name',
            "last_name",
            'email',
            'username',
            'id_no',
            'section',
            'batch',
            'mobile'

        )


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'first_name',
            "last_name",
            'email',
            'type',
            'username',
            'id_no',
            'mobile',
            'short_name'
        )


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = 'key'


class UserSerializerMin(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'type',
            'department'
        )


class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'username', 'first_name', 'last_name', 'email', 'type', 'id_no', 'mobile', 'id_no', 'department',
            'token')

    def get_token(self, obj):
        return Token.objects.get(user=obj).key


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ('batch', 'section', 'designation', 'short_name', 'completed', 'user')
