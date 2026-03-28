from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from .models import User

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    is_admin = serializers.ReadOnlyField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                  'prenom', 'role', 'avatar', 'full_name', 'is_admin']
        read_only_fields = ['id', 'role']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'prenom']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            prenom=validated_data.get('prenom', '')
        )
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Identifiants incorrects")

class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'prenom', 'email', 'avatar']
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=6)
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Ancien mot de passe incorrect")
        return value

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    
    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
            return user
        except User.DoesNotExist:
            raise serializers.ValidationError("Aucun utilisateur avec cet email")

class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=6)
    
    def validate_token(self, value):
        try:
            user = User.objects.get(reset_password_token=value)
            from django.utils import timezone
            if user.reset_password_expires and user.reset_password_expires < timezone.now():
                raise serializers.ValidationError("Token expiré")
            return user
        except User.DoesNotExist:
            raise serializers.ValidationError("Token invalide")
