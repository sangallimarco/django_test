from django.db import models

# Create your models here.
def getNaturalKeys(d):
	o={}
	for k,v in d.items():
		if '_' not in k:
			o[k]=v
	return o
#when deserializing
class TagManager(models.Manager):
	def get_by_natural_key(self, id):
		return self.get(id=id)

class Tag(models.Model):
	#objects = TagManager()
	
	name = models.CharField(max_length=200)
	
	def __unicode__(self):
		return self.name
	
	def natural_key(self):
		return getNaturalKeys(self.__dict__)
	
	class Meta:
		ordering = ('name',)

class Group(models.Model):
	LEVELS = (
		(0,'Member'),
		(1,'Silver'),
		(2,'Gold'),
	)
	DEF=0
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=200)
	level = models.SmallIntegerField(choices=LEVELS)

	def is_gold(self):
		if self.level == 0:
			return True
		else:
			return False

	def __unicode__(self):
		return self.name

class Person(models.Model):
	name = models.CharField(max_length=200)
	surname = models.CharField(max_length=200)
	tags = models.ManyToManyField(Tag, verbose_name="list of tags")
	groups = models.ManyToManyField(Group, verbose_name="list of groups")
	img = models.ImageField(upload_to="pictures/%Y/%m/%d", null=True, blank=True)

	def __unicode__(self):
		return self.name

class Event(models.Model):
	people = models.ManyToManyField(Person, verbose_name="list of people", )
	name = models.CharField(max_length=50)
	description = models.TextField()
	address = models.CharField(max_length=250)
	ts = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.name

class Score(models.Model):
	voter = models.ForeignKey(Person,related_name='score_voter')
	voted = models.ForeignKey(Person,related_name='score_voted')
	stars = models.SmallIntegerField()
	ts = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return "%s" % self.stars

class Message(models.Model):
	sender = models.ForeignKey(Person,related_name='message_sender')
	destination = models.ForeignKey(Person,related_name='message_destination')
	message = models.TextField()
	ts = models.DateTimeField(auto_now_add = True)

	def __unicode__(self):
		return self.message

class Picture(models.Model):
	title = models.CharField(max_length=250)
	tag = models.ManyToManyField(Tag, verbose_name="list of tags")
	resource = models.CharField(max_length=250)

	def __unicode__(self):
		return self.title

class Video(models.Model):
	title = models.CharField(max_length=250)
	url = models.CharField(max_length=250)

	def __unicode__(self):
		return self.title

class Geo(models.Model):
	title = models.CharField(max_length=250)
