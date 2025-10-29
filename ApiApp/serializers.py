from django.contrib.auth.models import User

from rest_framework import serializers

from ApiApp.models import AttestedFCMDevice

from ApiApp.utils import verify_attestation, generate_device_jwt


class NonceRequestSerializer(serializers.Serializer):
    device_uuid = serializers.CharField()
    platform = serializers.ChoiceField(choices=["android", "ios"])

    def create_or_get_device(self):
        """
        Get an existing device or create a new one.
        Returns the AttestedFCMDevice instance.
        """
        device_uuid = self.validated_data["device_uuid"]
        platform = self.validated_data["platform"]

        device, _ = AttestedFCMDevice.objects.get_or_create(
            device_id=device_uuid,
            defaults={"type": platform}
        )
        return device


class FCMTokenSerializer(serializers.Serializer):
    fcm_token = serializers.CharField(max_length=255)


class DeviceRegisterSerializer(serializers.Serializer):
    device_uuid = serializers.UUIDField()
    platform = serializers.ChoiceField(choices=['android', 'ios'])
    attestation = serializers.CharField()

    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, attrs):
        device_id = attrs.get("device_uuid")
        platform = attrs.get("platform")
        attest_token = attrs.get("attestation")

        try:
            device = AttestedFCMDevice.objects.get(device_id=device_id, type=platform)
        except AttestedFCMDevice.DoesNotExist:
            raise serializers.ValidationError("Device not found or invalid platform.")

        if not device.verify_attestation(attest_token):
            raise serializers.ValidationError("Attestation verification failed.")

        return attrs

    def create(self, validated_data):
        device_uuid = validated_data['device_uuid']
        platform = validated_data['platform']

        device, _ = AttestedFCMDevice.objects.update_or_create(
            device_id=device_uuid,
            defaults={
                "type": platform,
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
