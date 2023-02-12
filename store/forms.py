from django import forms
from .models import *

class CustomerForm(forms.ModelForm):
	class Meta:
		model = Customer
		exclude = ("date_updated", "date_created",)