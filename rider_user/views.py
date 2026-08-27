from django.shortcuts import render,redirect
from admin_users.models import User
from django.db.models import Q
from django.contrib import messages
# from django.contrib.auth.hashers import check_password

def user_register(request):
    if request.method == "POST":
        name = request. POST.get('name').strip()
        email = request.POST.get('email').strip()
        phone = request.POST.get('phone').strip()
        pws = request.POST.get("password").strip()
        cpws = request.POST.get('confirm_password').strip()
        
        form_data = {
            "name":name,
            "email":email,
            "phone":phone
        }
        
        if not name or not email or not phone or not pws or not cpws:
            return render(request,"pages/register.html",{
                'error_message':"All required fields must be filled out.",
                "form_data":form_data
            })
            
        if pws != cpws:
            return render(request, 'pages/register.html', {
                'error_message': 'Passwords do not match. Please try again.',
                'form_data': form_data
            })
            
        if len(pws) < 6:
            return render(request, 'pages/register.html', {
                'error_message': 'Password must be at least 6 characters long.',
                'form_data': form_data
            })
        
        if User.objects.filter(name__iexact=name).exists():
            error_message = f'Username "{name}" is already registered.'
        elif User.objects.filter(email__iexact=email).exists():
            error_message = f'Email "{email}" is already registered.'
        elif User.objects.filter(mobile=phone).exists():
            error_message = f'Phone number "{phone}" is already registered.'
        else:
            error_message = None

        if error_message:
            return render(request, 'pages/register.html', {
                'error_message': error_message,
                'form_data': form_data
            })  
            
        new_user = User.objects.create(
            name = name,
            email = email,
            mobile = phone
        ) 
        new_user.set_password(pws)
        new_user.save()
        return render(request, 'pages/register.html', {
            'success_message': f'Account for "{name}" registered successfully! You can now log in.'
        })
        
        
    return render(request,'pages/register.html')

def user_login(request):
    context = {}
    
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        context['email'] = email
        
        if not email or not password:
            context['error_message'] = "Please enter both username and password."
            return render(request,"pages/login.html",context)
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            context['error_message'] = "Email not found."
            return render(request, "pages/login.html", context)
        
        if user.check_password(password):
            if email and password:
                request.session["user_id"] = user.id
                request.session["user_name"] = user.name
                
                messages.success(request,"Login successfully..")
                return redirect('user-dashboard')
        else:
            context['error_message'] = "Incorrect password. Please try again."
            return render(request, "pages/login.html", context)
        
    return render(request,"pages/login.html",context)

def user_logout(request):
    request.session.pop("user_id", None)
    messages.success(request, "Logged out successfully.")
    context={
        "success_message":"Logout successfully.."
    }
    return render(request,"pages/login.html",context)

from django.shortcuts import render, redirect

def user_dashboard(request):
    if not request.session.get("user_id"):
        return render(request, "pages/login.html", {
            "error_message": "Unauthorized access. Please sign in.",
        })
    
    
    return render(request, "pages/dashboard.html")
