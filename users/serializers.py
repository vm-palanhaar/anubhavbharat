from rest_framework import serializers

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password

from users import models as UserMdl


class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    class Meta:
        model = UserMdl.User
        fields = ['first_name','last_name','contact_no','email','username','password']

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
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    is_verified = serializers.BooleanField(read_only=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    class Meta:
        model = UserMdl.User
        fields = ['username','first_name','last_name','is_verified','password']

    def validate(self, data):
        user = authenticate(**data)
        if user:
            return user
        return serializers.ValidationError()
        #raise TExp.CustomValidation('message',UserApiV1Msg.UserLoginMsg.userLoginFailed_UserCredInvalid(), 400)


class UserLoggedInSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    is_verified = serializers.BooleanField(read_only=True)
    class Meta:
        model = UserMdl.User
        fields = ['username','first_name','last_name','is_verified']
