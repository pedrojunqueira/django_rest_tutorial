from django.urls import path

from .api import (
                    FriendList,
                    FriendDetail
                  )

urlpatterns = [
    path("friends/", FriendList.as_view(), name="friend_list"),
    path("friends/<int:pk>/", FriendDetail.as_view(), name="friend_detail"),
]