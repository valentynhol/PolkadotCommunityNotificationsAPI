from rest_framework import permissions, views, authentication
from rest_framework.response import Response

from firebase_admin import messaging

from ApiApp.serializers import PushNotificationSerializer, DeviceRegisterSerializer
from ApiApp.auth import DeviceJWTAuthentication
from ApiApp.permissions import IsRegisteredDevice


class DeviceRegisterView(views.APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = DeviceRegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        tokens = serializer.save() # serializer returns JWT pair after saving the device instance

        return Response(tokens)


class NonceView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = NonceRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        device = serializer.create_or_get_device()
        nonce = device.generate_nonce()

        return Response({"nonce": nonce})


# TODO: REMOVE, test only, already implemented by Firebase
class SendGlobalNotification(views.APIView):
    authentication_classes = [authentication.SessionAuthentication, authentication.BasicAuthentication, DeviceJWTAuthentication]
    permission_classes = [permissions.IsAuthenticated | IsRegisteredDevice]
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
