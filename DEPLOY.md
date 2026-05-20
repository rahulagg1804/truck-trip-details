# Deployment

## URLs

| Service | URL |
|---------|-----|
| Application | https://rahulagg1804.github.io/truck-trip-details/ |
| API | https://rahulagg1804-truck-trip-api.hf.space |

The frontend deploys on push to `main` via GitHub Actions. The API runs on a free **Hugging Face Space** (Docker).

---

## Backend (Hugging Face Spaces)

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
