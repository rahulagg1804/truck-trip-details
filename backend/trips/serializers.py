from rest_framework import serializers


class PlanTripSerializer(serializers.Serializer):
    current_location = serializers.CharField(max_length=500, trim_whitespace=True)
    pickup_location = serializers.CharField(max_length=500, trim_whitespace=True)
    dropoff_location = serializers.CharField(max_length=500, trim_whitespace=True)
    current_cycle_used = serializers.FloatField(min_value=0, max_value=70, default=0)

    def validate_current_location(self, value):
        if not value:
            raise serializers.ValidationError("This field is required.")
        return value

    def validate_pickup_location(self, value):
        if not value:
            raise serializers.ValidationError("This field is required.")
        return value

    def validate_dropoff_location(self, value):
        if not value:
            raise serializers.ValidationError("This field is required.")
        return value
