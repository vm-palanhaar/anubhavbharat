from rest_framework import serializers

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password

from users import models as UserMdl


class UserSignupSerializer(serializers.ModelSerializer):
    firstName = serializers.CharField(source='first_name')
    lastName = serializers.CharField(source='last_name')
    contactNo = serializers.CharField(source='contact_no')
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    class Meta:
        model = UserMdl.User
        fields = ['firstName','lastName','contactNo','email','username','password']

    def create(self, validated_data):
        user = UserMdl.User.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            contact_no = validated_data['contact_no'],
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    firstName = serializers.CharField(read_only=True, source='first_name')
    lastName = serializers.CharField(read_only=True, source='last_name')
    isKyc = serializers.BooleanField(read_only=True, source='is_kyc')
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    class Meta:
        model = UserMdl.User
        fields = ['username','firstName','lastName','isKyc','password']

    def validate(self, data):
        user = authenticate(**data)
        if user:
            return user
        return serializers.ValidationError()


class UserProfileSrl(serializers.ModelSerializer):
    firstName = serializers.CharField(read_only=True, source='first_name')
    lastName = serializers.CharField(read_only=True, source='last_name')
    contactNo = serializers.CharField(source='contact_no')
    isActive = serializers.BooleanField(read_only=True, source='is_active')
    isKyc = serializers.BooleanField(read_only=True, source='is_kyc')
    class Meta:
        model = UserMdl.User
        fields = ['firstName','lastName','username','email','contactNo','isActive','isKyc']
