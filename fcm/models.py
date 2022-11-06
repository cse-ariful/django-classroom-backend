from django.db import models

# Create your models here.
from account.models import User


class FcmToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    can_send_notification = models.BooleanField(default=True)
    token = models.TextField(blank=True)

    def __str__(self):
        return self.user.email
