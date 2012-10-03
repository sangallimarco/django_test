from django.conf import settings
from models import Person
from django.shortcuts import render_to_response
from django.template import RequestContext

def render_page(request, template, data):
	"""
	shortcut to render template
	"""

	#add user datails
	user = Person.objects.get(name = request.user)
	data['user']=user.name
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