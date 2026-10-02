from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Student


class StudentSerializer(serializers.ModelSerializer):

    def validate_profile_image(self, image):
        # Maximum size: 2 MB
        if image.size > 2 * 1024 * 1024:
            raise serializers.ValidationError(
                "Image size must be less than 2 MB."
            )

        # Allowed image formats
        allowed_formats = ["JPEG", "PNG", "WEBP"]

        if image.image.format not in allowed_formats:
            raise serializers.ValidationError(
                "Only JPEG, PNG, and WEBP images are allowed."
            )

        return image

    class Meta:
        model = Student
        fields = "__all__"


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"]
        )

        return user