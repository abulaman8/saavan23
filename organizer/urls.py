from django.urls import path
from . import views


urlpatterns = [
        # path('events/', views.get_event_head_events, name='get_event_head_events'),
        path('event/', views.get_event_head_event, name='get_event_head_event'),
        path('event/participants/', views.get_event_participants,
             name='get_event_participants'),
        path('event/participant/<int:id>/', views.get_participant_data,
             name='get_participant_data'),
        path('event/all_participants/', views.get_all_participants_data, name='get_all_participants_data'),
        ]
