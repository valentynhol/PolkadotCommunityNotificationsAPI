from django.contrib.auth.models import User

from rest_framework import serializers

from fcm_django.models import FCMDevice


class PushNotificationSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    body = serializers.CharField(max_length=1000)


class BriefFCMDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FCMDevice
        fields = ["id", "registration_id", "type"]
