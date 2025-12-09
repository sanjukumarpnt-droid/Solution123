from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import StudentProfile
from datetime import datetime

User = get_user_model()


# ---------------- HOME PAGE ----------------
def home(request):
    return render(request, "home.html")



# ---------------- DASHBOARD ----------------
@login_required
def dashboard(request):
    return render(request, "dashboard.html")



# ---------------- SIGN-UP ----------------
def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        dob = request.POST['dob']
        gender = request.POST['gender']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        profile_image = request.FILES['profile_image']

        if password != confirm_password:
            return render(request, "signup.html", {"error": "Passwords do not match"})

        user = User.objects.create_user(username=username, email=email, password=password)

        StudentProfile.objects.create(
            user=user,
            dob=dob,
            gender=gender,
            profile_image=profile_image
        )

        login(request, user)
        return redirect("dashboard")  

    return render(request, "signup.html")


# ---------------- LOGIN ----------------
def user_login(request):
    if request.method == "POST":
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect("dashboard")
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})
    
    return render(request, "login.html")
def login_user(request):
    if request.method == "POST":

        username_or_email = request.POST.get("username")
        password = request.POST.get("password")

        # Try login with username
        user = authenticate(request, username=username_or_email, password=password)

        # If username login fails → try email login
        if user is None:
            try:
                user_email = User.objects.get(email=username_or_email)
                user = authenticate(request, username=user_email.username, password=password)
            except User.DoesNotExist:
                user = None

        if user is not None:
            login(request, user)
            return redirect("dashboard")   # ✅ FIXED HERE

        messages.error(request, "Invalid username/email or password!")
        return redirect("login")

    return render(request, "login.html")



# ---------------- LOGOUT ----------------
def logout_user(request):
    logout(request)
    return redirect("login")
def abcd():
    pass



# ---------------- FORGET PASSWORD ----------------
def forget_password(request):
    if request.method == "POST":

        email = request.POST.get("email")

        if not User.objects.filter(email=email).exists():
            messages.error(request, "Email is not registered!")
            return redirect("forget_password")

        messages.success(request, "Password reset link sent to your email!")
        return redirect("login")

    return render(request, "forget_password.html")
