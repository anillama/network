from django.contrib import admin

# Register your models here.
from .models import User, Profile, LikesUnlikes, Following

class UserData(admin.ModelAdmin):
	list_display = ("username", "id")

class ProfileData(admin.ModelAdmin):
	list_display = ('id', 'userName', 'userBio', 'timestamp')

class LikesData(admin.ModelAdmin):
	list_display = ('countLikes', 'postId', 'userNameOnLU')

class FollowingData(admin.ModelAdmin):
	list_display = ('user', 'follStatu', 'following')

admin.site.register(User, UserData)
admin.site.register(Profile, ProfileData)
admin.site.register(LikesUnlikes, LikesData)
admin.site.register(Following, FollowingData)