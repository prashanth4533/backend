from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import permission_classes
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
import json
from .models import Vehicle
from .serializers import VehicleSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Vehicle  
import json
import requests
from django.http import JsonResponse
from django.conf import settings
from django.core.mail import send_mail
from django.utils.crypto import get_random_string


# Register View
@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        username = data.get('uname1')
        email = data.get('email')
        password = data.get('upswd1')
        confirm_password = data.get('upswd2')

        # Password validation
        if password != confirm_password:
            return Response({'success': False, 'message': 'Passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check for missing fields
        if not username or not email or not password or not confirm_password:
            return Response({'success': False, 'message': 'All fields are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if username or email is taken
        if User.objects.filter(username=username).exists():
            return Response({'success': False, 'message': 'Username already taken.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(email=email).exists():
            return Response({'success': False, 'message': 'Email already registered.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create user
        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password)  # Password hashing
        )

        return Response({'success': True, 'message': 'Registration successful.'}, status=status.HTTP_201_CREATED)

# User Login View
@api_view(['POST'])

def login(request):
    username = request.data.get('uname')
    password = request.data.get('upswd')
    user = authenticate(username=username, password=password)

    if user is not None:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"message": "Login successful", "token": token.key}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def forgot_password(request):
    email = request.data.get('email')

    if not email:
        return Response({'message': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)
        reset_token = get_random_string(length=32)
        user.profile.reset_token = reset_token
        user.profile.save()

        reset_link = f"http://localhost:3000/reset-password/{reset_token}"
        send_mail(
            'Password Reset Request',
            f'Click the link to reset your password: {reset_link}',
            'admin@example.com',
            [email],
            fail_silently=False,
        )

        return Response({'message': 'Password reset link has been sent to your email.'}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'message': 'No user found with this email address.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_vehicle(request):
   
        # Extract data from the request
        vehicle_type = request.data.get("vehicleType")
        vehicle_model = request.data.get("vehicleModel")
        model_year = request.data.get("modelYear")
        rc_number = request.data.get("rcNumber")
        license_number = request.data.get("licenseNumber")

        # Validate required fields
        if not all([vehicle_type, vehicle_model, model_year, rc_number, license_number]):
            return Response({"message": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Create the vehicle object
        vehicle = Vehicle.objects.create(
            vehicle_type=vehicle_type,
            vehicle_model=vehicle_model,
            model_year=model_year,
            rc_number=rc_number,
            license_number=license_number,
            owner=request.user  # Associate with the logged-in user
        )

       
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_vehicles(request):
    if not request.user.is_authenticated:
        return Response({"message": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

    # Fetch vehicles associated with the logged-in user
    vehicles = Vehicle.objects.filter(owner=request.user)

    # If no vehicles found, return an empty list
    if not vehicles:
        return Response([], status=status.HTTP_200_OK)

    # Prepare vehicle data for the response
    vehicle_data = [{
        "vehicleType": vehicle.vehicle_type,
        "vehicleModel": vehicle.vehicle_model,
        "modelYear": vehicle.model_year,
        "rcNumber": vehicle.rc_number,
        "licenseNumber": vehicle.license_number,
    } for vehicle in vehicles]

    return Response(vehicle_data, status=status.HTTP_200_OK)


@csrf_exempt
@permission_classes([IsAuthenticated])
def vehicle_list(request):
    if request.method == 'GET':
        # Retrieve vehicles for the logged-in user
        vehicles = Vehicle.objects.filter(user=request.user)  # Assuming each vehicle is linked to a user
        vehicle_data = list(vehicles.values('vehicleType', 'vehicleModel', 'modelYear', 'rcNumber', 'licenseNumber'))
        return JsonResponse(vehicle_data, safe=False)

    elif request.method == 'POST':
        # Create a new vehicle for the logged-in user
        vehicle_data = json.loads(request.body)
        new_vehicle = Vehicle.objects.create(
            user=request.user,
            vehicleType=vehicle_data['vehicleType'],
            vehicleModel=vehicle_data['vehicleModel'],
            modelYear=vehicle_data['modelYear'],
            rcNumber=vehicle_data['rcNumber'],
            licenseNumber=vehicle_data['licenseNumber'],
        )
        return JsonResponse({'message': 'Vehicle added successfully'}, status=201)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
def create_order(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            amount = body.get("amount", "0.00")

            # Get PayPal access token
            auth_response = requests.post(
                f"{settings.PAYPAL_API_URL}/v1/oauth2/token",
                auth=(settings.PAYPAL_CLIENT_ID, settings.PAYPAL_SECRET),
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data={"grant_type": "client_credentials"},
            )
            auth_response.raise_for_status()
            access_token = auth_response.json()["access_token"]

            # Create PayPal order
            order_response = requests.post(
                f"{settings.PAYPAL_API_URL}/v2/checkout/orders",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/json",
                },
                json={
                    "intent": "CAPTURE",
                    "purchase_units": [{"amount": {"currency_code": "USD", "value": amount}}],
                },
            )
            order_response.raise_for_status()
            approval_url = next(
                link["href"]
                for link in order_response.json()["links"]
                if link["rel"] == "approve"
            )

            return JsonResponse({"approval_url": approval_url}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)
# Refresh Token View
@api_view(['POST'])
def refresh_token_view(request):
    refresh_token = request.data.get('refresh')

    if not refresh_token:
        return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        refresh = RefreshToken(refresh_token)
        access_token = str(refresh.access_token)
        return Response({
            "access": access_token,
            "refresh": str(refresh)
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    # Any custom logic, like adding extra claims, etc.
    pass
# User Logout View
@api_view(['POST'])
def user_logout(request):
    return Response({"message": "Logged out successfully. Please remove your token from the client."}, status=200)
