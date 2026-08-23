"""
Copyright (c) 2025 Anant Madhok. All Rights Reserved.

This software is proprietary and confidential. Unauthorized copying, modification,
distribution, or use of this software, via any medium, is strictly prohibited
without the express written permission of Anant Madhok.

For licensing inquiries: GitHub @Anant-Madhok231
"""

import os
import secrets

from dotenv import load_dotenv

load_dotenv()


def _credential(name):
    """Read a credential from the environment.

    Credentials are never hardcoded in this file. If one is missing the value
    comes back empty and a warning is logged, so the application still starts
    and only the feature that needs it fails. That is deliberate: a missing
    key should not take the whole site down at import time.
    """
    value = os.environ.get(name, "")
    if not value:
        print(
            "[config] {name} is not set. "
            "Features that depend on it will not work until it is configured "
            "in .env (local) or the host's environment settings.".format(name=name)
        )
    return value


class Config:
    # Mail transport. Not secret, so defaults are fine.
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "True").lower() == "true"

    # Credentials for the application's sending account.
    MAIL_USERNAME = _credential("MAIL_USERNAME")
    MAIL_PASSWORD = _credential("MAIL_PASSWORD")

    # Signs Flask session cookies. Falls back to a fresh random value per
    # process: sessions reset on restart, but a publicly known key can never
    # be used to forge one.
    SECRET_KEY = os.environ.get("SECRET_KEY") or secrets.token_hex(32)

    # Market data providers.
    ALPHA_VANTAGE_API_KEY = _credential("ALPHA_VANTAGE_API_KEY")
    FMP_API_KEY = _credential("FMP_API_KEY")
    POLYGON_API_KEY = _credential("POLYGON_API_KEY")
