from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import RegistrationForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created successfully!')
            return redirect('login')  # Replace 'login' with your login view URL name
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegistrationForm()

    return render(request, 'activities/registeration.html', {'form': form})

from rest_framework import generics, permissions
from .models import Activity
from .serializers import ActivitySerializer
from django.db.models import Q
from rest_framework.filters import OrderingFilter
from .pagination import ActivityPagination

class ActivityListCreateView(generics.ListCreateAPIView):
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = ActivityPagination
    filter_backends = [OrderingFilter]
    ordering_fields = ['date', 'duration', 'calories_burned']
    ordering = ['date']  # Default ordering

    def get_queryset(self):
        queryset = Activity.objects.filter(user=self.request.user)
        
        # Optional filters
        activity_type = self.request.query_params.get('activity_type')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if activity_type:
            queryset = queryset.filter(activity_type=activity_type)
        
        if start_date and end_date:
            queryset = queryset.filter(date__range=[start_date, end_date])
        
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class ActivityRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Activity.objects.filter(user=self.request.user)

from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum
from rest_framework.decorators import api_view

class ActivitySummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        activities = Activity.objects.filter(user=user)
        
        if start_date and end_date:
            activities = activities.filter(date__range=[start_date, end_date])

        summary = activities.aggregate(
            total_duration=Sum('duration'),
            total_distance=Sum('distance'),
            total_calories_burned=Sum('calories_burned')
        )

        return Response(summary)
