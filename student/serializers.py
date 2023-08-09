from rest_framework.serializers import ModelSerializer
from .models import Student, StudentTeam, StudentEventApplication, StudentTeamEventApplictaion
from event.serializers import EventSerializer


class StudentSerializer(ModelSerializer):
    events = EventSerializer(many=True)

    class Meta:
        model = Student
        fields = '__all__'


class StudentTeamSerializer(ModelSerializer):
    members = StudentSerializer(many=True)
    event = EventSerializer()

    class Meta:
        model = StudentTeam
        fields = '__all__'


class StudentEventApplicationSerializer(ModelSerializer):
    student = StudentSerializer()
    event = EventSerializer()

    class Meta:
        model = StudentEventApplication
        fields = '__all__'


class StudentTeamEventApplictaionSerializer(ModelSerializer):
    team = StudentTeamSerializer()
    event = EventSerializer()

    class Meta:
        model = StudentTeamEventApplictaion
        fields = '__all__'
