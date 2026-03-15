# 🚀 Quick Share Setup

## Option 1: ngrok (Recommended - 2 minutes setup)

ngrok requires a free account, but it's quick:

1. **Sign up** (free): https://dashboard.ngrok.com/signup
2. **Get your authtoken**: https://dashboard.ngrok.com/get-started/your-authtoken
3. **Configure ngrok:**
   ```bash
   cd "/Users/shrijatewari/ZOMATHON PS 1"
   ./ngrok config add-authtoken YOUR_TOKEN_HERE
   ```
4. **Start tunnel:**
   ```bash
   ./ngrok http 8504
   ```
5. **Copy the URL** that appears (e.g., `https://abc123.ngrok-free.app`)

---

## Option 2: localtunnel (No signup, but needs manual install)

1. **Install localtunnel** (requires sudo):
   ```bash
   sudo npm install -g localtunnel
   ```

2. **Start tunnel:**
   ```bash
   lt --port 8504
   ```

3. **Copy the URL** that appears (e.g., `https://random-name.loca.lt`)

---

## Option 3: Cloudflare Tunnel (Free, no signup)

1. **Download cloudflared:**
   ```bash
   cd "/Users/shrijatewari/ZOMATHON PS 1"
   curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-amd64 -o cloudflared
   chmod +x cloudflared
   ```

2. **Start tunnel:**
   ```bash
   ./cloudflared tunnel --url http://localhost:8504
   ```

3. **Copy the URL** that appears

---

## ⚡ Fastest Right Now

**For immediate sharing, use ngrok (Option 1)** - it takes 2 minutes:
1. Go to https://dashboard.ngrok.com/signup
2. Copy your authtoken
3. Run: `cd "/Users/shrijatewari/ZOMATHON PS 1" && ./ngrok config add-authtoken YOUR_TOKEN`
4. Run: `./ngrok http 8504`
5. Share the URL!

---

## 📝 Remember

- Keep Streamlit running: `streamlit run app.py --server.port 8504`
- Keep the tunnel terminal open
- Share the HTTPS URL with your teammates
