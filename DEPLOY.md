# Deployment (always-on, free, no credit card)

**Do not use Render or PythonAnywhere** — both require payment. Use **Railway** (different product: free trial with $5 credit, **no card**).

## URL to share with interviewers (one link)

After Railway setup below, share your Railway app URL, e.g.:

`https://truck-trip-details-production.up.railway.app`

That single URL serves the React UI and the Django API (no Mac, no tunnel).

GitHub Pages (https://rahulagg1804.github.io/truck-trip-details/) stays available as a backup frontend only.

---

## One-time setup on Railway (~10 minutes)

1. Sign up: https://railway.com/ — **Sign in with GitHub** (no credit card on free trial)
2. Verify for full network access (needed for geocoding): https://railway.com/verify
3. **New Project** → **Deploy from GitHub repo** → `rahulagg1804/truck-trip-details`
4. Railway reads `railway.toml` at the repo root and builds frontend + backend
5. Open the service → **Variables** → add:
   - `DEBUG` = `false`
   - `ALLOWED_HOSTS` = `*`
   - `GEOCODING_ENABLED` = `true`
6. **Settings → Networking → Generate Domain** (if not already created)
7. Wait until deploy status is **Active** / green
8. Test:
   ```bash
   curl -s https://YOUR-RAILWAY-DOMAIN.up.railway.app/api/health/
   ```
   Expected: `{"status":"ok"}`
9. Open the same domain in a browser and plan a test trip

**Trial:** $5 credit for ~30 days — enough for an interview project. No sleep timer (unlike Render free tier).

---

## Optional: GitHub Pages + Railway API only

If you prefer the GitHub Pages URL for the UI:

1. Deploy on Railway with **Root Directory** = `backend` (API only)
2. Set GitHub variable `VITE_API_URL` = your Railway API URL (no `/api` suffix)
3. Re-run **Deploy to GitHub Pages**

---

## Hugging Face (not recommended)

The Space was paused (`Flagged as abusive` from a bad deploy that included `venv/`). Use Railway instead.

---

## Verify end-to-end

1. Health: `curl -s https://YOUR-DOMAIN/api/health/`
2. UI: open your Railway domain
3. Trip: Chicago → Indianapolis → Nashville
