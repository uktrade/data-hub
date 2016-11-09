from dateutil import parser
from django.conf import settings
from django.db import models
from django.utils.timezone import now
from rest_framework import status

from core.mixins import DeferredSaveModelMixin
from korben.exceptions import KorbenException


class BaseModel(DeferredSaveModelMixin, models.Model):
    """Common fields for most of the models we use."""

    archived = models.BooleanField(default=False)
    archived_on = models.DateTimeField(null=True)
    archived_reason = models.TextField(blank=True, null=True)
    archived_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
    created_on = models.DateTimeField(null=True, blank=True)
    modified_on = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def archive(self, user, reason=None):
        """Archive the model instance."""

        self.archived = True
        self.archived_by = user
        self.archived_reason = reason
        self.archived_on = now()
        self.save()

    def unarchive(self):
        """Unarchive the model instance."""

        self.archived = False
        self.archived_reason = ''
        self.archived_by = None
        self.archived_on = None
        self.save()

    def clean(self):
        """Custom validation for created_on and modified_on.

        If the fields are empty, populate them.
        """

        self.created_on = self.created_on if self.created_on else now()
        self.modified_on = self.modified_on if self.modified_on else now()

    def _map_korben_response_to_model_instance(self, korben_response):
        """Handle date time object."""
        if korben_response.status_code == status.HTTP_200_OK:
            for key, value in korben_response.json().items():
                setattr(self, key, value)
            self.archived_on = parser.parse(self.archived_on) if self.archived_on else self.archived_on
            self.modified_on = parser.parse(self.modified_on) if self.modified_on else self.modified_on
            self.created_on = parser.parse(self.created_on) if self.created_on else self.created_on
        elif korben_response.status_code == status.HTTP_404_NOT_FOUND:
            return
        else:
            raise KorbenException(korben_response.json())


class BaseConstantModel(models.Model):
    """Constant tables for FKs."""

    id = models.UUIDField(primary_key=True)
    name = models.TextField(blank=True)

    class Meta:
        abstract = True
        ordering = ('name', )

    def __str__(self):
        return self.name
