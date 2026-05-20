from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import PlanTripSerializer
from .services.geocoding import geocode
from .services.hos_planner import plan_trip
from .services.routing import get_route


def health(request):
    return JsonResponse({"status": "ok"})


class PlanTripView(APIView):
    def post(self, request):
        serializer = PlanTripSerializer(data=request.data)
        if not serializer.is_valid():
            errors = serializer.errors
            first = next(iter(errors.values()))[0]
            return Response({"error": str(first)}, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        current = data["current_location"]
        pickup = data["pickup_location"]
        dropoff = data["dropoff_location"]
        cycle_used = data["current_cycle_used"]

        try:
            waypoints = [geocode(current), geocode(pickup), geocode(dropoff)]
            route = get_route(waypoints)
            plan = plan_trip(
                route=route,
                waypoints=waypoints,
                cycle_used_hours=cycle_used,
            )
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exc:
            return Response({"error": str(exc)}, status=status.HTTP_502_BAD_GATEWAY)

        return Response(
            {
                "route": route,
                "plan": plan,
                "inputs": {
                    "current_location": current,
                    "pickup_location": pickup,
                    "dropoff_location": dropoff,
                    "current_cycle_used": cycle_used,
                },
            }
        )
