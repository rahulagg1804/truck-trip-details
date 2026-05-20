# Deployment (always-on, free)

## URLs to share with interviewers

| | URL |
|--|-----|
| **Application** | https://rahulagg1804.github.io/truck-trip-details/ |
| **API** | https://truck-trip-api.onrender.com *(after Render setup below)* |

The frontend on GitHub Pages is already always-on. You only need to deploy the API once on Render (free, no credit card).

---

## One-time API setup on Render (~10 minutes)

1. Sign up: https://dashboard.render.com/ (free tier, **no credit card** required)
2. **New +** → **Blueprint** → connect GitHub repo `rahulagg1804/truck-trip-details`
3. Render reads `render.yaml` and creates service **truck-trip-api**
4. Wait until the deploy is **Live** (first build ~5–10 min)
5. Open the service URL (default): **https://truck-trip-api.onrender.com**
6. Verify:
   ```bash
   curl -s https://truck-trip-api.onrender.com/api/health/
   ```
   Expected: `{"status":"ok"}`
7. Point the frontend at the API — GitHub repo **Settings → Secrets and variables → Actions → Variables**:
   - Name: `VITE_API_URL`
   - Value: `https://truck-trip-api.onrender.com`
8. **Actions → Deploy to GitHub Pages → Run workflow** (or push to `main`)

**Note:** Free Render services sleep after ~15 minutes of no traffic. The first request after sleep takes ~30–60 seconds to wake up; then the app works normally. Fine for interview demos.

---

## Frontend (GitHub Pages)

Already configured in `.github/workflows/deploy.yml` — deploys on every push to `main`.

1. **Settings → Pages → Source: GitHub Actions**
2. Site: https://rahulagg1804.github.io/truck-trip-details/

---

## Optional: Hugging Face Spaces (backup)

If Render is unavailable, use **Actions → Deploy API to Hugging Face** (requires `HF_TOKEN` secret). Default Space name: `truck-trip-planner-api`.

---

## Verify end-to-end

1. `curl -s https://truck-trip-api.onrender.com/api/health/`
2. Open https://rahulagg1804.github.io/truck-trip-details/
3. Plan a trip (e.g. Chicago → Indianapolis → Nashville)

If the UI loads but planning fails, check the browser Network tab — `VITE_API_URL` must match your live Render URL.
