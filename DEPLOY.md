# Deploy

## Live URLs (update after deploy)

| App | URL |
|-----|-----|
| Frontend | _set after Vercel deploy_ |
| Backend API | _set after Render deploy_ |

## 1. Backend — Render

1. https://dashboard.render.com → **New** → **Blueprint**
2. Connect repo `rahulagg1804/truck-trip-details`
3. Apply `render.yaml` (creates API + static site)
4. For **truck-trip-web**, set env `VITE_API_URL` = `https://truck-trip-api.onrender.com` (your API URL)
5. Redeploy **truck-trip-web** after setting the variable

## 2. Frontend only — Vercel (alternative)

```bash
cd frontend
npx vercel --prod
```

Set `VITE_API_URL` in Vercel project settings to your Render API URL.

## 3. CORS

In Render **truck-trip-api** → Environment:

```
CORS_ALLOWED_ORIGINS=https://your-frontend-url.vercel.app
```

Or for Render static frontend:

```
CORS_ALLOWED_ORIGINS=https://truck-trip-web.onrender.com
```
