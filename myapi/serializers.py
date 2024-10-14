from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Model, Brand, Group, CustomUser
from myapi.models import Brand


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'enabled')

    def create(self, validated_data):

        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            enabled=validated_data.get('enabled', 0)
        )
        return user
class ModelSerializer(serializers.ModelSerializer):
    brand = serializers.SlugRelatedField(queryset=Brand.objects.all(), slug_field='name')
    class Meta:
        model = Model
        fields = '__all__'

class MarqueSerializer(serializers.ModelSerializer):
    group = serializers.SlugRelatedField(queryset=Group.objects.all(), slug_field='name')

    class Meta:
        model = Brand
        fields = '__all__'

class GroupeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ['name']