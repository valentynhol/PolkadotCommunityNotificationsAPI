from typing import Literal

from rest_framework_simplejwt.tokens import RefreshToken
from pyattest.configs.google_play_integrity_api import GooglePlayIntegrityApiConfig
from pyattest.attestation import Attestation

from ApiCore.settings import (APK_NAME, DEBUG, ATTESTATION_DECRYPTION_KEY, ATTESTATION_VERIFICATION_KEY,
                              ATTESTATION_APP_SIGNING_KEY)


def verify_attestation(attest_token: str, nonce: bytes, platform: Literal["android", "ios"]) -> bool:
    """
    Verify attestation using Play Integrity (android) or App Attest (ios)

    Parameters:
        attest_token: JWT sent by app installation
        nonce: nonce used to encode the token
        platform: device's platform

    Returns:
        bool: True if verified, False if not
    """
    print("INFO: Verifying attestation")

    if platform == "android":
        try:
            config = GooglePlayIntegrityApiConfig(
                decryption_key=ATTESTATION_DECRYPTION_KEY,
                verification_key=ATTESTATION_VERIFICATION_KEY,
                apk_package_name=APK_NAME,
                production=not DEBUG,
                allow_non_play_distribution=DEBUG,
                verify_code_signature_hex=[
                    ATTESTATION_APP_SIGNING_KEY
                ],
                required_device_verdict="MEETS_STRONG_INTEGRITY", # TODO
            )
        except ValueError:
            return False

        attestation = Attestation(attest_token, nonce, config)

        try:
            attestation.verify()
            return True
        except PyAttestException:
            return False
    elif platform == "ios":
        # TODO
        return False # do not accept requests from ios devices for now
    else:
        # does not support web push notifications
        return False


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