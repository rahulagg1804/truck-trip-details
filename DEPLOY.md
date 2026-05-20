# Deployment

## URLs

| Service | URL |
|---------|-----|
| Application | https://rahulagg1804.github.io/truck-trip-details/ |
| API | https://rahulagg1804.pythonanywhere.com |

The frontend deploys on push to `main` via GitHub Actions. The API runs on PythonAnywhere.

---

## Backend (PythonAnywhere)

1. Create an account at https://www.pythonanywhere.com/
2. Open **Consoles** → **Bash** and run:

```bash
curl -sL https://raw.githubusercontent.com/rahulagg1804/truck-trip-details/main/deploy/pa-console-setup.sh | bash
```

3. **Web** → **Add a new web app** → Manual configuration → Python 3.10
4. Set virtualenv: `/home/rahulagg1804/truck-trip-details/backend/venv`
5. Replace the WSGI file with the contents of `deploy/pythonanywhere_wsgi.py` (update `YOUR_USERNAME`)
6. Click **Reload**

**CORS errors from GitHub Pages:** the WSGI file must allow `https://rahulagg1804.github.io` (no path). Use `deploy/pythonanywhere_wsgi.py` as-is, then **Reload**.

**Automated setup (optional):** add GitHub secret `PA_API_TOKEN` from [Account → API Token](https://www.pythonanywhere.com/account/#api_token), then run the **Deploy API to PythonAnywhere** workflow. Or locally: `PA_API_TOKEN=... ./deploy/pa-remote-setup.sh`.

If geocoding or routing fails, allow outbound access to `nominatim.openstreetmap.org` and `router.project-osrm.org` in the Web tab.

Health check: `https://rahulagg1804.pythonanywhere.com/api/health/`

---

## Frontend (GitHub Pages)

Configured in `.github/workflows/deploy.yml`.

1. Push to `main`
2. In the repository: **Settings** → **Pages** → **Build and deployment** → Source: **GitHub Actions**
3. When the workflow completes, the site is available at the application URL above

Set the repository variable `VITE_API_URL` if the API hostname differs from the default.
