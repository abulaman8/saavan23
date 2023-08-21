from rest_framework.serializers import ModelSerializer
from .models import Student, StudentTeam, StudentEventApplication, StudentTeamEventApplictaion
from event.serializers import EventSerializer, SimpleEventSerializer
from django.contrib.auth.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'groups', 'user_permissions', 'is_staff', 'is_active', 'is_superuser', 'last_login']


class StudentSerializer(ModelSerializer):
    events = SimpleEventSerializer(many=True)
    user = UserSerializer()

    class Meta:
        model = Student
        fields = '__all__'


class SimpleStudentSerializer(ModelSerializer):
    
    class Meta:
        model = Student
        fields = '__all__'


class StudentTeamSerializer(ModelSerializer):
    members = StudentSerializer(many=True)
    event = SimpleEventSerializer()

    class Meta:
        model = StudentTeam
        fields = '__all__'


class SimpleStudentTeamSerializer(ModelSerializer):

    class Meta:
        model = StudentTeam
        fields = '__all__'


class StudentEventApplicationSerializer(ModelSerializer):
    student = SimpleStudentSerializer()
    event = SimpleEventSerializer()

    class Meta:
        model = StudentEventApplication
        fields = '__all__'


class StudentTeamEventApplictaionSerializer(ModelSerializer):
    team = SimpleStudentTeamSerializer()
    event = SimpleEventSerializer()

    class Meta:
        model = StudentTeamEventApplictaion
        fields = '__all__'
