from django.conf import settings
from models import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core import serializers
import os.path
import urllib, urllib2
from django.utils.encoding import smart_str
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.mail import send_mail

def getAbsPath():
	return os.path.abspath(os.path.dirname(__file__))

def getRelPath():
	return getAbsPath().split("/").pop()

def render_page(request, template, data, menu = "home"):
	"""
	shortcut to render template
	"""
	#add user datails
	user = getUser(request)
	#get unread messages
	m_counter = Message.getUnreadCounter(user)
	f_counter = Match.getFansCounter(user)
	#
	data['MENU'] = menu
	data['SUBMENU'] = "subnav/%s.html" % menu
	data['USER'] = user
	#get group level
	if user:
		data['LEVEL'] = user.level
	else:
		data['LEVEL'] = -1
	#
	data['MESSAGE_COUNTER'] = m_counter
	data['MATCH_COUNTER'] = f_counter
	#
	data['TEMPLATE'] = template
	data['APP_PATH']= "/%s/" % getRelPath()
	print os.path.abspath(os.path.dirname(__file__))
	#
	return render_to_response('%s/templates/%s.html' % (getAbsPath(), template),
	                          data,
	                          context_instance = RequestContext(request))

def getUser(request):
	if request.user.is_authenticated():
		try:
			uid = request.session["uid"]
		except:
			uid = Person.objects.get(username = request.user)
			#save into session
			request.session["uid"] = uid
		return uid
	else:
		return None

def send_email(subject, template, person):
	f =  settings.GENERAL_EMAIL
	body = render_to_string('%s/templates/%s.html' % (getAbsPath(), template), person)
	send_mail(subject , body, f,[ person.email ], fail_silently=False)


def get_lat_lng(location):
	# Reference: http://djangosnippets.org/snippets/293/
	# https://gist.github.com/1372541

	location = urllib.quote_plus(smart_str(location))
	url = 'http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false' % location
	response = urllib2.urlopen(url).read()
	result = serializers.deserialize("json",response)
	if result['status'] == 'OK':
		lat = str(result['results'][0]['geometry']['location']['lat'])
		lng = str(result['results'][0]['geometry']['location']['lng'])
		return '%s,%s' % (lat, lng)
	else:
		return ''