from django.db.models import Q
from django.conf import settings
from django.template import Template, Context
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
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


solo_reg_template = '''
<html>
    <head>
        <title>Event Registration</title>
    </head>
    <body>
        <h1>Event Registration Confirmation</h1>
        <p>Hi {{ name }},</p>
        <p>You have successfully registered for the event {{ event_name }}.</p>
        <p>You can find further details on your Profile page at the Saavan Dashboard.<p>
        <p>Regards,<br>
        Saavan Team</p>
        
       
    </body>

</html>
'''


team_reg_template = '''
<html>
    <head>
        <title>Event Registration</title>
    </head>
    <body>
        <h1>Event Registration Confirmation</h1>
        <p>Hi {{ name }},</p>
        <p>You have successfully registered for the event {{ event_name }} under
        the {{ team_name }} team.</p>
        <p>You can find further details on your Profile page at the Saavan Dashboard.<p>
        <p>Regards,<br>
        Saavan Team</p>
        
       
    </body>

</html>
'''



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
                user = User.objects.get(email=member)
                student = Student.objects.get(user=user)
            except Student.DoesNotExist:
                return Response({'message': 'Student does not exist'}, status=status.HTTP_404_NOT_FOUND)
            except User.DoesNotExist:
                return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
            team_members.append(student)
        for member in team_members:
            if event in member.events.all():
                return Response({'message': f'User {member.user.email} has already registered'}, status=status.HTTP_400_BAD_REQUEST)
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
        for student in student_team.members.all():

            template = Template(team_reg_template)
            context = Context(
                    {
                        'name': student.user.first_name,
                        'event_name': event.name,
                        'team_name': student_team.name,

                        }
                    )
            rendered = template.render(context)
            subject = 'Registration for ' + event.name
            from_email = settings.EMAIL_HOST_USER
            to_email = [student.user.email]
            msg = EmailMultiAlternatives(subject, rendered, from_email, to_email)
            msg.attach_alternative(rendered, "text/html")
            msg.send()


        return Response({'message': 'Successfully registered'}, status=status.HTTP_201_CREATED)
    else:
        student.events.add(event)
        event_application = StudentEventApplication.objects.create(
                student=student,
                event=event,
                artifacts=data.get('artifacts', None),
                custom_data=data.get('custom_data', None),
                )
        template = Template(solo_reg_template)
        context = Context(
                {
                    'name': student.user.first_name,
                    'event_name': event.name,

                    }
                )
        rendered = template.render(context)
        subject = 'Registration for ' + event.name
        from_email = settings.EMAIL_HOST_USER
        to_email = [student.user.email]
        msg = EmailMultiAlternatives(subject, rendered, from_email, to_email)
        msg.attach_alternative(rendered, "text/html")
        msg.send()

        return Response({'message': 'Event registered'}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@student_required
def delete_registration(request, id):
    student = Student.objects.get(user=request.user)
    try:
        event = Event.objects.get(id=id)
    except Event.DoesNotExist:
        return Response({'message': 'Event does not exist'}, status=status.HTTP_404_NOT_FOUND)
    if event.is_team_event:
        if event in student.events.all():
            team = student.teams.filter(event=event).first()
            if team:
                for member in team.members.all():
                    member.events.remove(event)
                    member.save()
                team.delete()
                return Response({'message': 'Event unregistered'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Team does not exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'message': 'You are not registered to this Event.'}, status=status.HTTP_404_NOT_FOUND)
    else:
        if event in student.events.all():
            student.events.remove(event)
            student.save()
            application = StudentEventApplication.objects.filter(student=student, event=event).first()
            if application:
                application.delete()
            else:
                return Response({'message': 'Application does not exist'}, status=status.HTTP_404_NOT_FOUND)
            return Response({'message': 'Event unregistered'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'You are not registered to this Event.'}, status=status.HTTP_404_NOT_FOUND)


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
            # team = StudentTeam.objects.filter(event=event,
            #                                   members__id=student.id).first()
            team = student.teams.filter(event=event).first()
            application = StudentTeamEventApplictaion.objects.filter(event=event, team=team).first()
            data = StudentTeamEventApplictaionSerializer(application).data
            
            return Response(
                    data, status=status.HTTP_200_OK
                    )
        else:
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

#
# @api_view(['PUT'])
# @student_required
# def update_event_application(request, id):
#     data = request.data
#     student = Student.objects.get(user=request.user)
#     try:
#         event = Event.objects.get(id=id)
#     except Event.DoesNotExist:
#         return Response(
#                 {
#                     'message': 'Event Does not exist'
#                     },
#                 status=status.HTTP_404_NOT_FOUND
#                 )
#     if event in student.events.all():
#         if event.is_team_event:
#             team = student.teams.filter(event=event).first()
#             if team:
#                 for member in team.members:
#                     member.events.remove(event)
#             team.members.clear()
#
#             application = StudentTeamEventApplictaion.objects.filter(event=event, team=team).first()
#
#             team_members = []
#             for member in data['team_members']:
#                 try:
#                     user = User.objects.get(email=member)
#                     student = Student.objects.get(user=user)
#                 except Student.DoesNotExist:
#                     return Response({'message': 'Student does not exist'}, status=status.HTTP_404_NOT_FOUND)
#                 except User.DoesNotExist:
#                     return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
#                 team_members.append(student)
#             for member in team_members:
#                 member.events.add(event)
#             team.members.set(team_members)
#             application.custom_data = data.get('custom_data', {})
#             application.save()
#             return Response({'message': 'Team updated successfully'}, status=status.HTTP_200_OK)
#         else:
#             student.events.add(event)
#             application = StudentEventApplication.objects.filter(event=event, student=student).first()
#             application.custom_data = data.get('custom_data', {})
#             application.save()
#             return Response({'message': 'Application updated successfully'}, status=status.HTTP_200_OK)
#




