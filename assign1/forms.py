from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class SignUpForm(UserCreationForm):
    user_registration_file = forms.FileField()

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'user_registration_file',
            )
        
    def clean_user_registration_file(self):
        file = self.cleaned_data.get("user_registration_file", False)
        if not file:
            return file
        content_type = file.content_type
        if not content_type == 'application/pdf':
            raise forms.ValidationError(_('Filetype not supported. Only pdf files are supported.'))
        return file

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = (
            'username', 'password',
            )