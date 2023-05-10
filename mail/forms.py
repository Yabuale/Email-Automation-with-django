from django import forms
from .models import Member

class UserForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['firstname', 'email', ]