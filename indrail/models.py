from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _
from django.db import models

from business import models as BMdl

from tourism.models.shops import ShopMdl, ShopLicExpMdl, ShopEmpMdl


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
    return f'business/shop/ir/station/{folder_name}/{filename}'

class Shop(ShopMdl):
    img = models.ImageField(_('Image'), upload_to=upload_to_shop_image_primary,
            validators=[FileExtensionValidator(allowed_extensions=["png","jpeg","jpg"])])
    # location
    station = models.ForeignKey(Station, on_delete=models.CASCADE, verbose_name='Railway Station')
    plt1 = models.CharField(max_length=10, blank=True, null=True, verbose_name='Primary Platform')
    plt2 = models.CharField(max_length=10, blank=True, null=True, verbose_name='Secondary Platform')
    def __str__(self):
        return f'{self.name}, {self.station.name} ({self.station.code})'


class ShopEmp(ShopEmpMdl):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name='Shop')
    def __str__(self):
        return f'{self.org_emp.user.first_name} {self.org_emp.user.last_name}'


def upload_to_shop_lic(instance,filename):
    pf_name = f'{instance.shop.station.code}_{instance.shop.shop_no}'
    return f'business/shop/ir/station/{pf_name}/lic/{filename}'
    
class ShopDoc(ShopLicExpMdl):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name='Shop Name')
    doc = models.FileField(_('Document'), upload_to=upload_to_shop_lic,
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])])
    def __str__(self):
        return self.shop.name
    

def upload_to_shop_fssai(instance,filename):
    pf_name = f'{instance.shop.station.code}_{instance.shop.shop_no}'
    return f'business/shop/ir/station/{pf_name}/fssai/{filename}'
    
class ShopFssai(ShopLicExpMdl):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name='Shop Name')
    doc = models.FileField(_('Document'), upload_to=upload_to_shop_fssai,
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])])
    contact_no = models.CharField(max_length=10, verbose_name='Contact No.')
    def __str__(self):
        return self.shop.name
  

class ShopGst(ShopLicExpMdl):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name='Shop Name')
    gst = models.ForeignKey(BMdl.OrgDoc, on_delete=models.CASCADE, verbose_name='GSTIN')
    def __str__(self):
        return self.shop.name
    

class Train(models.Model):
    train_no = models.IntegerField(verbose_name='Train No', primary_key=True)
    train_name = models.CharField(max_length=60, verbose_name='Train Name')
    station_from = models.ForeignKey(Station, on_delete=models.CASCADE, verbose_name='Station From', related_name='train_station_from')
    station_to = models.ForeignKey(Station, on_delete=models.CASCADE, verbose_name='Station To', related_name='train_station_to')
    run_sun = models.BooleanField(default=False, verbose_name='Train runs on Sunday')
    run_mon = models.BooleanField(default=False, verbose_name='Train runs on Monday')
    run_tue = models.BooleanField(default=False, verbose_name='Train runs on Tuesday')
    run_wed = models.BooleanField(default=False, verbose_name='Train runs on Wednesday')
    run_thu = models.BooleanField(default=False, verbose_name='Train runs on Thursday')
    run_fri = models.BooleanField(default=False, verbose_name='Train runs on Friday')
    run_sat = models.BooleanField(default=False, verbose_name='Train runs on Saturday')
    run_daily = models.BooleanField(default=False, verbose_name='Train runs Daily')
    duration = models.CharField(max_length=15, null=True, blank=True, verbose_name='Duration')
    def __str__(self):
        return f'{self.train_no} - {self.train_name}'


class TrainSchedule(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE, verbose_name='Train')
    seq = models.IntegerField(verbose_name='Station No')
    day = models.IntegerField(verbose_name='Day')
    distance = models.IntegerField(verbose_name='Distance (in KMs)')
    station = models.ForeignKey(Station, on_delete=models.CASCADE, verbose_name='Station')
    platform = models.CharField(max_length=6, blank=True, null=True, verbose_name='Platform')
    dep_time = models.TimeField(null=True, blank=True, verbose_name='Departure Time')
    arv_time = models.TimeField(null=True, blank=True, verbose_name='Arrival Time')
    halt_time = models.TimeField(null=True, blank=True, verbose_name='Halt Time')
    rev_dir = models.BooleanField(default=False, verbose_name='Reverse Direction')
    def __str__(self):
        return f'{self.station.name} - {self.station.code}'
