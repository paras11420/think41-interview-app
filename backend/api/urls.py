from django.urls import path
from . import views

urlpatterns = [
    # Task endpoints (existing)
    path('tasks/', views.task_list, name='task-list'),
    path('tasks/<int:task_id>/', views.task_detail, name='task-detail'),
    
    # NEW: Customer API endpoints for Milestone 2
    path('customers/', views.customer_list, name='customer-list'),
    path('customers/<int:customer_id>/', views.customer_detail, name='customer-detail'),
    path('customers/<int:customer_id>/order-count/', views.customer_order_count, name='customer-order-count'),
]
