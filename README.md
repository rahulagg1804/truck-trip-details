# Truck Trip Planner

Django + React app — trip inputs in, route + daily log sheets out.

## Setup

**Backend**

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py runserver 8000
```

**Frontend**

```bash
cd frontend
npm install
npm run dev
```

App runs at http://localhost:5173 (API proxied to port 8000).

## API

`POST /api/plan-trip/`

```json
{
  "current_location": "Chicago, IL",
  "pickup_location": "Indianapolis, IN",
  "dropoff_location": "Nashville, TN",
  "current_cycle_used": 12
}
```

## Assumptions

- Property carrier, 70 hours / 8 days
- Fuel every 1,000 miles
- 1 hour on duty at pickup and dropoff
- 11 hr drive / 14 hr window / 30 min break / 10 hr sleeper reset

## Project layout

```
frontend/src/
  api.js                 # axios client
  constants/             # trip form fields, stop icons, log grid
  hooks/usePlanTrip.js   # trip submit state
  utils/                 # errors, export, formatting
  components/
    ui/                  # Button, FormField, Card, Alert, StatCard
    icons/               # lucide icon map
    layout/AppHeader.jsx
    TripForm.jsx
    TripResults/         # results sections
    EldLogSheet/         # log grid + export
    RouteMap.jsx
backend/trips/
  serializers.py         # request validation
  services/              # geocoding, routing, hos_planner
  views.py
```

## Deploy

- Backend: Railway, Render, etc.
- Frontend: Vercel — set `VITE_API_URL` to the backend URL
