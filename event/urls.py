from django.urls import path
from . import views

urlpatterns = [
        path('categories/', views.get_categories, name='get-categories'),
        path('create-event/', views.create_event, name='create-event'),
        path('all/', views.get_events, name='get-events'),
        path('<int:id>/', views.get_event, name='get-event'),
        path('update/<int:id>/', views.update_event, name='update-event'),
        path('delete/<int:id>/', views.delete_event, name='delete-event'),
        path('add-winners/', views.add_winners, name='add-winners'),
        path('set-template/<int:id>/', views.setup_template, name='set-template'),
        path('set-header-image/<int:id>/', views.add_header_image, name='set-header-image'),
        path('<str:category>/', views.get_events_by_category, name='get-events-by-category'),
        path('open/<int:id>/', views.open_registration, name='open-registration'),
        path('close/<int:id>/', views.close_registration, name='close-registration'),
        ]
