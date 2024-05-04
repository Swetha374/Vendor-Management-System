from rest_framework import serializers
from .models import Vendor, PurchaseOrder, HistoricalPerformance


class VendorSerializer(serializers.ModelSerializer):
    average_response_time = serializers.SerializerMethodField()

    class Meta:
        model = Vendor
        fields = "__all__"

    def get_average_response_time(self, obj):
        """
        Retrieve the average response time of the vendor in a human-readable format.
        Args:
            obj: An instance of Vendor.
        Returns:
            str: A string representation of the average response time in the format HH:MM:SS.
        """
        # Assuming obj is an instance of Vendor
        avg_response_time_seconds = obj.average_response_time

        # Convert seconds to hours, minutes, and seconds
        avg_response_time_hours = int(avg_response_time_seconds // 3600)
        avg_response_time_minutes = int((avg_response_time_seconds % 3600) // 60)
        avg_response_time_seconds = int(avg_response_time_seconds % 60)

        # Format the response time as HH:MM:SS
        return "{:02d}:{:02d}:{:02d}".format(
            avg_response_time_hours,
            avg_response_time_minutes,
            avg_response_time_seconds,
        )


class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = "__all__"


class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPerformance
        fields = "__all__"


class UserCredentialsSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
