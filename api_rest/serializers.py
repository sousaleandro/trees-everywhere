from rest_framework import serializers

from .models import User

# User serializer with all fields, there is no usage for this now but I'm starting to work with serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
