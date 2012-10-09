from django.conf import settings
from models import *
from django.shortcuts import render_to_response
from django.template import RequestContext
import os.path

def render_page(request, template, data):
	"""
	shortcut to render template
	"""

	#add user datails
	print request.user
	if request.user.is_authenticated():
		user = Person.objects.get(name = request.user)
	else:
		user = None
	#get unread messages
	counter = Message.getUnreadCounter(user)
	#
	data['user'] = user
	data['counter'] = counter
	data['APP_PATH']= "/%s/" % os.path.abspath(os.path.dirname(__file__)).split("/").pop()
	#
	return render_to_response('mainapp/templates/%s' % template,
	                          data,
	                          context_instance = RequestContext(request))


def getUserId(request):
	"""
	get current user id
	"""
	uid = Person.objects.get(name = request.user)
	if uid:
		return uid.pk
	else:
		return None


def getUser(request):
	uid = Person.objects.get(name = request.user)
	if uid:
		return uid
	else:
		return None