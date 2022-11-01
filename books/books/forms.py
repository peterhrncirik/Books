from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db.models import fields

from .models import User, Book, Ratings, Message

class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'district',]
        fields = ['username', 'email', 'password1', 'password2', 'district',]

        help_texts = {
            'username': None,
            'district': 'Mentioning districts helps you connect with other users in your area.'
        }

        labels = {
            'district': 'Bezirk',
        }

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']

        widgets = {
            'password': forms.PasswordInput()
        }

        # labels = {
        #     'email': 'Ihre E-mail',
        #     'password': 'Passwort',
        # }

class UpdateAccountForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'district', 'mobile', 'about_me', 'is_private']

        # changing email disabled for now
        exclude = ('email',)

        labels = {
            'is_private': 'Make my account private',
            'district': 'District',
            'about_me': 'About me',
        }

class SellBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'category', 'language', 'ISBN']

class ContactUsForm(forms.Form):
    name = forms.CharField(label='Your name', max_length=100)
    email = forms.EmailField(label='Your e-mail')
    message = forms.CharField(widget=forms.Textarea)

class RateUserForm(forms.ModelForm):

    class Meta:
        model = Ratings
        fields = ['rating', 'comment']

        labels = {
            'comment': 'Would you like to add anything else?',
        }

class MessageUserForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = ['message']