from django.shortcuts import render_to_response
from django.template import RequestContext
from mainapp.models import *
from django import forms
from django.forms.models import modelformset_factory
from django.core import serializers
from django.http import HttpResponse
# Create your views here.

class TestForm(forms.Form):
	name=forms.CharField(max_length=200)
	surname=forms.CharField(max_length=200)

class PersonForm(forms.ModelForm):
	class Meta:
		model = Person


def index(request):
	"""
	home page
	"""
	PersonFormSet = modelformset_factory(Person)

	if request.method == 'POST':
		formset = PersonFormSet(request.POST)
		#form = PersonForm(request.POST)
		if formset.is_valid():
			formset.save()	
			#add tags
	else:
		#formset = PersonFormSet(queryset=Person.objects.filter(name__startswith='O'))
		formset = PersonFormSet(queryset=Person.objects.filter(name__startswith='---'))
	
	a=Person.objects.all()
	return render_to_response('mainapp/templates/index.html',{'persons':a,'formset':formset}, context_instance=RequestContext(request))

def index_bs(request):
	"""
	home page
	"""
	PersonFormSet = modelformset_factory(Person)

	if request.method == 'POST':
		formset = PersonFormSet(request.POST)
		#form = PersonForm(request.POST)
		if formset.is_valid():
			formset.save()
		#add tags
	else:
		#formset = PersonFormSet(queryset=Person.objects.filter(name__startswith='O'))
		formset = PersonFormSet(queryset=Person.objects.filter(name__startswith='---'))

	a=Person.objects.all()
	return render_to_response('mainapp/templates/index.html',{'persons':a,'formset':formset}, context_instance=RequestContext(request))


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


