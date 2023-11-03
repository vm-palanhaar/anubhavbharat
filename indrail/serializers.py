from datetime import datetime

from rest_framework import serializers
from datetime import date

from indrail import models as IRMdl

from users import models as UserMdl


'''
--- Common APIs serializers
1. RailStationListSrl
--- iDUkaan APIs serializers
1. AddShop_iDukaanSrl
2. OrgShopList_iDukaanSrl
3. UpdateShop_iDukaanSrl
4. ShopInfo_iDukaanSrl
--- Yatrigan APIs serializers
1. ShopList_YatriganSrl
2. ShopInfo_YatriganSrl
3. TrainList_YatriganSrl
4. TrainSchedule_YatriganSrl [_TrainScheduleStationList]
'''

class RailStationListSrl(serializers.ModelSerializer):
    station = serializers.SerializerMethodField()
    class Meta:
        model = IRMdl.Station
        fields = ['station']

    def get_station(self, instance):
        return f'{instance.name} - {instance.code}'


class AddShop_iDukaanSrl(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    org = serializers.CharField()
    img = serializers.ImageField(write_only=True)
    contact_no = serializers.CharField(write_only=True)
    # station
    lat = serializers.CharField(write_only=True)
    lon = serializers.CharField(write_only=True)
    plt1 = serializers.CharField(write_only=True, allow_blank=True, allow_null=True)
    plt2 = serializers.CharField(write_only=True, allow_blank=True, allow_null=True)
    # payments
    is_cash = serializers.BooleanField(write_only=True)
    is_card = serializers.BooleanField(write_only=True)
    is_upi = serializers.BooleanField(write_only=True)
    # shop license
    lic_no = serializers.CharField(required=True, write_only=True)
    lic_doc = serializers.FileField(required=True, write_only=True)
    lic_sd = serializers.DateField(required=True, write_only=True)
    lic_ed = serializers.DateField(required=True, write_only=True)
    class Meta:
        model = IRMdl.Shop
        exclude = ['created_at','updated_at','is_open','is_active','is_verified']

    def create(self, validated_data):
        today_date = date.today()
        is_active = today_date < validated_data['lic_ed']
        shop = IRMdl.Shop.objects.create(
            org = self.context.get('org'),
            name = validated_data['name'],
            shop_no = validated_data['shop_no'],
            img = validated_data['img'],
            contact_no = validated_data['contact_no'],
            # station
            station = validated_data['station'],
            lat = validated_data['lat'],
            lon = validated_data['lon'],
            plt1 = validated_data['plt1'],
            plt2 = validated_data['plt2'],
            # payments
            is_cash = validated_data['is_cash'],
            is_card = validated_data['is_card'],
            is_upi = validated_data['is_upi'],
            # status
            is_active = is_active,
        )
        shop.save()
        # add employee as manager
        shop_emp = IRMdl.ShopEmp.objects.create(
            shop = shop,
            org_emp = self.context.get('org_emp'),
            join_date = datetime.now().date(),
            is_manager = True
        )
        shop_emp.save()
        # add shop X lic doc
        shop_lic = IRMdl.ShopDoc.objects.create(
            shop = shop,
            reg_no = validated_data['lic_no'],
            doc = validated_data['lic_doc'],
            start_date = validated_data['lic_sd'],
            end_date = validated_data['lic_ed'],
        )
        shop_lic.save()
        return shop


class OrgShopList_iDukaanSrl(serializers.ModelSerializer):
    id = serializers.CharField()
    org = serializers.SerializerMethodField()
    station = serializers.SerializerMethodField()
    emp_manager = serializers.SerializerMethodField()
    class Meta:
        model = IRMdl.Shop
        fields = ['id','org','shop_no','name','img','station','plt1','plt2',
                  'is_open', 'is_active','is_verified','emp_manager','msg']
        
    def get_org(self, instance):
        return str(instance.org.id)
    
    def get_emp_manager(self, instance):
        return self.context.get('emp_manager')
    
    def get_station(self, instance):
        return f'{instance.station.name} - {instance.station.code}'


class UpdateShop_iDukaanSrl(serializers.ModelSerializer):
    id = serializers.CharField()
    class Meta:
        model = IRMdl.Shop
        fields = ['id','contact_no','is_open','is_cash','is_card','is_upi']


class ShopInfo_iDukaanSrl(serializers.ModelSerializer):
    id = serializers.CharField()
    station = serializers.CharField()
    class Meta:
        model = IRMdl.Shop
        exclude = ['org','created_at','updated_at','lat','lon']


class AddShopEmp_iDukaanSrl(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    join_date = serializers.DateField(write_only=True)
    class Meta:
        model = IRMdl.ShopEmp
        fields = ['id','shop','org_emp','join_date','is_manager']


class ShopEmpList_iDukaanSrl(serializers.ModelSerializer):
    id = serializers.CharField()
    name = serializers.SerializerMethodField()
    exp = serializers.SerializerMethodField()
    class Meta:
        model = IRMdl.ShopEmp
        exclude = ['shop','org_emp','created_at','updated_at']

    def get_name(self, instance):
        user = UserMdl.User.objects.get(username=instance.org_emp.user)
        return f'{user.first_name} {user.last_name}'
    
    def get_exp(self, instance):
        joining_date = datetime.strptime(str(instance.join_date), '%Y-%m-%d')
        current_date = datetime.now()

        delta = current_date - joining_date

        years = delta.days // 365
        months = (delta.days % 365) // 30
        days = (delta.days % 365) % 30

        return f'{years} years {months} months {days} days'


class UpdateShopEmp_iDukaanSrl(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    name = serializers.SerializerMethodField(read_only=True)
    exp = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = IRMdl.ShopEmp
        fields = ['id', 'name', 'is_manager','join_date', 'exp']

    def get_name(self, instance):
        user = UserMdl.User.objects.get(username=instance.org_emp.user)
        return f'{user.first_name} {user.last_name}'
    
    def get_exp(self, instance):
        joining_date = datetime.strptime(str(instance.join_date), '%Y-%m-%d')
        current_date = datetime.now()

        delta = current_date - joining_date

        years = delta.days // 365
        months = (delta.days % 365) // 30
        days = (delta.days % 365) % 30

        return f'{years} years {months} months {days} days'


class ShopList_YatriganSrl(serializers.ModelSerializer):
    id = serializers.CharField()
    class Meta:
        model = IRMdl.Shop
        fields = ['id','name','shop_no','img','plt1','plt2','is_open']


class ShopInfo_YatriganSrl(serializers.ModelSerializer):
    id = serializers.CharField()
    class Meta:
        model = IRMdl.Shop
        fields = ['id','name','shop_no','img','contact_no','plt1','plt2','is_cash','is_card','is_upi','lat','lon']


class TrainList_YatriganSrl(serializers.ModelSerializer):
    train = serializers.SerializerMethodField()
    class Meta:
        model = IRMdl.Train
        fields = ['train']

    def get_train(self, instance):
        return f'{instance.train_no} - {instance.train_name}'
    
class _TrainScheduleStationList(serializers.ModelSerializer):
    station = serializers.SerializerMethodField()
    class Meta:
        model = IRMdl.TrainSchedule
        exclude = ['id','seq','train']
    
    def get_station(self, instance):
        return f'{instance.station.name} - {instance.station.code}'
    

class TrainSchedule_YatriganSrl(serializers.ModelSerializer):
    station_from = serializers.SerializerMethodField()
    station_to = serializers.SerializerMethodField()
    stations = serializers.SerializerMethodField()
    run_status = serializers.SerializerMethodField()
    class Meta:
        model = IRMdl.Train
        fields = ['train_no','train_name','station_from','station_to'
                  ,'stations','run_status','duration']
        
    def get_station_from(self, instance):
        return f'{instance.station_from.name} - {instance.station_from.code}'
    
    def get_station_to(self, instance):
        return f'{instance.station_to.name} - {instance.station_from.code}'

    def get_stations(self, instance):
        schedule = IRMdl.TrainSchedule.objects.filter(train=instance)
        serializer = _TrainScheduleStationList(schedule, many=True)
        return serializer.data
    
    def get_run_status(self, instance):
        days = []
        if instance.run_sun:
            days.append('SUN')
        if instance.run_mon:
            days.append('MON')
        if instance.run_tue:
            days.append('TUE')
        if instance.run_wed:
            days.append('WED')
        if instance.run_thu:
            days.append('THU')
        if instance.run_fri:
            days.append('FRi')
        if instance.run_sat:
            days.append('SAT')
        return days