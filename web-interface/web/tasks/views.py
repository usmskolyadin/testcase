from django.shortcuts import render


def dashboard(request):
    return render(request, "tasks/dashboard.html")

def register(request):
    return render(request, "tasks/register.html")

def login(request):
    return render(request, "tasks/login.html")