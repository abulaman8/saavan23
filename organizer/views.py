from event.models import Event, OrganizingTeam
from event.views import event_head_required
from event.serializers import SimpleEventSerializer, EventSerializer
from .models import EventHead
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET'])
@event_head_required
def get_event_head_events(request):
    event_head = EventHead.objects.get(user=request.user)
    events = Event.objects.filter(event_head=event_head)
    return Response(SimpleEventSerializer(events, many=True).data, status=status.HTTP_200_OK)


@api_view(['GET'])
@event_head_required
def get_event_head_event(request):
    event_head = EventHead.objects.get(user=request.user)
    try:
        team = OrganizingTeam.objects.get(event_head=event_head)
    except OrganizingTeam.DoesNotExist:
        return Response({'error': 'You are not an event head'}, status=status.HTTP_403_FORBIDDEN)
    try:
        event = Event.objects.get(team=team)
    except Event.DoesNotExist:
        return Response({'error': 'Event does not exist'}, status=status.HTTP_404_NOT_FOUND)
    return Response(EventSerializer(event).data, status=status.HTTP_200_OK)
