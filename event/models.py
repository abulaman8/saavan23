from django.db import models
from organizer.models import OrganizingTeam


class Judge(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    bio = models.CharField(max_length=2000)
    image = models.ImageField(upload_to='images/', blank=True)

    def __str__(self):
        return self.name


class Mentor(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    bio = models.CharField(max_length=2000)
    image = models.ImageField(upload_to='images/', blank=True)

    def __str__(self):
        return self.name


class Speaker(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    bio = models.CharField(max_length=2000)
    image = models.ImageField(upload_to='images/', blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Sponsor(models.Model):
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='images/', blank=True)
    website = models.URLField(max_length=600, blank=True)
    type = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name


class EventPicture(models.Model):
    image = models.ImageField(upload_to='images/', blank=True)

    def __str__(self):
        return self.image.url


class Event(models.Model):
    name = models.CharField(max_length=200)
    registration_start_date = models.DateTimeField(null=True, blank=True)
    registration_end_date = models.DateTimeField(null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=360, null=True, blank=True)
    description = models.CharField(max_length=2000)
    team = models.ForeignKey(OrganizingTeam, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    fee = models.IntegerField(default=0)
    max_participants = models.IntegerField(null=True, blank=True)
    meet_link = models.URLField(max_length=600, blank=True, null=True)
    yt_link = models.URLField(max_length=600, blank=True, null=True)
    ig_link = models.URLField(max_length=600, blank=True, null=True)
    fb_link = models.URLField(max_length=600, blank=True, null=True)
    twitter_link = models.URLField(max_length=600, blank=True, null=True)
    judges = models.ManyToManyField(Judge, blank=True)
    mentors = models.ManyToManyField(Mentor, blank=True)
    sponsors = models.ManyToManyField(Sponsor, blank=True)
    pictures = models.ManyToManyField(EventPicture, blank=True)

    def __str__(self):
        return self.name
