from django.db import models
from django.contrib.auth.models import User


class IMAPHost(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    port = models.IntegerField(
        null=True,
        blank=True,
    )

    ssl = models.BooleanField(default=True)

    public = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name
