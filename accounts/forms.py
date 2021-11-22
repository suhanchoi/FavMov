from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import User
from django import forms


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields

class FondForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['like_genres', 'hate_genres', 'like_movies']
