from django.db.models import Q
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, authentication_classes
from event.models import Event
from .models import (
        Student,
        StudentEventApplication,
        StudentTeam,
        StudentTeamEventApplictaion
        )

from event.serializers import EventSerializer
from .serializers import StudentEventApplicationSerializer, StudentSerializer, StudentTeamEventApplictaionSerializer


def student_required(view_func):
    # @permission_classes([IsAuthenticated])
    @authentication_classes([OAuth2Authentication])
    def wrap(request, *args, **kwargs):
        print(request.user)
        try:
            student = Student.objects.get(user=request.user)
            if student:
                return view_func(request, *args, **kwargs)
        
            else:
                return Response(
                        {'message': 'You are not authorized to view this page'},
                        status=status.HTTP_401_UNAUTHORIZED
                        )
        except Student.DoesNotExist:
            return Response(
                    {'message': 'You are not authorized to view this page'},
                    status=status.HTTP_401_UNAUTHORIZED
                    )
        except TypeError as e:
            print(e)
            return Response(
                    {'message': 'You are not authorized to view this page, try logging in'},
                    status=status.HTTP_401_UNAUTHORIZED
                    )
    return wrap



@api_view(['GET'])
def home(request):
    content = {'message': 'Hello, World!'}
    return Response(content, status=status.HTTP_200_OK)


@api_view(['GET'])
@student_required
def registered_events(request):
    student = Student.objects.get(user=request.user)
    events = student.events.all()
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@student_required
def register_event(request, id):
    student = Student.objects.get(user=request.user)
    data = request.data
    try:
        event = Event.objects.get(id=id)
    except Event.DoesNotExist:
        return Response({'message': 'Event does not exist'}, status=status.HTTP_404_NOT_FOUND)
    if event in student.events.all():
        return Response({'message': 'Already registered'}, status=status.HTTP_400_BAD_REQUEST)
    if event.is_team_event:
        team_members = []
        for member in data['team_members']:
            try:
                student = Student.objects.get(email=member)
            except Student.DoesNotExist:
                return Response({'message': 'Student does not exist'}, status=status.HTTP_404_NOT_FOUND)
            team_members.append(student)
        for member in team_members:
            if event in member.events.all():
                return Response({'message': f'User {member.email} has already registered'}, status=status.HTTP_400_BAD_REQUEST)
            member.events.add(event)
        student_team = StudentTeam.objects.create(
                name=data['team_name'],
                event=event,
                )
        student_team.members.set(team_members)
        stea = StudentTeamEventApplictaion.objects.create(
                event=event,
                team=student_team,
                custom_data=data['custom_data'],
                artifacts=data['artifacts'],
                )
        return Response({'message': 'Successfully registered'}, status=status.HTTP_201_CREATED)
    else:
        student.events.add(event)
        event_application = StudentEventApplication.objects.create(
                student=student,
                event=event,
                artifacts=data.get('artifacts', None),
                custom_data=data.get('custom_data', None),
                )
        return Response({'message': 'Event registered'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@student_required
def get_student_profile(request):
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        return Response({'message': 'Student does not exist'}, status=status.HTTP_404_NOT_FOUND)
    serializer = StudentSerializer(student)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
@student_required
def update_student_profile(request):
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        return Response({'message': 'Student does not exist'}, status=status.HTTP_404_NOT_FOUND)
    data = request.data
    handle = data.get('handle', None)
    if handle:
        student.handle = handle
        student.save()
    return Response({'message': 'Profile updated'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@student_required
def get_event_appliaction_data(request, id):
    student = Student.objects.get(user=request.user)
    try:
        event = Event.objects.get(id=id)
    except Event.DoesNotExist:
        return Response(
                {
                    'message': 'Event Does not exist'
                    },
                status=status.HTTP_404_NOT_FOUND
                )
    if event in student.events.all():
        if event.is_team_event:
            team = StudentTeam.objects.filter(event=event,
                                              members__id=student.id).first()
            application = StudentTeamEventApplictaion.objects.filter(event=event, team=team).first()
            data = StudentTeamEventApplictaionSerializer(application).data
            
            return Response(
                    data, status=status.HTTP_200_OK
                    )
        application = StudentEventApplication.objects.filter(Q(student=student) & Q(event=event)).first()
        data = StudentEventApplicationSerializer(application).data
        return Response(
                data, status=status.HTTP_200_OK
                )
    else:
        return Response(
                {
                    'message': 'You are not registered to this event'
                    },
                status=status.HTTP_401_UNAUTHORIZED
                )
