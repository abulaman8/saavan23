from django.urls import path
from . import views


urlpatterns = [
        # path('events/', views.get_event_head_events, name='get_event_head_events'),
        path('event/', views.get_event_head_event, name='get_event_head_event')
        ]
