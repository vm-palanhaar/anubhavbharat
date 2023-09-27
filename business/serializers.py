from rest_framework import serializers

from business import models as BModel


class OrgTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = BModel.OrgType
        fields = ['entity','doc','desc']

