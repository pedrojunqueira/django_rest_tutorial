from django.shortcuts import render
from django.http import Http404

from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


from . import serializers
from . import models

class FriendList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        friends = models.Friend.objects.all()
        serializer = serializers.FriendSerializer(friends, many=True)
        return Response(serializer.data)
    
    
    @swagger_auto_schema(
        request_body=serializers.FriendSerializer,
        responses={
            201: serializers.FriendSerializer,
            400: 'Bad Request'
        }
    )
    def post(self, request):
        serializer = serializers.FriendSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class FriendDetail(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return models.Friend.objects.get(pk=pk, user=user)
        except models.Friend.DoesNotExist:
            raise Http404


    def get(self, request, pk):
        friend = self.get_object(pk, user=request.user)
        serializer = serializers.FriendSerializer(friend)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        request_body=serializers.FriendSerializer,
        responses={
            200: serializers.FriendSerializer,
            400: 'Bad Request'
        }
    )
    def put(self, request, pk):
        friend = self.get_object(pk, user=request.user)
        serializer = serializers.FriendSerializer(friend, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        friend = models.Friend.objects.get(pk=pk, user=request.user)
        friend.delete()
        return Response(status=204)