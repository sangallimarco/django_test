from django.shortcuts import redirect
from django.forms.models import modelformset_factory
from django.core import serializers
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
#from django.views.decorators.csrf import csrf_protect

from models import *
from forms import *
from utils import *


def index(request):
	"""
	home page
	"""
	if request.method == 'POST':
		formset = PersonForm(request.POST, request.FILES)
		if formset.is_valid():
			#create a new Person and a new User and link them
			try:
				formset.save()
			except:
				print "duplicated keys"
			else:
				return redirect('/mainapp/index/')
			#add tags
	else:
		p = Person()
		formset = PersonForm(instance = p)

	a = Person.objects.all()

	return render_page(request, 'index.html', {'list':a, 'formset':formset})


def log_in(request):
	if request.method == 'POST':
		formset = LoginForm(request.POST)
		if formset.is_valid():
			#authenticate user
			data = formset.cleaned_data
			user = authenticate(username = data['user'], password = data['password'])
			#check user
			if user is not None:
				if user.is_active:
					login(request, user)
					#goto index
					return redirect('/mainapp/index/')
	else:
		formset = LoginForm()

	return render_page(request, 'login.html', {'formset':formset})


def log_out(request):
	logout(request)
	#goto index
	return redirect('/mainapp/index/')


def tags(request):
	TagsFormSet = modelformset_factory(Tag)

	if request.method == 'POST':
		formset = TagsFormSet(request.POST)

		if formset.is_valid():
			formset.save()
	else:
		formset = TagsFormSet()

	a = Tag.objects.all()

	return render_page(request, 'tags.html', {'list':a, 'formset':formset})


def groups(request):
	GroupsFormSet = modelformset_factory(Group)

	if request.method == 'POST':
		formset = GroupsFormSet(request.POST)

		if formset.is_valid():
			formset.save()
	else:
		formset = GroupsFormSet()

	a = Group.objects.all()

	return render_page(request, 'groups.html', {'list':a, 'formset':formset})


@login_required(login_url = '/mainapp/login/')
def messages(request):
	#get user id
	uid = getUserId(request)

	#filter messages, display only messages with destination = user
	list = Message.getMessages(uid)

	return render_page(request, 'messages.html', {'list':list})


@login_required(login_url = '/mainapp/login/')
def new_message(request, sender_id):
	#get user id
	user = getUser(request)
	#get destination
	try:
		dest = Person.objects.get(name = sender_id)
	except:
		return redirect('/mainapp/messages/')

	#print request.POST
	#
	if request.method == 'POST':
		formset = MessageForm(request.POST)
		#
		if formset.is_valid():
			#add sender
			f = formset.save(commit = False)
			f.sender = user
			f.destination = dest
			f.save()
			#
			return redirect('/mainapp/messages/')
		#add tags
	else:
		p = Message()
		formset = MessageForm(instance = p)

	return render_page(request, 'new_message.html', {'formset':formset, 'destination':dest.name})


def reply_message(request, message_id):
	#get user id
	user = getUser(request)
	#get destination
	try:
		message = Message.objects.get(id = message_id)
		dest = message.sender
	except:
		return redirect('/mainapp/messages/')
	else:
		#update to viewed
		message.status = 1
		message.save()
		#get list of related messages
		list = Message.getAllMessages(dest)

	#print request.POST
	#
	if request.method == 'POST':
		formset = MessageForm(request.POST)
		#
		if formset.is_valid():
			#add sender
			f = formset.save(commit = False)
			f.sender = user
			f.destination = dest
			f.save()
			#
			return redirect('/mainapp/messages/')
		#add tags
	else:
		p = Message()
		formset = MessageForm(instance = p)

	return render_page(request, 'new_message.html',
	                   {'formset':formset, 'destination':dest.name, 'list':list, 'message':message})


@login_required(login_url = '/mainapp/login/')
def showid(request, name_id):
	a = Person.objects.get(id = name_id)
	if a:
		t = a.tags.all()
	else:
		t = []

	return render_page(request, 'show.html', {'persons':a, 'tags':t})


@login_required(login_url = '/mainapp/login/')
def profile(request):
	#get user id
	a = getUser(request)
	print a.name
	#get tags
	if a:
		t = a.tags.all()
	else:
		t = []

	return render_page(request, 'show.html', {'person':a, 'tags':t})


def json_person(request):
	a = Person.objects.all()
	json_serializer = serializers.get_serializer("json")()
	res = json_serializer.serialize(a, ensure_ascii = False, indent = 2, use_natural_keys = True)
	return HttpResponse(res, mimetype = "application/json")


def json_tag(request):
	a = Tag.objects.all()
	json_serializer = serializers.get_serializer("json")()
	res = json_serializer.serialize(a, ensure_ascii = False, indent = 2, use_natural_keys = True)
	return HttpResponse(res, mimetype = "application/json")


def xml_test(request):
	a = Tag.objects.all()
	xml = serializers.serialize('xml', a)
	return HttpResponse(xml, mimetype = 'application/xml')


