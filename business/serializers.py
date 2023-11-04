from datetime import datetime

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from business import models as BModel

from users import models as UserMdl


class OrgTypesSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    doc = serializers.SerializerMethodField()
    doc_no = serializers.SerializerMethodField()
    desc = serializers.SerializerMethodField()
    is_doc = serializers.SerializerMethodField()
    class Meta:
        model = BModel.OrgType
        exclude = ['created_at','updated_at','doc_type']

    def get_doc(self, obj):
        return obj.doc_type.doc
    def get_doc_no(self, obj):
        return obj.doc_type.doc_no
    def get_desc(self, obj):
        return obj.doc_type.desc
    def get_is_doc(self, obj):
        return obj.doc_type.is_doc


class AddOrgSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    reg_no = serializers.CharField(write_only=True,
            validators=[UniqueValidator(queryset=BModel.OrgDoc.objects.all())])
    doc = serializers.FileField(write_only=True, required=False)
    end_date = serializers.DateField(allow_null=True)
    class Meta:
        model = BModel.Org
        exclude = ['is_active','is_verified','created_at','updated_at']

    def create(self, validated_data):
        org = BModel.Org.objects.create(
            type = validated_data['type'],
            name = validated_data['name'],
        )
        org.save()
        # add associated user as manager in org
        org_emp = BModel.OrgEmp.objects.create(
            org = org,
            user = self.context.get('user'),
            join_date = datetime.now().date(),
            is_manager = True
        )
        org_emp.save
        # save org doc
        if validated_data['type'].doc_type.is_doc:
            org_doc = BModel.OrgDoc.objects.create(
                org = org,
                doc_type = validated_data['type'].doc_type,
                reg_no = validated_data['reg_no'],
                doc = validated_data['doc'],
                end_date = validated_data['end_date'],
            )
        else:
            org_doc = BModel.OrgDoc.objects.create(
                org = org,
                doc_type = validated_data['type'].doc_type,
                reg_no = validated_data['reg_no'],
                end_date = validated_data['end_date'],
            )
        org_doc.save()
        return org


class OrgListSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    class Meta:
        model = BModel.Org
        exclude = ['type','created_at','updated_at']


class OrgInfoSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    type = serializers.CharField()
    emp = serializers.SerializerMethodField()
    class Meta:
        model = BModel.Org
        fields = ['id','name','type','emp']
    
    def get_emp(self, instance):
        return BModel.OrgEmp.objects.filter(org=instance).count()


class AddOrgEmpSerializer(serializers.ModelSerializer):
    id = serializers.CharField(required=False, read_only=True)
    user = serializers.CharField()
    class Meta:
        model = BModel.OrgEmp
        exclude = ['created_at','updated_at']

    def create(self, validated_data):
        org_emp = BModel.OrgEmp.objects.create(
            org = validated_data['org'],
            user = self.context.get('user'),
            join_date = validated_data['join_date'],
            is_manager = validated_data['is_manager']
        )
        org_emp.save
        return org_emp


class OrgEmpListSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    name = serializers.SerializerMethodField()
    exp = serializers.SerializerMethodField()
    class Meta:
        model = BModel.OrgEmp
        exclude = ['user','org','created_at','updated_at']

    def get_name(self, instance):
        user = UserMdl.User.objects.get(username=instance.user)
        return f'{user.first_name} {user.last_name}'
    
    def get_exp(self, instance):
        joining_date = datetime.strptime(str(instance.join_date), '%Y-%m-%d')
        current_date = datetime.now()

        delta = current_date - joining_date

        years = delta.days // 365
        months = (delta.days % 365) // 30
        days = (delta.days % 365) % 30

        return f'{years} years {months} months {days} days'


class UpdateOrgEmpSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    name = serializers.SerializerMethodField(read_only=True)
    exp = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = BModel.OrgEmp
        fields = ['id', 'name', 'is_manager','join_date', 'exp']

    def get_name(self, instance):
        user = UserMdl.User.objects.get(username=instance.user)
        return f'{user.first_name} {user.last_name}'
    
    def get_exp(self, instance):
        joining_date = datetime.strptime(str(instance.join_date), '%Y-%m-%d')
        current_date = datetime.now()

        delta = current_date - joining_date

        years = delta.days // 365
        months = (delta.days % 365) // 30
        days = (delta.days % 365) % 30

        return f'{years} years {months} months {days} days'
    