from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('registered-events/', views.registered_events, name='registered-events'),
    path('register-event/<int:id>/', views.register_event, name='register-event'),
        ]
