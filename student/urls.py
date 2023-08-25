from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('registered-events/', views.registered_events, name='registered-events'),
    path('register-event/<int:id>/', views.register_event, name='register-event'),
    path('profile/', views.get_student_profile, name='profile'),
    path('profile/edit/', views.update_student_profile, name='edit-profile'),
    path('registered-events/<int:id>/', views.get_event_appliaction_data,
         name='get_event_appliaction_data_'),
    path('unregister/<int:id>/', views.delete_registration, name='unregister'),
        ]
