# Quick Deployment Guide

## Step 1: Push to GitHub

Run these commands in your terminal:

```bash
cd "/Users/anantmadhok/Desktop/insider 2 copy 2"

# Create a new repository on GitHub first, then:
git remote add origin https://github.com/Anant-Madhok231/insider-trade-platform.git
git branch -M main
git push -u origin main
```

**OR** if you want to use a different repository name:

1. Go to https://github.com/new
2. Create a new repository (e.g., `insider-trade-platform`)
3. Copy the repository URL
4. Run:
   ```bash
   git remote add origin <YOUR_REPO_URL>
   git branch -M main
   git push -u origin main
   ```

## Step 2: Deploy on Render (Free Hosting)

1. **Sign up/Login to Render**
   - Go to https://render.com
   - Sign up with your GitHub account

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub account if not already connected
   - Select your repository: `insider-trade-platform`

3. **Configure Settings**
   - **Name**: `insider-trade-platform` (or your choice)
   - **Environment**: `Python 3`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: (leave empty)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`

4. **Add Environment Variables**
   
   Click "Advanced" → "Add Environment Variable" and add these:
   
   ```
   MAIL_SERVER = smtp.gmail.com
   MAIL_PORT = 587
   MAIL_USE_TLS = True
   MAIL_USERNAME = insidertrade05@gmail.com
   MAIL_PASSWORD = cxiu rhyt fxea figg
   SECRET_KEY = <generate-random-key>
   ALPHA_VANTAGE_API_KEY = T21J4YZC2W2M1WL5
   FMP_API_KEY = wsxz6HnLfi2bLaV7wFP3DDcDeAfLfKhz
   PYTHON_VERSION = 3.11.0
   ```
   
   **To generate SECRET_KEY**, run this in Python:
   ```python
   import secrets
   print(secrets.token_hex(32))
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Wait for build to complete (5-10 minutes first time)
   - Your app will be live at: `https://insider-trade-platform.onrender.com`

## Step 3: Update GitHub Repository (Optional)

After deployment, you can add the live URL to your GitHub repository:
- Go to your GitHub repo → Settings → Pages (if using GitHub Pages for docs)
- Or add the Render URL to your README.md

## Troubleshooting

- **Build fails**: Check the build logs in Render dashboard
- **App crashes**: Check the logs tab in Render
- **Environment variables not working**: Make sure they're set in Render dashboard, not in code
- **Slow first load**: Render free tier spins down after 15 min inactivity - first request may be slow

## Next Steps

- Your app is now live! Share the Render URL with others
- Monitor usage in Render dashboard
- Consider upgrading to paid tier for better performance (no spin-down)

