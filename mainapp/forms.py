from models import *
from django import forms

class TestForm(forms.Form):
	name = forms.CharField(max_length = 200)
	surname = forms.CharField(max_length = 200)


class PersonForm(forms.ModelForm):
	class Meta:
		model = Person
		exclude = ('user', 'level', 'location', 'credits')

class ProfileForm(forms.ModelForm):
	class Meta:
		model = Person
		exclude = ('name', 'user', 'level', 'credits')

class LoginForm(forms.Form):
	user = forms.CharField(max_length = 200)
	password = forms.CharField(max_length = 200, widget = forms.PasswordInput)


class MessageForm(forms.ModelForm):
	class Meta:
		model = Message
		exclude = ('status', 'sender', 'destination')


class TagForm(forms.ModelForm):
	class Meta:
		model = Tag