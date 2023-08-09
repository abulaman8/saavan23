from django.urls import path, include
from . import views

urlpatterns = [
        path('', views.secretary_home, name='secretary_home'),
        path('login/', views.secretary_login, name='secretary_login'),
        path('logout/', views.secretary_logout, name='secretary_logout'),
        path('events/<int:event_id>/', views.event_details, name='event_detail'),
        path('events/delete/<int:event_id>/', views.delete_event, name='delete_event'),
        path('events/approve/<int:id>/', views.approve_event, name='approve_event'),
        path('events/disapprove/<int:id>/', views.disapprove_event, name='disapprove_event'),



        ]
