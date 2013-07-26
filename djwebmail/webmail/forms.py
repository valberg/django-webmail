from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from .models import IMAPHost


class LoginForm(AuthenticationForm):

    host = forms.ModelChoiceField(
        queryset=IMAPHost.objects.filter(public=True)
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        host = self.cleaned_data.get('host')

        if username and password and host:
            self.user_cache = authenticate(
                username=username,
                password=password,
                host=host,
            )
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            elif not self.user_cache.is_active:
                raise forms.ValidationError(
                    self.error_messages['inactive'],
                    code='inactive',
                )

        return self.cleaned_data
