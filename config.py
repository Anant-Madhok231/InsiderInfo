"""
Copyright (c) 2025 Anant Madhok. All Rights Reserved.

This software is proprietary and confidential. Unauthorized copying, modification,
distribution, or use of this software, via any medium, is strictly prohibited
without the express written permission of Anant Madhok.

For licensing inquiries: GitHub @Anant-Madhok231
"""

import os

from dotenv import load_dotenv

load_dotenv()


class ConfigError(RuntimeError):
    """Raised when the application is started without its required settings."""


def _required(name):
    """Return an environment variable, or fail loudly if it is not set.

    Credentials deliberately have no default. A missing value should stop the
    application at startup rather than silently fall through to a placeholder.
    """
    value = os.environ.get(name)
    if not value:
        raise ConfigError(
            "Missing required environment variable: {name}. "
            "Copy .env.example to .env and fill it in for local development, "
            "or set {name} in your host's environment settings.".format(name=name)
        )
    return value


class Config:
    # Mail transport. These are not secrets, so a sensible default is fine.
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "True").lower() == "true"

    # Credentials for the application's sending account.
    MAIL_USERNAME = _required("MAIL_USERNAME")
    MAIL_PASSWORD = _required("MAIL_PASSWORD")

    # Signs Flask session cookies. A known value lets anyone forge a session.
    SECRET_KEY = _required("SECRET_KEY")

    # Market data providers.
    ALPHA_VANTAGE_API_KEY = _required("ALPHA_VANTAGE_API_KEY")
    FMP_API_KEY = _required("FMP_API_KEY")
