from rest_framework.serializers import ModelSerializer
from .models import Event, Judge, Mentor, Speaker, Sponsor, EventPicture, Category
from organizer.serializers import OrganizingTeamSerializer


class JudgeSerializer(ModelSerializer):
    class Meta:
        model = Judge
        fields = '__all__'


class MentorSerializer(ModelSerializer):
    class Meta:
        model = Mentor
        fields = '__all__'


class SpeakerSerializer(ModelSerializer):
    class Meta:
        model = Speaker
        fields = '__all__'


class SponsorSerializer(ModelSerializer):
    class Meta:
        model = Sponsor
        fields = '__all__'


class EventPictureSerializer(ModelSerializer):
    class Meta:
        model = EventPicture
        fields = '__all__'


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class EventSerializer(ModelSerializer):

    judges = JudgeSerializer(many=True)
    mentors = MentorSerializer(many=True)
    speakers = SpeakerSerializer(many=True)
    sponsors = SponsorSerializer(many=True)
    pictures = EventPictureSerializer(many=True)
    category = CategorySerializer()
    team = OrganizingTeamSerializer()

    class Meta:
        model = Event
        fields = '__all__'













