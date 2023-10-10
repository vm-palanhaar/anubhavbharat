from datetime import datetime

from rest_framework import serializers
from datetime import date

from indrail import models as IRMdl


'''
--- Common APIs serializers
1. RailStationListSrl
--- iDUkaan APIs serializers
1. AddShop_iDukaanSrl
2. OrgShopList_iDukaanSrl
3. UpdateShop_iDukaanSrl
4. ShopInfo_iDukaanSrl
--- Yatrigan APIs serializers
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

        shop_lic = IRMdl.ShopLic.objects.create(
            shop = shop,
            reg_no = validated_data['lic_no'],
            doc = validated_data['lic_doc'],
            start_date = validated_data['lic_sd'],
            end_date = validated_data['lic_ed'],
        )
        shop_lic.save()

        shop_emp = IRMdl.ShopEmp.objects.create(
            shop = shop,
            user = self.context.get('user'),
            join_date = datetime.now().date(),
            is_manager = True
        )
        shop_emp.save()

        return shop


class OrgShopList_iDukaanSrl(serializers.ModelSerializer):
    id = serializers.CharField()
    org = serializers.SerializerMethodField()
    class Meta:
        model = IRMdl.Shop
        fields = ['id','org','shop_no','name','img','station','plt1','plt2',
                  'is_open', 'is_active','is_verified']
        
    def get_org(self, instance):
        return str(instance.org.id)


class UpdateShop_iDukaanSrl(serializers.ModelSerializer):
    class Meta:
        model = IRMdl.Shop
        fields = ['id','contact_no','is_open','is_cash','is_card','is_upi']


class ShopInfo_iDukaanSrl(serializers.ModelSerializer):
    id = serializers.CharField()
    station = serializers.CharField()
    class Meta:
        model = IRMdl.Shop
        exclude = ['org','created_at','updated_at','lat','lon']
