# Insider Trade Ratio (ITR) Platform

**Copyright (c) 2025 Anant Madhok. All Rights Reserved.**

A Flask-based web application for analyzing stock market data and calculating Insider Trade Ratios to identify unusual trading patterns.

> **⚠️ PROPRIETARY SOFTWARE**: This software is proprietary and confidential. Unauthorized copying, modification, distribution, or use is strictly prohibited without express written permission from the copyright holder.

## Features

- Real-time stock data fetching
- Insider Trade Ratio (ITR) calculation
- User authentication (signup/login with email verification)
- Portfolio and watchlist management
- Options data analysis
- Search functionality for stocks and underlyings

## Insider Trade Ratio (ITR)

The ITR metric identifies trades that resemble insider behavior — large, sudden, high-risk positions that stand out from normal market activity.

**Formula:**
```
ITR = [(Volume + 1) × |Vega| × |Delta| × Implied Volatility] / [(Open Interest + 1) × (|Gamma| + |Theta| + 1)]
```

**Interpretation:**
- **> 0.02**: Aggressive or unusual trading (potential insider-like behavior)
- **0.004 – 0.01**: Normal market activity
- **< 0.003**: Inactive, conservative, or hedging behavior

## Setup Instructions

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/Anant-Madhok231/insider-trade-platform.git
   cd insider-trade-platform
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=True
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-password
   SECRET_KEY=your-secret-key-here
   ALPHA_VANTAGE_API_KEY=your-alpha-vantage-api-key
   FMP_API_KEY=your-fmp-api-key
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

   The app will be available at `http://localhost:5000`

## Deployment to Render (Free Hosting)

### Step 1: Push to GitHub

1. **Initialize git repository** (if not already done)
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **Create a new repository on GitHub**
   - Go to https://github.com/new
   - Repository name: `insider-trade-platform` (or your preferred name)
   - Make it public or private
   - Don't initialize with README (we already have one)

3. **Push to GitHub**
   ```bash
   git remote add origin https://github.com/Anant-Madhok231/insider-trade-platform.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Deploy on Render

1. **Sign up for Render**
   - Go to https://render.com
   - Sign up with your GitHub account (free tier available)

2. **Create a New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the repository you just pushed

3. **Configure the service**
   - **Name**: `insider-trade-platform` (or your choice)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`

4. **Set Environment Variables**
   
   In the Render dashboard, go to "Environment" and add:
   ```
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=True
   MAIL_USERNAME=insidertrade05@gmail.com
   MAIL_PASSWORD=cxiu rhyt fxea figg
   SECRET_KEY=<generate-a-random-secret-key>
   ALPHA_VANTAGE_API_KEY=T21J4YZC2W2M1WL5
   FMP_API_KEY=wsxz6HnLfi2bLaV7wFP3DDcDeAfLfKhz
   PYTHON_VERSION=3.11.0
   ```

   **To generate a SECRET_KEY:**
   ```python
   import secrets
   print(secrets.token_hex(32))
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Render will automatically build and deploy your app
   - Your app will be available at `https://your-app-name.onrender.com`

### Important Notes

- **Free tier limitations**: Render's free tier spins down after 15 minutes of inactivity. The first request after spin-down may take 30-60 seconds.
- **Environment variables**: Never commit sensitive keys to GitHub. Always use environment variables.
- **Database**: Currently using in-memory storage. For production, consider using a database like PostgreSQL (available on Render).

## Project Structure

```
.
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── models.py              # Database models
├── requirements.txt       # Python dependencies
├── Procfile              # Deployment configuration for Render
├── render.yaml           # Render deployment config
├── templates/            # HTML templates
├── static/               # CSS, JS, and other static files
└── README.md            # This file
```

## API Keys Required

- **Alpha Vantage API**: Get free key from https://www.alphavantage.co/support/#api-key
- **Financial Modeling Prep API**: Get free key from https://site.financialmodelingprep.com/developer/docs/
- **Gmail App Password**: For email verification, create an app password in your Google Account settings

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **APIs**: Alpha Vantage, Financial Modeling Prep, yfinance
- **Deployment**: Render, Gunicorn

## Copyright & License

**Copyright (c) 2025 Anant Madhok. All Rights Reserved.**

This software is proprietary and confidential. Unauthorized copying, modification, distribution, or use of this software, via any medium, is strictly prohibited without the express written permission of Anant Madhok.

### Permitted Use
- Personal, non-commercial use only
- Educational purposes (with attribution)

### Prohibited Use
- Commercial use without license
- Redistribution or resale
- Modification and distribution of derivative works
- Removal of copyright notices

### Licensing Inquiries
For licensing, commercial use, or collaboration inquiries, please contact:
- **GitHub**: [@Anant-Madhok231](https://github.com/Anant-Madhok231)

See [COPYRIGHT.txt](COPYRIGHT.txt) and [LICENSE](LICENSE) for full terms.

## Support

For issues or questions, please open an issue on GitHub or contact the copyright holder.

