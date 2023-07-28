from django.contrib import admin
from .models import Event, Judge, Mentor, Sponsor, EventPicture, Category

admin.site.register(Event)
admin.site.register(Category)
admin.site.register(Judge)
admin.site.register(Mentor)
admin.site.register(Sponsor)
admin.site.register(EventPicture)
