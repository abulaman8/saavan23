from rest_framework.serializers import ModelSerializer
from .models import EventHead, Organizer, OrganizingTeam


class EventHeadSerializer(ModelSerializer):
    class Meta:
        model = EventHead
        fields = '__all__' 


class OrganizerSerializer(ModelSerializer):
    class Meta:
        model = Organizer
        fields = '__all__'


class OrganizingTeamSerializer(ModelSerializer):

    event_head = EventHeadSerializer()
    organizers = OrganizerSerializer(many=True, read_only=True)

    class Meta:
        model = OrganizingTeam
        fields = '__all__'

  
