import time

from django.contrib.auth.models import User
from django.conf import settings

from imapclient import IMAPClient


class IMAPAuthenticationBackend(object):

    def authenticate(self, username=None, password=None, host=None):

        if host:
            try:
                host_addr = host.address
                host_port = host.port
                host_ssl = host.ssl
            except:
                pass
        else:
            host_addr = settings.IMAP_DEFAULT_HOST
            host_port = settings.IMAP_DEFAULT_PORT
            host_ssl = settings.IMAP_DEFAULT_SSL

        try:
            server = IMAPClient(
                host_addr,
                port=host_port,
                ssl=host_ssl,
            )
            server.login(username, password)
            server.logout()
        except:
            return None

        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            user = User.objects.create_user(
                time.time(),
                username,
                'password-not-in-use',
            )

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
