from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _
from django.db import models
import uuid

from tourism.models.timestamp import TimestampMdl

from users import models as UserModel


class OrgDocType(TimestampMdl):
    doc = models.CharField(max_length=90, verbose_name='Document')
    doc_no = models.CharField(max_length=120, verbose_name='Document Number')
    desc = models.TextField()
    is_doc = models.BooleanField(default=False, verbose_name="Document Required")
    def __str__(self):
        return f'{self.doc} - {self.doc_no}'

class OrgType(TimestampMdl):
    entity = models.CharField(max_length=30, verbose_name='Entity')
    doc_type = models.ForeignKey(OrgDocType, on_delete=models.CASCADE, verbose_name='Document')
    def __str__(self):
        return self.entity


class Org(TimestampMdl):
    type = models.ForeignKey(OrgType, on_delete=models.CASCADE, verbose_name='Type')
    name = models.CharField(max_length=180, verbose_name='Name')
    # organization is operational
    is_active = models.BooleanField(default=True, verbose_name='Active')
    # organization verified by following SOPs
    is_verified = models.BooleanField(default=False, verbose_name='Verified')
    # message
    msg = models.TextField(blank=True, null=True, verbose_name='Message')
    def __str__(self):
        return self.name
    

class OrgEmp(TimestampMdl):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    org = models.ForeignKey(Org, on_delete=models.CASCADE, verbose_name='Organization')
    user = models.ForeignKey(UserModel.User, on_delete=models.CASCADE, verbose_name='User')
    join_date = models.DateField(verbose_name='Joining Date')
    is_manager = models.BooleanField(default=False, verbose_name='Manager')

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    

def upload_to_org(instance,filename):
    pf_name = f'{instance.org.id}_{instance.org.name}'
    sf_name = f'{instance.doc_type.doc}'
    return f'business/org/{pf_name}/{sf_name}/{filename}'

class OrgDoc(TimestampMdl):
    org = models.ForeignKey(Org, on_delete=models.CASCADE, verbose_name='Organization')
    doc_type = models.ForeignKey(OrgDocType, on_delete=models.CASCADE, verbose_name='Document')
    reg_no = models.CharField(max_length=256, unique=True, verbose_name='Document No')
    # doc only required for partnership firm
    doc = models.FileField(_('Document'), upload_to=upload_to_org, blank=True,
            validators=[FileExtensionValidator(allowed_extensions=["pdf"])])
    end_date = models.DateField(blank=True, null=True, verbose_name='Expiry Date')
    is_active = models.BooleanField(default=True, verbose_name='Active')
    is_valid = models.BooleanField(default=False, verbose_name='Valid')
    def __str__(self):
        return f'{self.reg_no}'
