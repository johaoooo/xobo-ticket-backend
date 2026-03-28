from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Stand, Validation

class StandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stand
        fields = '__all__'
        read_only_fields = ['id', 'numero_stand', 'created_at', 'updated_at', 'validation_code', 'validation_code_expires']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance, validated_data)

class StandListSerializer(serializers.ModelSerializer):
    has_temp_password = serializers.SerializerMethodField()

    class Meta:
        model = Stand
        fields = [
            'id', 'nom', 'numero_stand', 'email',
            'nom_prop', 'prenom_prop', 'adresse',
            'statut', 'created_at', 'user', 'has_temp_password'
        ]

    def get_has_temp_password(self, obj):
        return bool(obj.temp_password)

class ValidateStandSerializer(serializers.Serializer):
    validation_password = serializers.CharField(write_only=True, required=True, min_length=4)
    comment = serializers.CharField(required=False, allow_blank=True)
