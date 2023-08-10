from django.db import models
from django.contrib.auth.models import User
from event.models import Event


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    handle = models.CharField(max_length=200)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    profile_picture = models.URLField(max_length=600, null=True, blank=True)
    events = models.ManyToManyField(Event, related_name="participants", blank=True)
    
    def __str__(self):
        return self.handle


class StudentEventApplication(models.Model):
    stduent = models.ForeignKey(Student, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    application_date = models.DateTimeField(auto_now_add=True)
    artifacts = models.URLField(max_length=600, blank=True, null=True)
    custom_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.stduent.handle + ' - ' + str(self.event)


class StudentTeam(models.Model):
    name = models.CharField(max_length=200)
    members = models.ManyToManyField(Student, related_name="teams", blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="teams")

    def __str__(self):
        return self.name + ' - ' + str(self.event)


class StudentTeamEventApplictaion(models.Model):
    team = models.ForeignKey(StudentTeam, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    application_date = models.DateTimeField(auto_now_add=True)
    artifacts = models.URLField(max_length=600, blank=True, null=True)
    custom_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.team.name + ' - ' + str(self.event)


class Winner(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="winners")
    winner = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="wins")
    position = models.IntegerField()

    def __str__(self):
        return self.winner.handle + ' - ' + str(self.event) + ' - ' + str(self.position)


class WinningTeam(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="winning_teams")
    winner = models.ForeignKey(StudentTeam, on_delete=models.CASCADE, related_name="wins")
    position = models.IntegerField()

    def __str__(self):
        return self.winner.name + ' - ' + str(self.event) + ' - ' + str(self.position)
