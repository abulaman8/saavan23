from django.db import models
from django.contrib.auth.models import User


class Organizer(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    role = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return self.name


class EventHead(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    handle = models.CharField(max_length=200)
    phone = models.CharField(max_length=200, null=True, blank=True)
    profile_picture = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.user.username


class OrganizingTeam(models.Model):
    event_head = models.ForeignKey(EventHead, on_delete=models.CASCADE)
    organizers = models.ManyToManyField(Organizer, blank=True)

    def __str__(self):
        return self.event_head.user.username



