from django.db import models
from django.utils.translation import gettext, gettext_lazy as _


class ContactPerson(models.Model):
    """
    A person with contact information
    """
    firstname = models.CharField(
        max_length=200,
        verbose_name=_("First name"),
    )
    lastname = models.CharField(
        max_length=200,
        verbose_name=_("Last name"),
    )
    phonenumber = models.CharField(
        max_length=30,
        verbose_name=_("Phone number"),
    )
    emailaddress = models.CharField(
        max_length=200,
        verbose_name=_("Email address"),
    )
