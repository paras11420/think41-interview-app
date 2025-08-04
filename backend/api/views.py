from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db.models import Count
import json
from .models import Task, User, Order

# Existing task views (keep these)
@csrf_exempt
def task_list(request):
    if request.method == 'GET':
        tasks = []
        for task in Task.objects.all():
            tasks.append({
                'id': task.id,
                'title': task.title,
                'completed': task.completed,
                'created_at': task.created_at.isoformat()
            })
        return JsonResponse({'tasks': tasks})
    
    elif request.method == 'POST':
        data = json.loads(request.body)
        task = Task.objects.create(title=data['title'])
        return JsonResponse({
            'id': task.id, 
            'title': task.title, 
            'completed': task.completed,
            'created_at': task.created_at.isoformat()
        })

@csrf_exempt
def task_detail(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return JsonResponse({'error': 'Task not found'}, status=404)
    
    if request.method == 'PUT':
        data = json.loads(request.body)
        task.completed = data.get('completed', task.completed)
        task.title = data.get('title', task.title)
        task.save()
        return JsonResponse({
            'id': task.id,
            'title': task.title,
            'completed': task.completed,
            'created_at': task.created_at.isoformat()
        })
    
    elif request.method == 'DELETE':
        task.delete()
        return JsonResponse({'success': True})

# NEW: Customer API endpoints for Milestone 2
@csrf_exempt
def customer_list(request):
    """List all customers with pagination"""
    try:
        # Get page number from query params (default: 1)
        page_num = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 20))
        
        # Get all customers with order count
        customers_queryset = User.objects.annotate(
            order_count=Count('order')
        ).order_by('id')
        
        # Paginate
        paginator = Paginator(customers_queryset, page_size)
        page = paginator.get_page(page_num)
        
        # Build response
        customers = []
        for customer in page:
            customers.append({
                'id': customer.id,
                'first_name': customer.first_name,
                'last_name': customer.last_name,
                'email': customer.email,
                'age': customer.age,
                'gender': customer.gender,
                'city': customer.city,
                'state': customer.state,
                'country': customer.country,
                'order_count': customer.order_count,
                'created_at': customer.created_at.isoformat()
            })
        
        return JsonResponse({
            'customers': customers,
            'pagination': {
                'current_page': page.number,
                'total_pages': paginator.num_pages,
                'total_customers': paginator.count,
                'has_next': page.has_next(),
                'has_previous': page.has_previous()
            }
        }, status=200)
        
    except ValueError:
        return JsonResponse({'error': 'Invalid page number'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def customer_detail(request, customer_id):
    """Get specific customer details with order analytics"""
    try:
        # Validate customer_id is integer
        try:
            customer_id = int(customer_id)
        except ValueError:
            return JsonResponse({'error': 'Invalid customer ID format'}, status=400)
        
        # Get customer or return 404
        try:
            customer = User.objects.get(id=customer_id)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Customer not found'}, status=404)
        
        # Get customer's orders
        orders = Order.objects.filter(user=customer)
        
        # Calculate analytics
        total_orders = orders.count()
        completed_orders = orders.filter(status='Complete').count()
        cancelled_orders = orders.filter(status='Cancelled').count()
        pending_orders = orders.filter(status='Pending').count()
        total_items = sum(order.num_of_item for order in orders)
        
        # Recent orders (last 5)
        recent_orders = []
        for order in orders.order_by('-created_at')[:5]:
            recent_orders.append({
                'order_id': order.order_id,
                'status': order.status,
                'num_of_item': order.num_of_item,
                'created_at': order.created_at.isoformat()
            })
        
        response_data = {
            'customer': {
                'id': customer.id,
                'first_name': customer.first_name,
                'last_name': customer.last_name,
                'email': customer.email,
                'age': customer.age,
                'gender': customer.gender,
                'city': customer.city,
                'state': customer.state,
                'country': customer.country,
                'street': customer.street,
                'postal_code': customer.postal_code,
                'traffic_src': customer.traffic_src,
                'created_at': customer.created_at.isoformat()
            },
            'order_analytics': {
                'total_orders': total_orders,
                'completed_orders': completed_orders,
                'cancelled_orders': cancelled_orders,
                'pending_orders': pending_orders,
                'total_items_ordered': total_items
            },
            'recent_orders': recent_orders
        }
        
        return JsonResponse(response_data, status=200)
        
    except Exception as e:
        return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)

@csrf_exempt
def customer_order_count(request, customer_id):
    """Get customer order count specifically"""
    try:
        # Validate customer_id
        try:
            customer_id = int(customer_id)
        except ValueError:
            return JsonResponse({'error': 'Invalid customer ID format'}, status=400)
        
        # Check if customer exists
        try:
            customer = User.objects.get(id=customer_id)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Customer not found'}, status=404)
        
        # Get order count
        order_count = Order.objects.filter(user=customer).count()
        
        return JsonResponse({
            'customer_id': customer.id,
            'customer_name': f"{customer.first_name} {customer.last_name}",
            'order_count': order_count
        }, status=200)
        
    except Exception as e:
        return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)
