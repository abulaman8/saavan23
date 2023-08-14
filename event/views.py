from oauth2_provider.models import AccessToken, RefreshToken
import json
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from datetime import datetime
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from organizer.models import EventHead, OrganizingTeam, Organizer
from organizer.serializers import EventHeadSerializer, OrganizerSerializer, OrganizingTeamSerializer
from .serializers import (
        EventSerializer,
        CategorySerializer,
        SimpleEventSerializer

        )
from .models import (
        Event,
        Category,
        Judge,
        Speaker,
        Mentor,
        Sponsor,
        EventPicture

        )
from student.models import Student, StudentTeam, Winner, WinningTeam


def event_head_required(view_func):
    # @permission_classes([IsAuthenticated])
    @authentication_classes([OAuth2Authentication])
    def wrap(request, *args, **kwargs):
        print(request.user)
        try:
            event_head = EventHead.objects.get(user=request.user)
            if event_head:
                return view_func(request, *args, **kwargs)
        
            else:
                return Response(
                        {'message': 'You are not authorized to view this page'},
                        status=status.HTTP_401_UNAUTHORIZED
                        )
        except EventHead.DoesNotExist:
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


@api_view(['POST'])
@event_head_required
def create_event(request):
    data = request.data
    print(data)
    judges = data.pop('judges', [])
    speakers = data.pop('speakers', [])
    mentors = data.pop('mentors', [])
    sponsors = data.pop('sponsors', [])
    team = data.pop('team', [])
    pictures = data.pop('pictures', [])
    data["registration_start_date"] = datetime.fromisoformat(data["registration_start_date"])
    data["registration_end_date"] = datetime.fromisoformat(data["registration_end_date"])
    data["date"] = datetime.fromisoformat(data["date"])
    category = Category.objects.get(id=data["category"])
    data["category"] = category

    event_head = EventHead.objects.get(user=request.user)
    judge_instances = []
    speaker_instances = []
    mentor_instances = []
    sponsor_instances = []
    organizer_instances = []
    picture_instances = []
    for judge in judges:
        try:
            judge_instances.append(Judge.objects.get_or_create(**judge)[0])
        except Exception as e:
            print(e)
            return Response(
                    {'message': e},
                    status=status.HTTP_400_BAD_REQUEST
                    )
    for speaker in speakers:
        try:
            speaker_instances.append(Speaker.objects.get_or_create(**speaker)[0])
        except Exception as e:
            print(e)
            return Response(
                    {'message': e},
                    status=status.HTTP_400_BAD_REQUEST
                    )
    for mentor in mentors:
        try:
            mentor_instances.append(Mentor.objects.get_or_create(**mentor)[0])
        except Exception as e:
            print(e)
            return Response(
                    {'message': e},
                    status=status.HTTP_400_BAD_REQUEST
                    )
    for sponsor in sponsors:
        try:
            sponsor_instances.append(Sponsor.objects.get_or_create(**sponsor)[0])
        except Exception as e:
            print(e)
            return Response(
                    {'message': e},
                    status=status.HTTP_400_BAD_REQUEST
                    )
    for picture in pictures:
        try:
            picture_instances.append(EventPicture.objects.get_or_create(**picture)[0])
        except Exception as e:
            print(e)
            return Response(
                    {'message': e},
                    status=status.HTTP_400_BAD_REQUEST
                    )

    for organizer in team:
        try:
            organizer_instances.append(Organizer.objects.get_or_create(**organizer)[0])
        except Exception as e:
            print(e)
            return Response(
                    {'message': e},
                    status=status.HTTP_400_BAD_REQUEST
                    )
    try:
        organizing_team = OrganizingTeam.objects.create(event_head=event_head)
    except Exception as e:
        print(e)
        return Response(
                {'message': e},
                status=status.HTTP_400_BAD_REQUEST
                )
    organizing_team.organizers.set(organizer_instances)
    data['team'] = organizing_team
    try:
        event = Event.objects.create(**data)
    except Exception as e:
        print(e)
        return Response(
                {'message': e},
                status=status.HTTP_400_BAD_REQUEST
                )
    event.judges.set(judge_instances)
    event.speakers.set(speaker_instances)
    event.mentors.set(mentor_instances)
    event.sponsors.set(sponsor_instances)
    event.pictures.set(picture_instances)
    return Response({"message": "event created successfully!!!"}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_events(request):
    events = Event.objects.all()
    serializer = SimpleEventSerializer(events, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_event(request, id):
    try:
        event = Event.objects.get(id=id)
    except Event.DoesNotExist:
        return Response({"message": "event not found"}, status=status.HTTP_404_NOT_FOUND)
    serializer = EventSerializer(event)
    return Response(serializer.data)


@api_view(['PUT'])
@event_head_required
def update_event(request, id):
    try:
        event = Event.objects.get(id=id)
    except Event.DoesNotExist:
        return Response({"message": "event not found"}, status=status.HTTP_404_NOT_FOUND)
    if event.team.event_head.user != request.user:
        return Response({"message": "you are not authorized to update this event"}, status=status.HTTP_401_UNAUTHORIZED)
    data = request.data

    judges = data.pop('judges', [])
    speakers = data.pop('speakers', [])
    mentors = data.pop('mentors', [])
    sponsors = data.pop('sponsors', [])
    team = data.pop('team', [])
    pictures = data.pop('pictures', [])
    data["registration_start_date"] = datetime.fromisoformat(data["registration_start_date"])
    data["registration_end_date"] = datetime.fromisoformat(data["registration_end_date"])
    data["date"] = datetime.fromisoformat(data["date"])
    category = Category.objects.get(id=data["category"])
    data["category"] = category

    event_head = EventHead.objects.get(user=request.user)
    judge_instances = []
    speaker_instances = []
    mentor_instances = []
    sponsor_instances = []
    organizer_instances = []
    picture_instances = []
    for judge in judges:
        judge_object = judge.objects.get_or_create(**judge)[0]
        for key, value in judge.items():
            setattr(judge_object, key, value)
        judge_object.save()
        judge_instances.append(judge_object)
    for speaker in speakers:
        speaker_object = Speaker.objects.get_or_create(**speaker)[0]
        for key, value in speaker.items():
            setattr(speaker_object, key, value)
        speaker_object.save()
        speaker_instances.append(speaker_object)
    for mentor in mentors:
        mentor_object = Mentor.objects.get_or_create(**mentor)[0]
        for key, value in mentor.items():
            setattr(mentor_object, key, value)
        mentor_object.save()
        mentor_instances.append(mentor_object)
    for sponsor in sponsors:
        sponsor_object = Sponsor.objects.get_or_create(**sponsor)[0]
        for key, value in sponsor.items():
            setattr(sponsor_object, key, value)
        sponsor_object.save()
        sponsor_instances.append(sponsor_object)
    for picture in pictures:
        picture_object = EventPicture.objects.get_or_create(**picture)[0]
        for key, value in picture.items():
            setattr(picture_object, key, value)
        picture_object.save()
        picture_instances.append(picture_object)
    for organizer in team:

        organizer_object = Organizer.objects.get_or_create(**organizer)[0]
        for key, value in organizer.items():
            setattr(organizer_object, key, value)
        organizer_object.save()
        organizer_instances.append(organizer_object)

    organizing_team = OrganizingTeam.objects.get_or_create(event_head=event_head)[0]
    organizing_team.organizers.set(organizer_instances)
    data['team'] = organizing_team
    for key, value in data.items():
        setattr(event, key, value)
    event.save()
    event.judges.set(judge_instances)
    event.speakers.set(speaker_instances)
    event.mentors.set(mentor_instances)
    event.sponsors.set(sponsor_instances)
    event.pictures.set(picture_instances)
    return Response({"message": "event created successfully!!!"}, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@event_head_required
def delete_event(request, id):
    try:
        event = Event.objects.get(id=id)
    except Event.DoesNotExist:
        return Response({"message": "event does not exist"}, status=status.HTTP_404_NOT_FOUND)
    if event.team.event_head.user != request.user:
        return Response({"message": "you are not authorized to delete this event"}, status=status.HTTP_401_UNAUTHORIZED)
    event.delete()
    return Response({"message": "event deleted successfully!!!"}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@event_head_required
def add_winners(request):
    data = request.data
    event_id = data.get('event_id')
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return Response({"message": "event does not exist"}, status=status.HTTP_404_NOT_FOUND)
    if event.team.event_head.user != request.user:
        return Response({"message": "you are not authorized to add winners to this event"},
                        status=status.HTTP_401_UNAUTHORIZED)
    if event.is_team_event:
        teams = data.get('teams')
        for team in teams:
            team_id = team.get('team_id')
            try:
                team_object = StudentTeam.objects.get(id=team_id)
            except StudentTeam.DoesNotExist:
                return Response({"message": "team does not exist"}, status=status.HTTP_404_NOT_FOUND)
            if team.event != event:
                return Response({"message": "team does not belong to this event"}, status=status.HTTP_400_BAD_REQUEST)
            winning_team = WinningTeam.objects.create(
                    winner=team_object,
                    event=event,
                    position=int(team.get('position'))
                    )
        return Response({"message": "winners added successfully"}, status=status.HTTP_201_CREATED)
    else:
        students = data.get('students')
        for student in students:
            student_id = student.get('student_id')
            try:
                student_object = Student.objects.get(id=student_id)
            except Student.DoesNotExist:
                return Response({"message": "student does not exist"}, status=status.HTTP_404_NOT_FOUND)
            if event not in student_object.events.all():
                return Response(
                        {"message": "student does not belong to this event"},
                        status=status.HTTP_400_BAD_REQUEST)
            winning_student = Winner.objects.create(
                    winner=student_object,
                    event=event,
                    position=int(student.get('position'))
                    )

        return Response({"message": "winners added successfully"}, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
@event_head_required
def setup_template(request, id):
    try:
        event = Event.objects.get(id=id)
    except Event.DoesNotExist:
        return Response({"message": "event does not exist"}, status=status.HTTP_404_NOT_FOUND)
    if event.team.event_head.user != request.user:
        return Response({"message": "you are not allowed to perform this action"}, status=status.HTTP_403_FORBIDDEN)
    data = request.data
    template = data.get('template')
    json_template = json.dumps(template)
    event.template = json_template
    event.save()
    return Response({"message": "template added successfully"}, status=status.HTTP_200_OK)
    

@api_view(['PUT'])
@event_head_required
def add_header_image(request, id):
    try:
        event = Event.objects.get(id=id)
    except Event.DoesNotExist:
        return Response({"message": "event does not exist"}, status=status.HTTP_404_NOT_FOUND)
    if event.team.event_head.user != request.user:
        return Response({"message": "you are not allowed to perform this action"}, status=status.HTTP_403_FORBIDDEN)
    data = request.data
    header_image = data.get('header_image')
    event.header_image = header_image
    event.save()
    return Response({"message": "header image added successfully"}, status=status.HTTP_200_OK)
