from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class SignUpForm(UserCreationForm):
    user_registration_file = forms.FileField(required=False)

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'user_registration_file',
            )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
