from django.contrib import admin
from .models import Student, StudentTeam, StudentEventApplication, StudentTeamEventApplictaion

admin.site.register(Student)
admin.site.register(StudentTeam)
admin.site.register(StudentEventApplication)
admin.site.register(StudentTeamEventApplictaion)
