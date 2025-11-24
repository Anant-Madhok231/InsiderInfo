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

class Config:
    # Email Settings for the application's Gmail account (this is the sender's email)
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'insidertrade05@gmail.com')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'cxiu rhyt fxea figg')
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-change-this-in-production')
    
    # API Keys
    ALPHA_VANTAGE_API_KEY = os.environ.get('ALPHA_VANTAGE_API_KEY', 'T21J4YZC2W2M1WL5')
    FMP_API_KEY = os.environ.get('FMP_API_KEY', 'wsxz6HnLfi2bLaV7wFP3DDcDeAfLfKhz') 