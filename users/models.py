from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from tourism.models.timestamp import TimestampMdl

class UserAccountManager(BaseUserManager):

    def create_superuser(self, email, username, first_name, last_name, contact_no, password=None, **other_fields):
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_kyc', True)
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, first_name, last_name, contact_no, password, **other_fields)

    def create_user(self, email, username, first_name, last_name, contact_no, password=None, **other_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, first_name=first_name, last_name=last_name, contact_no=contact_no, **other_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, TimestampMdl, PermissionsMixin):
    # personal info
    first_name = models.CharField(max_length=150, verbose_name='First Name')
    last_name = models.CharField(max_length=150, verbose_name='Last Name')
    # contact info
    contact_no = models.CharField(max_length=10, verbose_name='Contact No.')
    email = models.EmailField(unique=True, verbose_name='Email')
    # creds
    username = models.CharField(max_length=150, unique=True, verbose_name='Username')
    # status
    is_active = models.BooleanField(default=False, verbose_name='Active')
    is_kyc = models.BooleanField(default=False, verbose_name='Identity Verified')
    is_staff = models.BooleanField(default=False, verbose_name='Team Member')
    is_superuser = models.BooleanField(default=False, verbose_name='Administrator')
    # blocked reason is_active=false
    msg = models.TextField(blank=True, null=True, verbose_name="Account blocked (reason)")

    objects = UserAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'contact_no']

    def __str__(self):
        return self.username
