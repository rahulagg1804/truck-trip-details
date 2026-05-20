from django.urls import path

from .views import PlanTripView, health

urlpatterns = [
    path("health/", health),
    path("plan-trip/", PlanTripView.as_view()),
]
