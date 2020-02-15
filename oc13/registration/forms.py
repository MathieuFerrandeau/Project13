"""Register forms"""
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    """manages registration"""
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ConnexionForm(forms.Form):
    """manages the connection"""
    username = forms.CharField(label="Nom d'utilisateur",
                               max_length=30)
    password = forms.CharField(label="Mot de passe",
                               widget=forms.PasswordInput)


class AccountUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.exclude(pk=self.instance.pk).get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('Email "%s" is already used.' % email)  # pragma: no cover

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.exclude(pk=self.instance.pk).get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError('Username "%s" is already used.' % username)  # pragma: no cover


class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
