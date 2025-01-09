from django.urls import path
from .views import register, ActivityListCreateView, ActivityRetrieveUpdateDestroyView,ActivitySummaryView
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(template_name='activities/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('', ActivityListCreateView.as_view(), name='activity-list-create'),
    path('<int:pk>/', ActivityRetrieveUpdateDestroyView.as_view(), name='activity-detail'),
    path('summary/', ActivitySummaryView.as_view(), name='activity-summary'),
]