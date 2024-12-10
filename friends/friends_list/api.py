from django.shortcuts import render
from django.http import Http404

from rest_framework.response import Response
from rest_framework.views import APIView


from . import serializers
from . import models

class FriendList(APIView):
    def get(self, request):
        friends = models.Friend.objects.all()
        serializer = serializers.FriendSerializer(friends, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = serializers.FriendSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
class FriendDetail(APIView):

    def get_object(self, pk):
        try:
            return models.Friend.objects.get(pk=pk)
        except models.Friend.DoesNotExist:
            raise Http404


    def get(self, request, pk):
        friend = self.get_object(pk)
        serializer = serializers.FriendSerializer(friend)
        return Response(serializer.data)
    
    def put(self, request, pk):
        friend = self.get_object(pk)
        serializer = serializers.FriendSerializer(friend, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def delete(self, request, pk):
        friend = models.Friend.objects.get(pk=pk)
        friend.delete()
        return Response(status=204)