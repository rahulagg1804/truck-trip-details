# Deployment

## URLs

| Service | URL |
|---------|-----|
| Application | https://rahulagg1804.github.io/truck-trip-details/ |
| API (Hugging Face) | https://rahulagg1804-truck-trip-api.hf.space |

The frontend deploys on push to `main` via GitHub Actions. The API runs on a free **Hugging Face Space** (Docker) or optionally **Railway** ($5/month credit, no card required for signup).

---

## Backend — Hugging Face Spaces (recommended, free)

1. Create a free account at https://huggingface.co/join
2. Create an access token: **Settings → Access Tokens → New token** (role: **write**)
3. In this GitHub repo: **Settings → Secrets and variables → Actions → New repository secret**
   - Name: `HF_TOKEN`
   - Value: your Hugging Face token
4. **Actions → Deploy API to Hugging Face → Run workflow**
5. Wait for the Space to build (~3–5 min). Open https://huggingface.co/spaces/rahulagg1804/truck-trip-api
6. When the Space is **Running**, set the repository variable (optional if using the default URL):
   - **Settings → Secrets and variables → Actions → Variables**
   - Name: `VITE_API_URL`
   - Value: `https://rahulagg1804-truck-trip-api.hf.space`
7. Re-run **Deploy to GitHub Pages** (or push to `main`) so the frontend picks up the API URL

Health check: `https://rahulagg1804-truck-trip-api.hf.space/api/health/`

---

## Backend — Railway (alternative)

1. Sign up at https://railway.com/ (free trial includes $5 credit, no card required for initial signup)
2. **New Project → Deploy from GitHub repo** → select `truck-trip-details`
3. Set **Root Directory** to `backend`
4. Add variables: `DEBUG=false`, `ALLOWED_HOSTS=*`, `CORS_ALLOWED_ORIGINS=https://rahulagg1804.github.io`, `GEOCODING_ENABLED=true`
5. Copy the public URL (e.g. `https://truck-trip-api-production.up.railway.app`)
6. Set GitHub variable `VITE_API_URL` to that URL and redeploy GitHub Pages

Or use **Actions → Deploy API to Railway** with secrets `RAILWAY_TOKEN` and variable `RAILWAY_SERVICE`.

---

## Frontend (GitHub Pages)

Configured in `.github/workflows/deploy.yml`.

1. Push to `main`
2. **Settings → Pages → Build and deployment → Source: GitHub Actions**
3. Site: https://rahulagg1804.github.io/truck-trip-details/

---

## Verify end-to-end

```bash
curl -s https://rahulagg1804-truck-trip-api.hf.space/api/health/
```

Then open the application URL, enter cities (e.g. Chicago → Nashville), and confirm the map and ELD logs load.
