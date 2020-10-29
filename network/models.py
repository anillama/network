from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    pass

class Profile(models.Model):
	userName = models.CharField(max_length=65)
	userBio = models.CharField(max_length=250, null=True, blank=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	def serialize(self):
		return {
			"user" : self.userName,
			"post" : self.userBio
		}

class LikesUnlikes(models.Model):
	userNameOnLU = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	postId = models.IntegerField()
	countLikes = models.BooleanField(default=False)

	def seialize(self):
		return {
			"id": self.id,
			"postId": self.postId,
			"countLikes": self.countLikes
		}

class Following(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	follower = models.ManyToManyField(Profile)
	follStatu = models.CharField(max_length=30) #Main user
	following = models.CharField(max_length=30) #Followers

	def __str__(self):
		return f"{self.user}, {self.follStatu}, {self.following}"
  