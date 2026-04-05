import datetime
import json

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

from sonat_app.forms import LoginForm, RegisterForm
from sonat_app.models import User, UserConnection, UserProfile


@csrf_exempt
def api_login(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return JsonResponse({"error": "Username and password required"}, status=400)

    user = authenticate(request, username=username, password=password)

    if user is None:
        return JsonResponse({"error": "Invalid credentials"}, status=401)

    login(request, user)
    return JsonResponse({"success": True, "message": "Login successful"})

@csrf_exempt
def api_register(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    email = data.get("email")
    username = data.get("username")
    password = data.get("password")
    confirm_password = data.get("confirm_password")

    if not username or not password:
        return JsonResponse({"error": "Username and password required"}, status=400)

    if password != confirm_password:
        return JsonResponse({"error": "Passwords do not match"}, status=400)

    if User.objects.filter(username=username).exists():
        return JsonResponse({"error": "Username already exists"}, status=400)

    if User.objects.filter(email=email).exists():
        return JsonResponse({"error": "Email already exists"}, status=400)

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
    )

    UserProfile.objects.create(
        user=user,
        first_name="",
        last_name="",
        description="",
        birth_day=None,
    )

    return JsonResponse({
        'success': True,
        'message': 'User created',
        'user_id': user.id,
    })


def api_data_user(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Unauthorized"}, status=401)

    user = request.user

    spotify_connect = UserConnection.objects.filter(
        user = request.user,
        provider__iexact="SPOTIFY" or "spotify"
    ).exists()

    telegram_connect = UserConnection.objects.filter(
        user=request.user,
        provider__iexact="TELEGRAM" or "telegram"
    ).exists()

    return JsonResponse({
        "username": user.username,
        "first_name": user.profile.first_name,
        "last_name": user.profile.last_name,
        "description": user.profile.description,
        "birth_day": user.profile.birth_day.isoformat() if user.profile.birth_day else "",
        "spotify_link": spotify_connect,
        "telegram_link": telegram_connect,
    })

def api_edit_profile(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    user = request.user

    username = data.get("username")
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    birth_day = data.get("birth_day")
    description = data.get("description")

    if username is not None:
        user.username = username.strip()

    if first_name is not None:
        user.profile.first_name = first_name.strip()

    if last_name is not None:
        user.profile.last_name = last_name.strip()

    if description is not None:
        user.profile.description = description.strip()

    if birth_day is not None:
        try:
            user.profile.birth_day = datetime.datetime.strptime(birth_day, "%Y-%m-%d").date()
        except ValueError:
            return JsonResponse({"error": "Invalid date format. Use YYYY-MM-DD"}, status=400)

    user.profile.save()
    user.save()

    return JsonResponse({
        "message": "User data updated successfully",
    })


def api_logout(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    logout(request)
    return JsonResponse({"message": "Logged out successfully"})