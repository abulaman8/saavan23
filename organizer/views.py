from event.models import Event, OrganizingTeam
from event.views import event_head_required
from event.serializers import SimpleEventSerializer, EventSerializer
from student.serializers import (
        SimpleStudentSerializer,
        SimpleStudentTeamSerializer,
        StudentTeamEventApplictaionSerializer,
        StudentEventApplicationSerializer
        )
from .models import EventHead
from student.models import Student, StudentTeam, StudentTeamEventApplictaion, StudentEventApplication
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

#
# @api_view(['GET'])
# @event_head_required
# def get_event_head_events(request):
#     event_head = EventHead.objects.get(user=request.user)
#     events = Event.objects.filter(event_head=event_head)
#     return Response(SimpleEventSerializer(events, many=True).data, status=status.HTTP_200_OK)
#


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


@api_view(['GET'])
@event_head_required
def get_event_participants(request):
    event_head = EventHead.objects.get(user=request.user)
    try:
        team = OrganizingTeam.objects.get(event_head=event_head)
    except OrganizingTeam.DoesNotExist:
        return Response({'error': 'You are not an event head'}, status=status.HTTP_403_FORBIDDEN)
    try:
        event = Event.objects.get(team=team)
    except Event.DoesNotExist:
        return Response({'error': 'Event does not exist'}, status=status.HTTP_404_NOT_FOUND)
    if event.is_team_event:
        teams = event.teams.all()
        data = SimpleStudentTeamSerializer(teams, many=True).data
        return Response(data, status=status.HTTP_200_OK)
    else:
        participants = event.participants.all()
        data = SimpleStudentSerializer(participants, many=True).data
        return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
@event_head_required
def get_participant_data(request, id):
    event_head = EventHead.objects.get(user=request.user)
    try:
        team = OrganizingTeam.objects.get(event_head=event_head)
    except OrganizingTeam.DoesNotExist:
        return Response({'error': 'You are not an event head'}, status=status.HTTP_403_FORBIDDEN)
    try:
        event = Event.objects.get(team=team)
    except Event.DoesNotExist:
        return Response({'error': 'Event does not exist'}, status=status.HTTP_404_NOT_FOUND)
    if event.is_team_event:
        try:
            team = StudentTeam.objects.get(id=id)
        except StudentTeam.DoesNotExist:
            return Response({'error': 'Team does not exist'}, status=status.HTTP_404_NOT_FOUND)
        if team.event != event:
            return Response({'error': 'Team does not belong to this event'}, status=status.HTTP_400_BAD_REQUEST)
        application = StudentTeamEventApplictaion.objects.filter(team=team).first()
        data = StudentTeamEventApplictaionSerializer(application).data
        return Response(data, status=status.HTTP_200_OK)
    else:
        try:
            participant = Student.objects.get(id=id)
        except Student.DoesNotExist:
            return Response({'error': 'Participant does not exist'}, status=status.HTTP_404_NOT_FOUND)
        if participant not in event.participants.all():
            return Response({'error': 'Participant does not belong to this event'}, status=status.HTTP_400_BAD_REQUEST)
        application = StudentEventApplication.objects.filter(student=participant).first()
        data = StudentEventApplicationSerializer(application).data
        return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
@event_head_required
def get_all_participants_data(request):
    event_head = EventHead.objects.get(user=request.user)
    try:
        team = OrganizingTeam.objects.get(event_head=event_head)
    except OrganizingTeam.DoesNotExist:
        return Response({'error': 'You are not an event head'}, status=status.HTTP_403_FORBIDDEN)
    try:
        event = Event.objects.get(team=team)
    except Event.DoesNotExist:
        return Response({'error': 'Event does not exist'}, status=status.HTTP_404_NOT_FOUND)
    if event.is_team_event:
        applications = StudentTeamEventApplictaion.objects.filter(event=event).all()
        data = StudentTeamEventApplictaionSerializer(applications, many=True).data
        return Response(data, status=status.HTTP_200_OK)
    else:
        applications = StudentEventApplication.objects.filter(event=event).all()
        data = StudentEventApplicationSerializer(applications, many=True).data
        return Response(data, status=status.HTTP_200_OK)
