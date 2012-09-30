from django.shortcuts import render_to_response
from django.template import RequestContext
from django import forms
from django.forms.models import modelformset_factory
from django.core import serializers
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
#from django.views.decorators.csrf import csrf_protect
from models import *
from forms import *

def index(request):
	"""
	home page
	"""
	if request.method == 'POST':
		formset = PersonForm(request.POST, request.FILES)
		if formset.is_valid():
			formset.save()	
			#add tags
	else:
		p = Person()
		formset = PersonForm(instance=p)

	a=Person.objects.all()

	return render_to_response('mainapp/templates/index.html',{'persons':a,'formset':formset}, context_instance=RequestContext(request))

def login(request):
	if request.method == 'POST':
		formset = LoginForm(request.POST)
		if formset.is_valid():
			#authenticate user
			user = authenticate(username=formset.user, password=formset.password)
			#check user
			if user is not None:
				if user.is_active:
					login(request, user)
				else:
					print 'error'
	else:
		formset = LoginForm()

	return render_to_response('mainapp/templates/login.html',{'formset':formset},context_instance=RequestContext(request))


def tags(request):
	TagsFormSet = modelformset_factory(Tag)

	if request.method == 'POST':
		formset = TagsFormSet(request.POST)

		if formset.is_valid():
			formset.save()
	else:
		formset = TagsFormSet()

	a=Tag.objects.all()
	return render_to_response('mainapp/templates/tags.html',{'tags':a,'formset':formset}, context_instance=RequestContext(request))

def groups(request):
	GroupsFormSet = modelformset_factory(Group)

	if request.method == 'POST':
		formset = GroupsFormSet(request.POST)

		if formset.is_valid():
			formset.save()
	else:
		formset = GroupsFormSet()

	a=Group.objects.all()
	return render_to_response('mainapp/templates/groups.html',{'groups':a,'formset':formset}, context_instance=RequestContext(request))

@login_required
def showid(request,name_id):
	"""
	select row
	"""
	a=Person.objects.get(id=name_id)
	if a:
		t=a.tags.all()
	else:
		t=[]
	return render_to_response('mainapp/templates/show.html',{'person':a,'tags':t}, context_instance=RequestContext(request))
	
def json_person(request):
	a=Person.objects.all()
	json_serializer = serializers.get_serializer("json")()
	res = json_serializer.serialize(a,ensure_ascii=False, indent=2, use_natural_keys=True)
	return HttpResponse(res, mimetype="application/json")
	
def json_tag(request):
	a=Tag.objects.all()
	json_serializer = serializers.get_serializer("json")()
	res = json_serializer.serialize(a,ensure_ascii=False, indent=2, use_natural_keys=True)
	return HttpResponse(res, mimetype="application/json")

def xml_test(request):
	a=Tag.objects.all()
	xml=serializers.serialize('xml',a)
	return HttpResponse(xml,mimetype='application/xml')


