from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django_countries.serializer_fields import CountryField
from rest_framework import serializers
from .models import Image

from django.conf import settings
import os

from .image_processing import process


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    avatar = serializers.ImageField(required=False,)
    background = serializers.ImageField(required=False)
    country = CountryField()

    class Meta:
        model = User
        fields = ["username", "avatar", "password", "email", 'id', "first_name", "last_name", 'country', 'background', 'about']
        read_only_fields = ['id']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['country'] = instance.country.name
        return data


class ImageSerializer(serializers.ModelSerializer):
    #author = serializers.SlugRelatedField(slug_field='username', read_only=True)
    image = serializers.ImageField()
    description = serializers.CharField(required=False)

    class Meta:
        model = Image
        fields = ['author', 'image', 'name', 'tags', 'uploaded_at', 'id', 'description', 'color', 'height', 'width']
        read_only_fields = ['id', 'uploaded_at', 'tags', 'height', 'width', 'color', 'author']

    def create(self, validated_data):
        tags, h, w, hex_color = process(validated_data['image'].file)
        image = Image.objects.create(tags=tags, color=hex_color, height=h, width=w, **validated_data)
        return image

