from django.contrib.auth.models import User

from rest_framework import permissions, viewsets, views, authentication
from rest_framework.response import Response

from fcm_django.models import FCMDevice
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet

from firebase_admin import messaging

from ApiApp.serializers import PushNotificationSerializer, BriefFCMDeviceSerializer


class BriefFCMDeviceViewSet(FCMDeviceAuthorizedViewSet):
    serializer_class = BriefFCMDeviceSerializer

    def perform_create(self, serializer):
        device = serializer.save(user=self.request.user)

        topics = ["global", device.type]
        try:
            for topic in topics:
                messaging.subscribe_to_topic([device.registration_id], topic)
        except Exception as e:
            print(f"Error: Failed to subscribe device (ID: {device.id}) to topics: {e}")

        return device


class SendGlobalNotification(views.APIView):
    authentication_classes = [authentication.SessionAuthentication, authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PushNotificationSerializer

    def post(self, request):
        try:
            messaging.send(
                messaging.Message(
                    notification=messaging.Notification(
                        title=request.data.get('title'),
                        body=request.data.get('body'),
                    ),
                    topic="global"
                )
            )

            return Response({"success": True})
        except Exception as e:
            print(f"Error: Failed to send notification: {e}")
            return Response({"success": False}, status=500)
