from rest_framework import generics
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .serializers import (
    VendorSerializer,
    PurchaseOrderSerializer,
    UserCredentialsSerializer,
    HistoricalPerformanceSerializer,
)
from rest_framework.response import Response
from django.db.models import Avg, F
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_400_BAD_REQUEST


# vendor
class VendorListCreateAPIView(generics.ListCreateAPIView):
    """
    List and create vendors.
    Retrieves a list of all vendors or creates a new vendor.
    """

    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [
        IsAuthenticated,
    ]


class VendorRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a vendor.
    Retrieves, updates, or deletes a specific vendor by its ID.
    """

    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    allowed_methods = ("GET", "PUT", "DELETE")
    authentication_classes = [TokenAuthentication]
    permission_classes = [
        IsAuthenticated,
    ]


# purchase order
class PurchaseOrderListCreateAPIView(generics.ListCreateAPIView):
    """
    List and create purchase orders.
    Retrieves a list of all purchase orders or creates a new purchase order.
    """

    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [
        IsAuthenticated,
    ]


class PurchaseOrderRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a purchase order.
    Retrieves, updates, or deletes a specific purchase order by its ID.
    """

    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    allowed_methods = ("GET", "PUT", "DELETE")
    authentication_classes = [TokenAuthentication]
    permission_classes = [
        IsAuthenticated,
    ]


# vendor performance
class VendorPerformanceAPIView(generics.RetrieveAPIView):
    """
    Retrieve vendor performance metrics.

    Retrieves performance metrics for a specific vendor.
    """

    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [
        IsAuthenticated,
    ]

    def retrieve(self, request, *args, **kwargs):
        """
        Calculate and return vendor performance metrics.

        Calculates and returns performance metrics such as on-time delivery rate,
        quality rating average, average response time, and fulfillment rate.
        """
        instance = self.get_object()
        performance_data = self.calculate_performance(instance)
        return Response(performance_data)

    def calculate_performance(self, vendor):
        """
        Calculate vendor performance metrics.

        Calculates performance metrics such as on-time delivery rate,
        quality rating average, average response time, and fulfillment rate.
        """
        total_orders = vendor.purchase_orders.count()
        acknowledged_orders = vendor.purchase_orders.filter(
            acknowledgment_date__isnull=False
        ).count()  # Filter only acknowledged orders
        if total_orders == 0:
            return {
                "on_time_delivery_rate": 0,
                "quality_rating_avg": 0,
                "average_response_time": 0,
                "fulfillment_rate": 0,
            }

        # Calculate metrics based on acknowledged orders
        on_time_orders = vendor.purchase_orders.filter(
            status="completed", delivery_date__lt=F("acknowledgment_date")
        ).count()
        on_time_delivery_rate = (
            (on_time_orders / acknowledged_orders) * 100
            if acknowledged_orders > 0
            else 0
        )

        avg_quality_rating = (
            vendor.purchase_orders.filter(
                quality_rating__isnull=False, acknowledgment_date__isnull=False
            ).aggregate(avg_quality=Avg("quality_rating"))["avg_quality"]
            or 0
        )

        # avg_response_time = (
        #     vendor.purchase_orders.filter(acknowledgment_date__isnull=False)
        #     .aggregate(avg_response=Avg(F("acknowledgment_date") - F("issue_date")))[
        #         "avg_response"
        #     ]
        #     .total_seconds()
        #     / 3600
        #     if acknowledged_orders > 0
        #     else 0
        # )

        avg_response_time_seconds = (
            vendor.purchase_orders.filter(acknowledgment_date__isnull=False)
            .aggregate(avg_response=Avg(F("acknowledgment_date") - F("issue_date")))[
                "avg_response"
            ]
            .total_seconds()
            if acknowledged_orders > 0
            else 0
        )

        avg_response_time_hours = int(avg_response_time_seconds // 3600)
        avg_response_time_minutes = int((avg_response_time_seconds % 3600) // 60)
        avg_response_time_seconds = int(avg_response_time_seconds % 60)

        avg_response_time = "{:02d}:{:02d}:{:02d}".format(
            avg_response_time_hours,
            avg_response_time_minutes,
            avg_response_time_seconds,
        )

        fulfilled_orders = vendor.purchase_orders.filter(
            status="completed", issue_date__isnull=False
        ).count()
        fulfillment_rate = (
            (fulfilled_orders / acknowledged_orders) * 100
            if acknowledged_orders > 0
            else 0
        )

        performance_data = {
            "on_time_delivery_rate": on_time_delivery_rate,
            "quality_rating_avg": avg_quality_rating,
            "average_response_time": avg_response_time,
            "fulfillment_rate": fulfillment_rate,
        }
        return performance_data


class AcknowledgePurchaseOrder(APIView):
    """
    Acknowledge a purchase order.
    Acknowledges a specific purchase order by its ID.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request, po_id):
        # Retrieve the purchase order
        purchase_order = get_object_or_404(PurchaseOrder, pk=po_id)

        # Check if the purchase order has already been acknowledged
        if purchase_order.acknowledgment_date:
            return Response(
                {"error": "Purchase order already acknowledged"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Update the acknowledgment date
        purchase_order.acknowledgment_date = timezone.now()
        purchase_order.save()

        # Calculate the new average response time
        vendor = purchase_order.vendor
        total_acknowledged_orders = vendor.purchase_orders.filter(
            acknowledgment_date__isnull=False
        ).count()
        total_response_time_seconds = sum(
            (po.acknowledgment_date - po.issue_date).total_seconds()
            for po in vendor.purchase_orders.filter(acknowledgment_date__isnull=False)
        )
        new_avg_response_time = (
            total_response_time_seconds / total_acknowledged_orders
            if total_acknowledged_orders > 0
            else 0
        )

        # Update the average_response_time field of the Vendor model
        vendor.average_response_time = new_avg_response_time
        vendor.save()

        return Response(
            {"success": "Purchase order acknowledged successfully"},
            status=status.HTTP_200_OK,
        )


class HistoricalPerformanceList(generics.ListAPIView):
    """
    Retrieve a list of historical performance records.
    Retrieves a paginated list of all historical performance records.
    """

    queryset = HistoricalPerformance.objects.all()
    serializer_class = HistoricalPerformanceSerializer


# Token authentication
class TokenObtainView(generics.CreateAPIView):
    """
    Obtain authentication token.
    Obtain authentication token using provided username and password.
    """

    serializer_class = UserCredentialsSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get("username")
        password = serializer.validated_data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        else:
            return Response(
                {"error": "Invalid credentials"}, status=HTTP_400_BAD_REQUEST
            )
