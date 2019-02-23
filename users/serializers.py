from django.contrib.auth.models import User
from rest_framework import serializers




class MeSerializer(serializers.ModelSerializer):
    
    class Meta():
        model = User
        fields = (
            'id',
            'username',
            'last_name',
            'first_name'
        )

class MeFullSerializer(serializers.ModelSerializer):
    
    class Meta():
        model = User
        fields = (
            'id',
            'username',
            'last_name',
            'first_name',
            'email',
        )