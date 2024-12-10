from rest_framework import serializers
from .models import Friend


class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = ['id', 'name', 'email', 'mobile', 'created_at', 'updated_at']
        read_only_fields = ('user',)