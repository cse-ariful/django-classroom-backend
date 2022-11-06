from django.contrib import admin
from .models import ProposalModel, CourseModel, ProposalSubmission, ProjectMember,ProjectAttachment

# Register your models here.
admin.site.register(ProposalModel)
admin.site.register(ProjectAttachment)
admin.site.register(CourseModel)
admin.site.register(ProposalSubmission)
admin.site.register(ProjectMember)
