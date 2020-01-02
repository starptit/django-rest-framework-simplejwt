from django.conf import settings
from django.db import models
from mongoengine import Document, fields, CASCADE
from django_mongoengine.mongo_auth.models import AbstractUser


class OutstandingToken(Document):
    user = fields.ReferenceField(AbstractUser, reverse_delete_rule=CASCADE, null=True, blank=True)

    jti = fields.StringField(unique=True, max_length=255)
    token = fields.StringField()

    created_at = fields.DateTimeField(null=True, blank=True)
    expires_at = fields.DateTimeField()

    class Meta:
        # Work around for a bug in Django:
        # https://code.djangoproject.com/ticket/19422
        #
        # Also see corresponding ticket:
        # https://github.com/encode/django-rest-framework/issues/705
        abstract = 'rest_framework_simplejwt.token_blacklist' not in settings.INSTALLED_APPS
        ordering = ('user',)

    def __str__(self):
        return 'Token for {} ({})'.format(
            self.user,
            self.jti,
        )


class BlacklistedToken(Document):
    token = fields.ReferenceField(OutstandingToken, reverse_delete_rule=CASCADE)

    blacklisted_at = fields.DateTimeField(auto_now_add=True)

    class Meta:
        # Work around for a bug in Django:
        # https://code.djangoproject.com/ticket/19422
        #
        # Also see corresponding ticket:
        # https://github.com/encode/django-rest-framework/issues/705
        abstract = 'rest_framework_simplejwt.token_blacklist' not in settings.INSTALLED_APPS

    def __str__(self):
        return 'Blacklisted token for {}'.format(self.token.user)
