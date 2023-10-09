from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _
from django.db import models

from tourism.models import TimestampModel
from business import models as BMdl
from users import models as UMdl


class Zone(models.Model):
    code = models.CharField(max_length=5, primary_key=True, verbose_name='Zone Code')
    name = models.CharField(max_length=90, verbose_name='Zone Name')
    def __str__(self):
        return self.name()


class Div(models.Model):
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, verbose_name='Railway Zone')
    code = models.CharField(max_length=5, primary_key=True, verbose_name='Division Code')
    name = models.CharField(max_length=60, verbose_name='Division Name')
    def __str__(self):
        return f'{self.name} - {self.zone.name}'
    

class StationCat(models.Model):
    cat = models.CharField(max_length=6, primary_key=True, verbose_name='Station Category')
    def __str__(self):
        return self.cat
    

class Station(models.Model):
    zone = models.ForeignKey(Zone, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Railway Zone')
    div = models.ForeignKey(Div, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Railway Division')
    code = models.CharField(max_length=10, primary_key=True, verbose_name='Station Code')
    name = models.CharField(max_length=100, verbose_name='Station Name')
    plt = models.IntegerField(blank=True, null=True, verbose_name='No. of Platforms')
    cat = models.ForeignKey(StationCat, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Station Category')
    def __str__(self):
        return f'{self.name} - {self.code}'
    

def upload_to_shop_image_primary(instance,filename):
    folder_name = f'{instance.station.code}_{instance.shop_no}'
    return f'business/shop/ir/stations/{folder_name}/{filename}'

class Shop(TimestampModel):
    org = models.ForeignKey(BMdl.Org, on_delete=models.CASCADE, verbose_name='Organization')
    name = models.CharField(max_length=60, verbose_name='Shop Name')
    shop_no = models.CharField(max_length=15, verbose_name='Shop No.')
    img = models.ImageField(_('Image'), upload_to=upload_to_shop_image_primary,
            validators=[FileExtensionValidator(allowed_extensions=["png","jpeg","jpg"])])
    contact_no = models.CharField(max_length=15, verbose_name='Contact No.')
    # location
    station = models.ForeignKey(Station, on_delete=models.CASCADE, verbose_name='Railway Station')
    lat = models.CharField(max_length=30, verbose_name='Latitude')
    lon = models.CharField(max_length=30, verbose_name='Longitude')
    plt1 = models.CharField(max_length=10, blank=True, null=True, verbose_name='Primary Platform')
    plt2 = models.CharField(max_length=10, blank=True, null=True, verbose_name='Secondary Platform')
    # open/close status
    is_open = models.BooleanField(default=False, verbose_name='Open')
    # shop is orperational
    is_active = models.BooleanField(default=False, verbose_name='Active')
    # shop verified by following SOPs
    is_verified = models.BooleanField(default=False, verbose_name='Verified')
    # payments
    is_cash = models.BooleanField(default=False, verbose_name='Cash')
    is_card = models.BooleanField(default=False, verbose_name='Card')
    is_upi = models.BooleanField(default=False, verbose_name='UPI')
    def __str__(self):
        return f'{self.name}, {self.station.name} ({self.station.code})'


class ShopEmp(TimestampModel):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name='Shop')
    user = models.ForeignKey(UMdl.User, on_delete=models.CASCADE, verbose_name='User')
    join_date = models.DateField(verbose_name='Joining Date')
    is_manager = models.BooleanField(default=False, verbose_name='Manager')
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


def upload_to_shop_license(instance,filename):
    folder_name = f'{instance.shop.station.code}_{instance.shop.shop_no}'
    return f'business/shop/ir/stations/{folder_name}/{filename}'
    
class ShopLic(TimestampModel):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name='Shop Name')
    reg_no = models.CharField(max_length=30, verbose_name='Registration No.', unique=True)
    doc = models.FileField(_('Document'), upload_to=upload_to_shop_license,
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])])
    start_date = models.DateField(blank=True, null=True, verbose_name='Start Date')
    end_date = models.DateField(blank=True, null=True, verbose_name='End Date')
    is_valid = models.BooleanField(default=False, verbose_name='Valid')
    def __str__(self):
        return self.shop.name
