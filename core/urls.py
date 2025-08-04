from django.urls import path
from .views import CustomerListView, CustomerDetailView, SectorInsightsAPIView

urlpatterns = [
    path('api/customers/', CustomerListView.as_view(), name='customer-list'),
    path('api/customers/<int:pk>/', CustomerDetailView.as_view(), name='customer-detail'),
    path('api/sector-insights/', SectorInsightsAPIView.as_view(), name='sector-insights'),
]
