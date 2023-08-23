from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Announcement


@api_view(['GET'])
def get_announcements(request):
    announcements = Announcement.objects.all()
    return Response(
        data=[{
            'id': announcement.id,
            'title': announcement.title,
            'description': announcement.description,
            'created_at': announcement.created_at,
            'updated_at': announcement.updated_at
        } for announcement in announcements],
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
def get_announcement(request, id):
    try:
        announcement = Announcement.objects.get(id=id)
        return Response(
            data={
                'id': announcement.id,
                'title': announcement.title,
                'description': announcement.description,
                'created_at': announcement.created_at,
                'updated_at': announcement.updated_at
            },
            status=status.HTTP_200_OK
        )
    except Announcement.DoesNotExist:
        return Response(
            data={
                'error': 'Announcement does not exist'
            },
            status=status.HTTP_404_NOT_FOUND
        )
