from django.db import models
from django.contrib.auth.models import User




class Profile(models.Model):
	user = models.OneToOneField(User,  on_delete=models.CASCADE)
	fname = models.CharField(max_length = 30)
	lname = models.CharField(max_length = 30)
	phone = models.CharField(max_length = 100)
	usn = models.CharField(max_length = 100)
	college = models.CharField(max_length = 100)
	branch = models.CharField(max_length = 30)
	sem =  models.IntegerField()
	
	def __str__(self):
		return self.fname

class Club(models.Model):
	cname = models.CharField(max_length = 100)
	motto = models.CharField(max_length = 500)
	image = models.ImageField(upload_to = 'static/club_image')
	about = models.TextField()
	misson = models.TextField(blank = 'True')
	vission = models.TextField(blank = 'True')

	def __str__(self):
		return self.cname


class Member(models.Model):
	type_of_user = (
	('A', 'Admin'),
	('CA', 'College Admin'),
	('O', 'Others'))
	type_of_user = models.CharField(max_length = 10,choices = type_of_user, default = 'O' )
	profile = models.OneToOneField(Profile, on_delete = models.CASCADE)
	club = models.ManyToManyField(Club)
	def __str__(self):
		return self.profile.fname


class Event(models.Model):
	ename = models.CharField(max_length=100)
	club_name = models.ForeignKey(Club, on_delete = models.CASCADE)
	desc = models.TextField()
	image = models.ImageField(upload_to = 'static/event_image', blank = True)
	fees = models.IntegerField()
	date =models.DateField()

	def __str__(self):
		return self.ename


class Gallery(models.Model):
	ename = models.ForeignKey(Event, on_delete = models.CASCADE)
	images = models.ImageField(upload_to = 'static/gallery', blank = True)
	def __str__(self):
		return self.ename.ename



class Registered_members(models.Model):
	ename = models.ForeignKey(Event, on_delete = models.CASCADE)
	details = models.ForeignKey(Profile, on_delete = models.CASCADE)
	def __str__(self):
		return self.ename

class Request(models.Model):
	member = models.ForeignKey(Profile, on_delete = models.CASCADE)
	def __str__(self):
		return self.member.fname

class Club_request(models.Model):
	club_name = models.CharField(max_length = 30)
	desc  = models.CharField(max_length = 100)
	profile = models.ForeignKey(Profile, on_delete = models.CASCADE)

	def __str__(self):
		return self.club_name






	



