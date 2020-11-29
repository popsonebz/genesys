from .models import User
from rest_framework import serializers, status
from .exceptions import CustomValidation
from django.contrib.auth import password_validation
from django.db import transaction


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password1 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    last_login = serializers.DateTimeField(read_only=True)

    def save(self):
        return super(UserSerializer, self).save()

    def validate(self, data):
        data = super(UserSerializer, self).validate(data)
        password_validation.validate_password(data['password1'], self.instance)
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('Passwords do not match')

        if User.objects.filter(email=data['email']).exists():
            raise CustomValidation('Duplicate Email. User already exists.', data['email'],
                                   status_code=status.HTTP_409_CONFLICT)

        return data

    def create(self, validated_data):

        # instantiate user
        user = User(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data['email'],
            is_active=True
        )

        with transaction.atomic():
            user.set_password(validated_data['password1'])
            user.save()

        return user

    def update(self, instance, validated_data):
        #instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    new_password1 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    new_password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                'Your old password was entered incorrectly. Please try again.'
            )
        return value

    def validate(self, data):
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError(
                {'new_password2': "The two passwords don't match."}
            )
        password_validation.validate_password(data['new_password1'],
                                              self.context['request'].user)
        return data

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def save(self, **kwargs):
        password = self.validated_data['new_password1']
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')