from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('vehicle-list/', views.vehicle_list, name='vehicle-list'),
    path('get_vehicles/', views.get_vehicles, name='get_vehicles'),
    path('add_vehicle/', views.add_vehicle, name='add_vehicle'),
    path('token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("create-order/", views.create_order, name="create-order"),
    path('refresh-token/', views.refresh_token_view, name='refresh_token'),
    path('logout/', views.user_logout, name='logout'),
]
