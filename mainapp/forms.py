from models import *
from django import forms

class TestForm(forms.Form):
	name=forms.CharField(max_length=200)
	surname=forms.CharField(max_length=200)

class PersonForm(forms.ModelForm):
	class Meta:
		model = Person

class LoginForm(forms.Form):
	name=forms.CharField(max_length=200)
	password=forms.CharField(max_length=200)