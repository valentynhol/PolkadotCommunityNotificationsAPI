from typing import Literal

from rest_framework_simplejwt.tokens import RefreshToken


def verify_attestation(token, uuid, platform: Literal["android", "ios"]) -> bool:
    """
    Verify attestation using Play Integrity (android) or App Attest (ios)

    Parameters:
        token: JWT sent by app installation
        uuid: UUID of app installation
        platform: device's platform

    Returns:
        bool: True if verified, False if not
    """
    # TODO
    print("Verifying attestation")
    return True


def generate_device_jwt(uuid: str, platform: Literal["android", "ios"]) -> (str, str):
    """
    Generate JWT access and refresh token pair for a device

    Parameters:
        uuid: UUID of the device
        platform: device's platform

    Returns:
        (str, str): access token, refresh token
    """

    refresh = RefreshToken()

    refresh['device_id'] = str(uuid)
    refresh['type'] = platform

    access = refresh.access_token
    return str(access), str(refresh)