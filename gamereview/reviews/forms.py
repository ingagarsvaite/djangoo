from .models import GameReview
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User

class GameReviewForm(forms.ModelForm):
    class Meta:
        model = GameReview
        fields = ('reviewer', 'game', 'content', 'rating')
        widgets = {'game': forms.HiddenInput(
        ), 'reviewer': forms.HiddenInput()}

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
