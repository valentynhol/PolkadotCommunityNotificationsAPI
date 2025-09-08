from django.contrib.auth.models import User

from rest_framework import serializers

from fcm_django.models import FCMDevice

from .utils import verify_attestation, generate_device_jwt


class BriefFCMDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FCMDevice
        fields = ["device_id", "registration_id", "type"]


class PushNotificationSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    body = serializers.CharField(max_length=1000)


class DeviceRegisterSerializer(serializers.Serializer):
    device_uuid = serializers.UUIDField()
    platform = serializers.ChoiceField(choices=['android', 'ios'])
    fcm_token = serializers.CharField()
    attestation = serializers.CharField()

    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, attrs):
        if not verify_attestation(attrs.get('attestation'), attrs.get('device_uuid'), attrs.get('platform')):
            raise serializers.ValidationError("Attestation verification failed.")

        return attrs

    def create(self, validated_data):
        device_uuid = validated_data['device_uuid']
        platform = validated_data['platform']
        fcm_token = validated_data['fcm_token']

        device, _ = FCMDevice.objects.update_or_create(
            device_id=device_uuid,
            defaults={
                "type": platform,
                "registration_id": fcm_token,
            }
        )

        # Subscribe to necessary FCM topics
        topics = ["global", device.type]
        for topic in topics:
            try:
                messaging.subscribe_to_topic([device.registration_id], topic)
            except Exception as e:
                print(f"Failed to subscribe device {device.id} to topic {topic}: {e}")

        access, refresh = generate_device_jwt(device_uuid, platform)

        return {
            "access": str(access),
            "refresh": str(refresh)
        }
