from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from .models import User, Order, Company, Sector
from .serializers import UserListSerializer, UserDetailSerializer

class CustomerListView(APIView):
    def get(self, request):
        users = User.objects.annotate(order_count=Count('order'))
        serializer = UserListSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CustomerDetailView(APIView):
    def get(self, request, pk):
        try:
            user = User.objects.prefetch_related('order_set').get(pk=pk)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserDetailSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SectorInsightsAPIView(APIView):
    def get(self, request):
        sector_name = request.GET.get("sector")
        if not sector_name:
            return Response({"error": "Sector name is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            sector = Sector.objects.get(name__iexact=sector_name)
        except Sector.DoesNotExist:
            return Response({"error": "Sector not found"}, status=status.HTTP_404_NOT_FOUND)
        
        companies = Company.objects.filter(sector=sector)
        insights = []

        for company in companies:
            orders_count = Order.objects.filter(company=company).count()
            insights.append({
                "company_name": company.name,
                "orders_count": orders_count
            })

        return Response({
            "sector": sector.name,
            "companies": insights
        }, status=status.HTTP_200_OK)
