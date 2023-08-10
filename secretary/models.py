from django.db import models
from django.contrib.auth.models import User


class Secretary(models.Model):
    handle = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    proile_picture = models.URLField(max_length=600, blank=True, null=True)

    def __str__(self):
        return self.handle
    
