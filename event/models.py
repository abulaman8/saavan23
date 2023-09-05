from django.db import models
from organizer.models import OrganizingTeam


class Judge(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    bio = models.CharField(max_length=2000)
    image = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


class Mentor(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    bio = models.CharField(max_length=2000)
    image = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


class Speaker(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    bio = models.CharField(max_length=2000)
    image = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Sponsor(models.Model):
    name = models.CharField(max_length=200)
    logo = models.URLField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    type = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name


class EventPicture(models.Model):
    image = models.URLField(blank=True)

    def __str__(self):
        return self.image.url


class Event(models.Model):
    name = models.CharField(max_length=200)
    registration_start_date = models.DateTimeField(null=True, blank=True)
    registration_end_date = models.DateTimeField(null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=360, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    header_image = models.URLField(blank=True, null=True)
    team = models.ForeignKey(OrganizingTeam, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    fee = models.IntegerField(default=0)
    max_participants = models.IntegerField(null=True, blank=True)
    is_team_event = models.BooleanField(default=False)
    meet_link = models.URLField(blank=True, null=True)
    yt_link = models.URLField(blank=True, null=True)
    ig_link = models.URLField(blank=True, null=True)
    fb_link = models.URLField(blank=True, null=True)
    twitter_link = models.URLField(blank=True, null=True)
    misc_links = models.URLField(blank=True, null=True)
    website_links = models.URLField(blank=True, null=True)
    judges = models.ManyToManyField(Judge, blank=True)
    mentors = models.ManyToManyField(Mentor, blank=True)
    sponsors = models.ManyToManyField(Sponsor, blank=True)
    speakers = models.ManyToManyField(Speaker, blank=True)
    pictures = models.ManyToManyField(EventPicture, blank=True)
    template = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=False)
    open = models.BooleanField(default=True)

    def __str__(self):
        return self.name
