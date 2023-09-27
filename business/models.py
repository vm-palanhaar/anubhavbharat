from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _
from django.db import models

from tourism.models import TimestampModel

from users import models as UserModel


class OrgType(TimestampModel):
    entity = models.CharField(max_length=30, verbose_name='Entity')
    doc = models.CharField(max_length=30, verbose_name='Document')
    desc = models.TextField(verbose_name='Description')
    def __str__(self):
        return self.entity


def upload_to_org(instance,filename):
    folder_name = f'{instance.name}_{instance.created_at}'
    return f'business/org/{folder_name}/{filename}'

class Org(TimestampModel):
    type = models.ForeignKey(OrgType, on_delete=models.CASCADE, verbose_name='Type')
    name = models.CharField(max_length=60, verbose_name='Name')
    reg_no = models.CharField(max_length=30, unique=True, verbose_name='Registration No')
    doc = models.FileField(_('Document'), upload_to=upload_to_org, 
            validators=[FileExtensionValidator(allowed_extensions=["pdf"])])
    is_active = models.BooleanField(default=False, verbose_name='Active')
    is_verified = models.BooleanField(default=False, verbose_name='Verified')
    def __str__(self):
        return self.name


class OrgEmp(TimestampModel):
    org = models.ForeignKey(Org, on_delete=models.CASCADE, verbose_name='Organization')
    user = models.ForeignKey(UserModel.User, on_delete=models.CASCADE, verbose_name='User')
    is_manager = models.BooleanField(default=False, verbose_name='Manager')
    is_delete = models.BooleanField(default=False, verbose_name='Delete')
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
