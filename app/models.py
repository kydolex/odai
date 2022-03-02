from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager, PermissionsMixin
from stdimage.models import StdImageField
from mdeditor.fields import MDTextField
from accounts.models import CustomUser,UserManager


class Post(models.Model):
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	title = models.CharField("タイトル", max_length=200)
	content = models.TextField("本文")
	created = models.DateTimeField("作成日", default=timezone.now)


	def __str__(self):
		return self.title

class Post2(models.Model):
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	title = models.CharField("タイトル", max_length=200)
	content = models.TextField("本文")
	created = models.DateTimeField("作成日", default=timezone.now)


	def __str__(self):
		return self.title



class Title(models.Model):
	author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	title = models.TextField("タイトル", max_length=200)
	created = models.DateTimeField("作成日", default=timezone.now)
	def __str__(self):
		return self.title

class Odai(models.Model):
	author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	title = models.ForeignKey(Title, on_delete=models.CASCADE)
	odai = models.TextField("タイトル", max_length=200,null=True)
	created = models.DateTimeField("作成日", default=timezone.now)
	def __str__(self):
		return self.odai


class AddTitle(models.Model):
	author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	title = models.TextField("タイトル", max_length=200)
	created = models.DateTimeField("作成日", default=timezone.now)
	def __str__(self):
		return self.title

class AddOdai(models.Model):
	author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	title = models.ForeignKey(Title, on_delete=models.CASCADE)
	odai = models.TextField("タイトル", max_length=200,null=True)
	created = models.DateTimeField("作成日", default=timezone.now)
	def __str__(self):
		return self.odai
