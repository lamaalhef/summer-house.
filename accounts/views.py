from django.shortcuts import render


def register_view(request):
    return render(request, "accounts/register.html")


def login_view(request):
    return render(request, "accounts/login.html")


def profile_view(request):
    return render(request, "accounts/profile.html")