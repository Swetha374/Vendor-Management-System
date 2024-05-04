from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Vendor, PurchaseOrder, HistoricalPerformance


class APITest(APITestCase):
    def setUp(self):
        # Creating a test user
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        # Creating a token for authentication
        self.token = Token.objects.create(user=self.user)
        # Creating a test vendor
        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            contact_details="Test Contact",
            address="Test Address",
            vendor_code="TEST123",
        )
        # Creating a test purchase order
        self.purchase_order = PurchaseOrder.objects.create(
            po_number="PO123",
            vendor=self.vendor,
            order_date="2024-05-04T12:00:00Z",
            delivery_date="2024-05-04T12:00:00Z",
            items=[],
            quantity=10,
            status="pending",
            issue_date="2024-05-04T12:00:00Z",
        )
        # Creating a test historical performance record
        self.historical_performance = HistoricalPerformance.objects.create(
            vendor=self.vendor,
            date="2024-05-04T12:00:00Z",
            on_time_delivery_rate=80,
            quality_rating_avg=4.5,
            average_response_time=2.5,
            fulfillment_rate=90,
        )

    # Test case for listing and creating vendors
    def test_vendor_list_create(self):
        url = reverse("vendor-list-create")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {
            "name": "New Vendor",
            "contact_details": "New Contact",
            "address": "New Address",
            "vendor_code": "NEW123",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Test case for retrieving, updating, and deleting a vendor
    def test_vendor_retrieve_update_destroy(self):
        url = reverse("vendor-retrieve-update-destroy", kwargs={"pk": self.vendor.pk})
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {
            "name": "Updated Vendor",
            "contact_details": "string",
            "address": "string",
            "vendor_code": "string",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # Test case for listing and creating purchase orders
    def test_purchase_order_list_create(self):
        url = reverse("purchase-order-list-create")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {
            "po_number": "PO456",
            "vendor": self.vendor.pk,
            "order_date": "2024-05-04T12:00:00Z",
            "delivery_date": "2024-05-04T12:00:00Z",
            "items": [],
            "quantity": 20,
            "status": "pending",
            "issue_date": "2024-05-04T12:00:00Z",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Test case for retrieving, updating, and deleting a purchase order
    def test_purchase_order_retrieve_update_destroy(self):
        url = reverse(
            "purchase-order-retrieve-update-destroy",
            kwargs={"pk": self.purchase_order.pk},
        )
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {
            "quantity": 30,
            "vendor": 1,
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # Test case for retrieving vendor performance
    def test_vendor_performance(self):
        url = reverse("vendor-performance", kwargs={"pk": self.vendor.pk})
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test case for acknowledging a purchase order
    def test_acknowledge_purchase_order(self):
        url = reverse(
            "acknowledge-purchase-order", kwargs={"po_id": self.purchase_order.pk}
        )
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test case for listing historical performance records
    def test_historical_performance_list(self):
        url = reverse("historical-performance-list")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test case for obtaining a token
    def test_token_obtain_view(self):
        url = reverse("token-obtain")
        data = {"username": "testuser", "password": "testpassword"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
