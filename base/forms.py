from django import forms
from django.contrib.auth.models import User
from . models import Profile

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email']

class ProfileUpdateForm(forms.Form):
    class Meta:
        model = Profile
        fields = ['name','bio','avatar','location','profession']