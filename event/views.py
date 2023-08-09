from oauth2_provider.models import AccessToken, RefreshToken
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
        CategorySerializer

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
    return wrap


@api_view(['POST'])
@event_head_required
def create_event(request):
    data = request.data
    print(data)
    judges = data.pop('judges', None)
    speakers = data.pop('speakers', None)
    mentors = data.pop('mentors', None)
    sponsors = data.pop('sponsors', None)
    team = data.pop('team', None)
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
    for judge in judges:
        judge_instances.append(Judge.objects.get_or_create(**judge)[0])
    for speaker in speakers:
        speaker_instances.append(Speaker.objects.get_or_create(**speaker)[0])
    for mentor in mentors:
        mentor_instances.append(Mentor.objects.get_or_create(**mentor)[0])
    for sponsor in sponsors:
        sponsor_instances.append(Sponsor.objects.get_or_create(**sponsor)[0])
    for organizer in team:
        organizer_instances.append(Organizer.objects.get_or_create(**organizer)[0])

    organizing_team = OrganizingTeam.objects.create(event_head=event_head)
    organizing_team.organizers.set(organizer_instances)
    data['team'] = organizing_team
    event = Event.objects.create(**data)
    event.judges.set(judge_instances)
    event.speakers.set(speaker_instances)
    event.mentors.set(mentor_instances)
    event.sponsors.set(sponsor_instances)
    return Response({"message": "event created successfully!!!"}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_events(request):
    events = Event.objects.all()
    serializer = EventSerializer(events, many=True)
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

    judges = data.pop('judges', None)
    speakers = data.pop('speakers', None)
    mentors = data.pop('mentors', None)
    sponsors = data.pop('sponsors', None)
    team = data.pop('team', None)
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
    for judge in judges:
        judge_instances.append(Judge.objects.get_or_create(**judge)[0])
    for speaker in speakers:
        speaker_instances.append(Speaker.objects.get_or_create(**speaker)[0])
    for mentor in mentors:
        mentor_instances.append(Mentor.objects.get_or_create(**mentor)[0])
    for sponsor in sponsors:
        sponsor_instances.append(Sponsor.objects.get_or_create(**sponsor)[0])
    for organizer in team:
        organizer_instances.append(Organizer.objects.get_or_create(**organizer)[0])

    organizing_team = OrganizingTeam.objects.get_or_create(event_head=event_head)[0]
    organizing_team.organizers.set(organizer_instances)
    data['team'] = organizing_team
    event = Event.objects.create(**data)
    event.judges.set(judge_instances)
    event.speakers.set(speaker_instances)
    event.mentors.set(mentor_instances)
    event.sponsors.set(sponsor_instances)
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

