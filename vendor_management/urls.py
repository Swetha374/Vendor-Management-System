from django.urls import path
from vendor_management.views import (
    VendorListCreateAPIView,
    VendorRetrieveUpdateDestroyAPIView,
    PurchaseOrderListCreateAPIView,
    PurchaseOrderRetrieveUpdateDestroyAPIView,
    VendorPerformanceAPIView,
    AcknowledgePurchaseOrder,
    TokenObtainView
)

urlpatterns = [
    path(
        "api/vendors/",
        VendorListCreateAPIView.as_view(),
    ),
    path(
        "api/vendors/<int:pk>/",
        VendorRetrieveUpdateDestroyAPIView.as_view(),
    ),
    path(
        "api/purchase_orders/",
        PurchaseOrderListCreateAPIView.as_view(),
    ),
    path(
        "api/purchase_orders/<int:pk>/",
        PurchaseOrderRetrieveUpdateDestroyAPIView.as_view(),
    ),
    path(
        "api/vendors/<int:pk>/performance/",
        VendorPerformanceAPIView.as_view(),
    ),
    path('api/purchase_orders/<int:po_id>/acknowledge/',
          AcknowledgePurchaseOrder.as_view(),),
     path('api/token/', TokenObtainView.as_view(),)

]
