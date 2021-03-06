from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q, Count
from django.core import serializers
import hashlib
import datetime
import time

# Follow Natural Keys
def getNaturalKeys(d):
	o = {}
	for k, v in d.items():
		if '_' not in k:
			o[k] = v
	return o


#when deserializing
class TagManager(models.Manager):
	def get_by_natural_key(self, id):
		return self.get(id = id)


class Video(models.Model):
	title = models.CharField(max_length = 250)
	url = models.CharField(max_length = 250)

	def __unicode__(self):
		return self.title


class Location(models.Model):
	"""
	Use google maps
	"""
	longitude = models.FloatField()
	latitude = models.FloatField()
	#cache google json response
	cache = models.TextField(default = "{}", null = True)

	def getCache(self):
		serializers.deserialize("json", self.cache)


class Tag(models.Model):
	#objects = TagManager()

	name = models.CharField(max_length = 200)

	def __unicode__(self):
		return self.name

	def natural_key(self):
		return getNaturalKeys(self.__dict__)

	class Meta:
		ordering = ('name',)


class Picture(models.Model):
	title = models.CharField(max_length = 250)
	tag = models.ManyToManyField(Tag, verbose_name = "list of tags")
	resource = models.CharField(max_length = 250)

	def __unicode__(self):
		return self.title


class Group(models.Model):
	name = models.CharField(max_length = 200)
	description = models.CharField(max_length = 200)

	def __unicode__(self):
		return self.name


class Person(models.Model):
	LEVELS = (
	(0, 'Member'),
	(1, 'Silver'),
	(2, 'Gold'),
	)
	DEF = 0

	user = models.ForeignKey(User, null = True)
	username = models.CharField(max_length = 50)
	name = models.CharField(max_length = 200)
	surname = models.CharField(max_length = 200)
	email = models.CharField(max_length = 200, default = '', null = True)
	phone = models.CharField(max_length = 50)
	tags = models.ManyToManyField(Tag, verbose_name = "Tags", null = True)
	groups = models.ForeignKey(Group, verbose_name = "Groups")
	level = models.SmallIntegerField(choices = LEVELS, default = DEF)
	img = models.ImageField(upload_to = "pictures/%Y/%m/%d", null = True, blank = True)
	location = models.ForeignKey(Location, null = True) #gmap json object
	credits = models.IntegerField(default = 0) #cache obj, calculated from history

	def Meta(self):
		ordering = ["name"]

	def save(self, *args, **kwargs):
		if not self.user:
			#create a new user, set an automatic password, confirmation email
			t = int(time.time()*1000)
			password = hashlib.sha1("%s" %  t).hexdigest()
			u = User.objects.create_user(self.username, self.email, password)
			u.save()
			#selet user
			self.user = u

		super(Person, self).save(*args, **kwargs)

	def addCredits(self, credits):
		self.credits += credits

	def rmCredits(self, credits):
		self.credits -= credits

	def is_gold(self):
		if self.level == 2:
			return True
		else:
			return False

	@classmethod
	def filterTags(cls, tags):
		return cls.objects.filter( tags__in = Tag.objects.filter( id__in = tags ) )

	def __unicode__(self):
		return self.name


class Event(models.Model):
	people = models.ManyToManyField(Person, verbose_name = "list of people", )
	name = models.CharField(max_length = 50)
	description = models.TextField()
	address = models.CharField(max_length = 250)
	ts = models.DateTimeField(auto_now_add = True)

	def __unicode__(self):
		return self.name

class Job(models.Model):
	LEVELS = (
		(0, 'Sent'),
		(1, 'Received'),
		(2, 'Approved'),
		(3, 'Done'),
		(4, 'Raise')
	)
	DEF = 0
	name = models.CharField(max_length=250)
	description = models.TextField()
	customer = models.ForeignKey(Person, related_name = 'job_customer')
	worker = models.ForeignKey(Person, related_name = 'job_worker')
	credits = models.SmallIntegerField(default=1)
	start_ts = models.DateTimeField()
	stop_ts = models.DateTimeField()
	ts = models.DateTimeField(auto_now_add = True)
	secret = models.CharField(max_length=250)
	status = models.SmallIntegerField(choices = LEVELS, default = DEF)

	def __unicode__(self):
		return "%s" % self.name

class Score(models.Model):
	voter = models.ForeignKey(Person, related_name = 'score_voter')
	voted = models.ForeignKey(Person, related_name = 'score_voted')
	stars = models.SmallIntegerField()
	ts = models.DateTimeField(auto_now_add = True)

	def __unicode__(self):
		return "%s" % self.stars


class Message(models.Model):
	sender = models.ForeignKey(Person, related_name = 'message_sender')
	destination = models.ForeignKey(Person, related_name = 'message_destination')
	message = models.TextField()
	status = models.SmallIntegerField(default = 0)
	ts = models.DateTimeField(auto_now_add = True)
	replied = models.DateTimeField(auto_now = True)

	def __unicode__(self):
		return self.message

	class Meta:
		ordering = ('id',)

	def setRead(self):
		self.status = 1
		self.save()

	@classmethod
	def getMessages(cls, uid):
		return cls.objects.filter(destination = uid).order_by("destination", "status", "-id").distinct("destination")

	@classmethod
	def getAllMessages(cls, uid):
		return cls.objects.filter(Q(sender = uid) | Q(destination = uid)).order_by("-id")

	@classmethod
	def getUnreadCounter(cls, uid):
		#cnt = cls.objects.filter(destination = uid, status = 0).annotate(cnt = Count('id'))[0].cnt
		return len(cls.objects.filter(destination = uid, status = 0))

	@classmethod
	def sendMatchMessage(cls, sender, destination):
		m = cls(sender = sender, destination = destination, message = "I Fancy you too!")
		m.save()


class Match(models.Model):
	sender = models.ForeignKey(Person, related_name = 'request_sender')
	destination = models.ForeignKey(Person, related_name = 'request_destination')
	status = models.SmallIntegerField(default = 0)
	ts = models.DateTimeField(auto_now_add = True)

	@classmethod
	def createMatch(cls, sender, destination):
		#verify if already sent
		try:
			res = cls.objects.get(sender = sender, destination = destination)
		except:
			#save
			res = cls(sender = sender, destination = destination)
			res.save()
		else:
			res = False
		#
		return res

	@classmethod
	def getFans(cls, uid):
		return cls.objects.filter(destination = uid, status__lte = 1).order_by("-id")

	@classmethod
	def getFansCounter(cls, uid):
		return len(cls.objects.filter(destination = uid, status = 0).order_by("-id"))

	@classmethod
	def setAccepted(cls, sender, destination):
		res = cls.objects.get(sender = destination, destination = sender)
		res.status = 1
		res.save()

	@classmethod
	def setDismissed(cls, sender, destination):
		res = cls.objects.get(sender = destination, destination = sender)
		res.status = 2
		res.save()

