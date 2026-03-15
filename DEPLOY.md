# PrepSense Deployment Guide

## GitHub Setup

Your repo includes:
- **prepsense/** – Streamlit dashboard + FastAPI backend
- **web/** – Next.js landing page
- **analysis/** – Advanced graphs

## Streamlit Cloud Deployment

Deploy the PrepSense dashboard to Streamlit Cloud (free):

### 1. Push to GitHub

```bash
cd "/Users/shrijatewari/ZOMATHON PS 1"
git add prepsense/ web/ analysis/ requirements.txt .gitignore DEPLOY.md
git status   # Review what will be committed
git commit -m "Add PrepSense Streamlit demo, landing page, and backend"
git push origin main
```

### 2. Deploy on Streamlit Cloud

1. Go to **https://share.streamlit.io**
2. Sign in with GitHub
3. Click **"New app"**
4. Select your repo: **shrijatewari/Zomathon-Repository**
5. Configure:
   - **Main file path:** `prepsense/app.py`
   - **Branch:** `main`
   - **Python version:** 3.11 (or 3.12)
6. Click **"Deploy!"**

### 3. After Deployment

- Your app will be at: `https://<your-app-name>.streamlit.app`
- **Note:** The Live Mode (WebSocket) features require the backend. For full functionality, deploy the backend separately (e.g., Railway, Render) and update the WebSocket URL in the app.

## Landing Page (Vercel)

Deploy the Next.js landing page to Vercel:

1. Go to **https://vercel.com**
2. Import your GitHub repo
3. Set **Root Directory** to `web`
4. Deploy

Update the landing page links to point to your Streamlit Cloud URL instead of `localhost:8504`.

## Backend (Optional – for Live Mode)

To enable WebSocket/Live Mode on Streamlit Cloud:

1. Deploy the backend to **Railway** or **Render**:
   - **Start command:** `cd prepsense/backend && uvicorn websocket_server:app --host 0.0.0.0 --port $PORT`
   - Set `PORT` from the platform (Railway/Render provide it)
2. Update `WEBSOCKET_URL` in `prepsense/app.py` to your deployed backend URL
3. Redeploy the Streamlit app
