from django.urls import path
from . import views


urlpatterns = [
        path('', views.get_announcements, name='get_announcements'),
        path('<int:id>/', views.get_announcement, name='get_announcement'),
        ]
