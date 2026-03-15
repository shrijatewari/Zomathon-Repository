# Sharing Your PrepSense Dashboard

## Quick Start (Easiest - ngrok)

### Option 1: Basic ngrok (No signup, URL changes each time)

1. **Make sure Streamlit is running:**
   ```bash
   cd prepsense
   streamlit run app.py --server.port 8504
   ```

2. **In a NEW terminal, start ngrok:**
   ```bash
   cd "/Users/shrijatewari/ZOMATHON PS 1"
   ./ngrok http 8504
   ```

3. **Copy the Forwarding URL** (looks like `https://abc123.ngrok-free.app`)
   - Share this URL with your teammates
   - They can access your dashboard from anywhere!

### Option 2: ngrok with Persistent URL (Requires free signup)

1. **Sign up for free:** https://dashboard.ngrok.com/signup

2. **Get your authtoken** from: https://dashboard.ngrok.com/get-started/your-authtoken

3. **Configure ngrok:**
   ```bash
   cd "/Users/shrijatewari/ZOMATHON PS 1"
   ./ngrok config add-authtoken YOUR_TOKEN_HERE
   ```

4. **Start Streamlit** (if not already running):
   ```bash
   cd prepsense
   streamlit run app.py --server.port 8504
   ```

5. **Start ngrok tunnel:**
   ```bash
   cd "/Users/shrijatewari/ZOMATHON PS 1"
   ./ngrok http 8504
   ```

6. **Share the URL** - With authtoken, you can get a custom domain!

---

## Alternative: localtunnel (No signup, simpler)

1. **Install Node.js** (if not installed): https://nodejs.org/

2. **Install localtunnel:**
   ```bash
   npm install -g localtunnel
   ```

3. **Start Streamlit** (if not already running):
   ```bash
   cd prepsense
   streamlit run app.py --server.port 8504
   ```

4. **Start tunnel:**
   ```bash
   lt --port 8504
   ```

5. **Share the URL** that appears (e.g., `https://random-name.loca.lt`)

---

## Using the Helper Scripts

### Quick Share (ngrok):
```bash
cd prepsense
./share_dashboard.sh
```

### Alternative (localtunnel):
```bash
cd prepsense
./share_dashboard_alternative.sh
```

---

## Important Notes

⚠️ **Keep your terminal open** - The tunnel only works while the terminal is running

⚠️ **Keep Streamlit running** - Make sure `streamlit run app.py` is running in another terminal

⚠️ **Security** - Anyone with the URL can access your dashboard. Don't share publicly if you have sensitive data.

⚠️ **Performance** - Free ngrok has rate limits. For production, consider deploying to Streamlit Cloud (free).

---

## Troubleshooting

**"ngrok: command not found"**
- Make sure you're in the project directory where ngrok was downloaded
- Or add ngrok to your PATH

**"Address already in use"**
- Port 8504 might be in use. Change the port:
  ```bash
  streamlit run app.py --server.port 8505
  ./ngrok http 8505
  ```

**"Connection refused"**
- Make sure Streamlit is running first before starting ngrok

---

## For Production Deployment

If you want a permanent URL without keeping your computer on:

1. **Streamlit Cloud** (Free): https://streamlit.io/cloud
   - Push your code to GitHub
   - Connect GitHub repo to Streamlit Cloud
   - Get a permanent URL like `yourapp.streamlit.app`

2. **Heroku** (Free tier available)
3. **Railway** (Free tier available)
4. **Render** (Free tier available)
