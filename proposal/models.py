from datetime import timedelta

from django.db import models

# Create your models here.
from django.utils.timezone import now
from django.core.validators import RegexValidator

from account.models import User

submission_status = [
    ("Draft", "Draft"),
    ("Ready", "Ready"),
    ("Published", "Published"),
    ("Blocked", "Blocked"),
]


class CourseModel(models.Model):
    code = models.CharField(max_length=50, unique=True, validators=[RegexValidator(
        regex="(?i)[a-zA-Z]+-[0-9]+",
        message="Invalid course Code"
    )])
    title = models.CharField(max_length=240)
    num_of_credit = models.DecimalField(decimal_places=1, max_digits=10)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


def get_day_after_one_month():
    return now() + timedelta(days=30)


class ProposalModel(models.Model):
    title = models.CharField(max_length=240)
    description = models.CharField(max_length=240, blank=True)
    course = models.ForeignKey(CourseModel, on_delete=models.CASCADE)
    semester = models.CharField(max_length=240)
    max_member = models.PositiveSmallIntegerField(default=3)
    submission_deadline = models.DateTimeField(default=get_day_after_one_month)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.course.title + "  | " + self.semester


class ProposalSubmission(models.Model):
    proposal = models.ForeignKey(ProposalModel, on_delete=models.CASCADE)
    preferred_supervisors = models.CharField(max_length=254, blank=True)
    project_name = models.CharField(max_length=254, blank=False)
    status = models.CharField(choices=submission_status, default=submission_status[0], max_length=100)
    notes = models.CharField(max_length=240, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.project_name


class ProjectMember(models.Model):
    proposal_submission = models.ForeignKey(ProposalSubmission, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="members")
    join_time = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="added_by")
    status = models.CharField((('Approved', 'A'), ("Pending", "P", "Denied", "D")), default="P", max_length=50)

    def __str__(self):
        return self.user.username


class ProjectAttachment(models.Model):
    submission = models.ForeignKey(ProposalSubmission, on_delete=models.CASCADE)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    path = models.CharField(max_length=240)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
