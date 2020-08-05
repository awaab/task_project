from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(_("age"), null=True)
    phone_number = models.CharField(max_length=12)
