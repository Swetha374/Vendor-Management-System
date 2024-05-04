from django.urls import path
from vendor_management.views import (
    VendorListCreateAPIView,
    VendorRetrieveUpdateDestroyAPIView,
    PurchaseOrderListCreateAPIView,
    PurchaseOrderRetrieveUpdateDestroyAPIView,
    VendorPerformanceAPIView,
    AcknowledgePurchaseOrder,
    TokenObtainView,
    HistoricalPerformanceList,
)

urlpatterns = [
    path("api/vendors/", VendorListCreateAPIView.as_view(), name="vendor-list-create"),
    path(
        "api/vendors/<int:pk>/",
        VendorRetrieveUpdateDestroyAPIView.as_view(),
        name="vendor-retrieve-update-destroy",
    ),
    path(
        "api/purchase_orders/",
        PurchaseOrderListCreateAPIView.as_view(),
        name="purchase-order-list-create",
    ),
    path(
        "api/purchase_orders/<int:pk>/",
        PurchaseOrderRetrieveUpdateDestroyAPIView.as_view(),
        name="purchase-order-retrieve-update-destroy",
    ),
    path(
        "api/vendors/<int:pk>/performance/",
        VendorPerformanceAPIView.as_view(),
        name="vendor-performance",
    ),
    path(
        "api/purchase_orders/<int:po_id>/acknowledge/",
        AcknowledgePurchaseOrder.as_view(),
        name="acknowledge-purchase-order",
    ),
    path("api/token/", TokenObtainView.as_view(), name="token-obtain"),
    path(
        "api/historical_performance/",
        HistoricalPerformanceList.as_view(),
        name="historical-performance-list",
    ),
]
