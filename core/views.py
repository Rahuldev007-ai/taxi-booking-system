from django.shortcuts import render,redirect


# Create your views here.
def admin_login(request):
    return render(request,'pages/login.html')