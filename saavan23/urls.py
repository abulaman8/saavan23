from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('drf_social_oauth2.urls')),
    path('events/', include('event.urls')),
    path('', include('student.urls')),
    path('organizers/', include('organizer.urls')),
]
