from rest_framework import permissions, views, authentication
from rest_framework.response import Response

from firebase_admin import messaging

from ApiApp.serializers import DeviceRegisterSerializer, NonceRequestSerializer, FCMTokenSerializer
from ApiApp.auth import DeviceJWTAuthentication
from ApiApp.permissions import IsRegisteredDevice
from ApiApp.models import AttestedFCMDevice


class DeviceRegisterView(views.APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = DeviceRegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        tokens = serializer.save() # serializer returns JWT pair after saving the device instance

        return Response(tokens)


class FCMTokenUpdateView(views.APIView):
    permission_classes = [IsRegisteredDevice]
    authentication_classes = [DeviceJWTAuthentication]

    serializer_class = FCMTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            fcm_token = serializer.validated_data['fcm_token']

            try:
                device = AttestedFCMDevice.objects.get(device_id=request.device_uuid)
            except AttestedFCMDevice.DoesNotExist:
                # shouldn't happen
                return Response({'error': 'Device not found.'}, status=status.HTTP_404_NOT_FOUND)

            device.registration_id = fcm_token
            device.save(update_fields=['registration_id'])

            return Response({'message': 'Token updated successfully.'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NonceView(views.APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = NonceRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        device = serializer.create_or_get_device()
        nonce = device.generate_nonce()

        return Response({"nonce": nonce})
