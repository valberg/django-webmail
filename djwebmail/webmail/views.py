from django.views import generic
from django.conf import settings
from django.contrib.auth import authenticate, login, REDIRECT_FIELD_NAME
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.http import is_safe_url
from django.shortcuts import resolve_url
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


from . import forms
from . import models
from .encrypt import encrypt, decrypt

from imapclient import IMAPClient


class ListMessages(generic.TemplateView):
    template_name = 'webmail/message_list.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ListMessages, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(ListMessages, self).get_context_data(*args, **kwargs)

        host = models.IMAPHost.objects.get(pk=self.request.session.get('host'))

        connection = IMAPClient(
            host.address,
            port=host.port,
            ssl=host.ssl,
        )

        connection.login(
            self.request.session.get('username'),
            decrypt(self.request.session.get('password'))
        )

        context['folders'] = connection.list_folders()

        return context


class Login(generic.FormView):

    form_class = forms.LoginForm
    template_name = 'webmail/login_form.html'

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        host = form.cleaned_data.get('host')

        redirect_to = self.request.REQUEST.get(REDIRECT_FIELD_NAME, '')

        # Ensure the user-originating redirection url is safe.
        if not is_safe_url(url=redirect_to, host=self.request.get_host()):
            redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

        if username and password and host:
            user = authenticate(
                username=username,
                password=password,
                host=host,
            )

            if user is not None:
                if user.is_active:
                    login(self.request, user)

                    self.request.session['username'] = username
                    self.request.session['password'] = encrypt(password)
                    self.request.session['host'] = host.id

                    return HttpResponseRedirect(redirect_to)

                else:
                    # User is not active
                    messages.error(self.request, _(u'User is disabled.'))
                    return HttpResponse(200, "User disabled")
            else:
                # Login failed
                messages.error(self.request, _(u'Authentication failed.'))
                return HttpResponse(200, "Login failed")
        else:
            return HttpResponse(200, "Missing info")
