from django.db import models


class Announcement(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title[:30]}...' if len(self.title) > 30 else self.title

