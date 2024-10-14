from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Model, Marque, Groupe
from myapi.models import Marque


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class ModelSerializer(serializers.ModelSerializer):
    marque = serializers.PrimaryKeyRelatedField(queryset=Marque.objects.all())  # Sélection de la marque par ID

    class Meta:
        model = Model
        fields = '__all__'

class MarqueSerializer(serializers.ModelSerializer):

    class Meta:
        model = Marque
        fields = ['nom', 'groupe']

class GroupeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Groupe
        fields = ['nom']