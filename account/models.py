from django.contrib.auth.models import AbstractUser
from django.db import models

from rest_framework.authtoken.models import Token

departments = [
    ("CSE", "Computer science"),
    ("EEE", "Electrical engineering")
]
designations = [
    ("Lecturer", "Lecturer"),
    ("Senior Lecturer", "Senior")
]


class User(AbstractUser):
    class Types(models.TextChoices):
        TEACHER = 'T', "Teacher"
        STUDENT = "S", "Student"
        GENERAL = "G", "General"

    email = models.EmailField(max_length=254, unique=True)
    type = models.CharField(max_length=20, choices=Types.choices, default=Types.GENERAL)
    id_no = models.CharField(max_length=100, blank=False)
    mobile = models.CharField(max_length=100)
    department = models.CharField(choices=departments, max_length=100, default="CSE")

    # avatar = models.CharField(blank=True)


# def get_my_token(self):
#     return Token.objects.get(user=self.user)
#
#
# my_token = property(get_my_token)


class Profile(models.Model):
    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return self.user.email

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    completed = models.BooleanField(default=False)

    # students
    batch = models.CharField(max_length=50, null=True, blank=True)
    section = models.CharField(max_length=50, null=True, blank=True)

    # teacher
    designation = models.CharField(max_length=240, null=True, blank=True)
    short_name = models.CharField(max_length=50, blank=True, null=True)
