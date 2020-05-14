from django import forms
from django.forms import ModelForm

from .models import *

class ChatForm(forms.ModelForm):
	title = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "enter your query"}
        ),
    )
	class Meta:
		model = Chatbot
		fields = [ "title", ]