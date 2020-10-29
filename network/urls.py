
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("postData", views.getPost, name="dataPost"),
    path("userInfo/<str:userId>", views.userInfo, name="userInfo"),
    path("follo/<str:userFollow>/<str:userFoller>", views.followIngo, name="followInfo"),
    path('followingPosts', views.followingPost, name="followingPosts"),
    path('updatepost/<int:post_id>', views.updatepost, name="updatepost"),
    path('likes/<int:likes_id>', views.checkLikes, name="checkLikes")
]
