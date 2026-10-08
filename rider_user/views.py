from django.shortcuts import render, redirect, get_object_or_404
from admin_users.models import User, Driver
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
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        
        context['email'] = email
        
        if not email or not password:
            context['error_message'] = "Please enter both email and password."
            return render(request,"pages/login.html",context)
        
        user_obj = User.objects.filter(email__iexact=email).first()
        driver_obj = None
        if not user_obj:
            driver_obj = Driver.objects.filter(email__iexact=email).first()
        
        account = user_obj or driver_obj
        if not account:
            context['error_message'] = "Email not found."
            return render(request, "pages/login.html", context)
        
        if account.check_password(password):
            request.session["user_id"] = account.id
            request.session["user_name"] = account.name
            request.session["user_email"] = account.email
            request.session["is_driver"] = bool(driver_obj)
            
            messages.success(request, f"Welcome back, {account.name}! Login successful.")
            if driver_obj:
                return redirect('driver-dashboard')
            return redirect('user-dashboard')
        else:
            context['error_message'] = "Incorrect password. Please try again."
            return render(request, "pages/login.html", context)
        
    return render(request,"pages/login.html",context)

def user_logout(request):
    request.session.pop("user_id", None)
    request.session.pop("user_name", None)
    request.session.pop("user_email", None)
    request.session.pop("is_driver", None)
    messages.success(request, "Logged out successfully.")
    context={
        "success_message":"Logout successfully.."
    }
    return render(request,"pages/login.html",context)

def user_dashboard(request):
    if not request.session.get("user_id"):
        return render(request, "pages/login.html", {
            "error_message": "Unauthorized access. Please sign in.",
        })
    
    if request.session.get("is_driver"):
        return redirect('driver-dashboard')
    
    return render(request, "pages/dashboard.html")

def driver_dashboard(request):
    if not request.session.get("user_id") or not request.session.get("is_driver"):
        return render(request, "pages/login.html", {
            "error_message": "Unauthorized access. Driver sign in required.",
        })
    
    driver_obj = get_object_or_404(Driver, id=request.session["user_id"])
    
    if request.method == "POST":
        new_status = request.POST.get("status", "").strip()
        if new_status in ['AVAILABLE', 'ON_TRIP', 'OFFLINE']:
            driver_obj.status = new_status
            driver_obj.save()
            messages.success(request, f"Duty status updated to {driver_obj.get_status_display()}.")
            return redirect('driver-dashboard')
            
    return render(request, "pages/driver_dashboard.html", {
        "driver_obj": driver_obj
    })

def driver_profile(request):
    if not request.session.get("user_id") or not request.session.get("is_driver"):
        return render(request, "pages/login.html", {
            "error_message": "Unauthorized access. Driver sign in required.",
        })
    
    driver_obj = get_object_or_404(Driver, id=request.session["user_id"])
    
    return render(request, "pages/driver_profile.html", {
        "driver_obj": driver_obj
    })

def driver_login(request):
    if request.session.get("user_id") and request.session.get("is_driver"):
        return redirect('driver-dashboard')
        
    context = {}
    
    if request.method == "POST":
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        
        context['email'] = email
        
        if not email or not password:
            context['error_message'] = "Please enter both email and password."
            return render(request, "pages/driver_login.html", context)
        
        driver_obj = Driver.objects.filter(email__iexact=email).first()
        
        if not driver_obj:
            context['error_message'] = "No driver account found with this email."
            return render(request, "pages/driver_login.html", context)
            
        if not driver_obj.is_active:
            context['error_message'] = "Your driver account is inactive. Please contact system administrator."
            return render(request, "pages/driver_login.html", context)
        
        if driver_obj.check_password(password):
            request.session["user_id"] = driver_obj.id
            request.session["driver_id"] = driver_obj.id
            request.session["user_name"] = driver_obj.name
            request.session["user_email"] = driver_obj.email
            request.session["is_driver"] = True
            
            messages.success(request, f"Welcome back, {driver_obj.name}! Driver login successful.")
            return redirect('driver-dashboard')
        else:
            context['error_message'] = "Incorrect password. Please try again."
            return render(request, "pages/driver_login.html", context)
            
    return render(request, "pages/driver_login.html", context)

def driver_register(request):
    if request.method == "POST":
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        license_number = request.POST.get('license_number', '').strip().upper()
        phone = request.POST.get('phone', '').strip()
        pws = request.POST.get("password", "").strip()
        cpws = request.POST.get('confirm_password', "").strip()
        vehicle_name = request.POST.get('vehicle_name', '').strip()

        form_data = {
            "name": name,
            "email": email,
            "license_number": license_number,
            "phone": phone,
            "vehicle_name": vehicle_name,
        }

        if not name or not email or not license_number or not phone or not pws or not cpws:
            return render(request, "pages/driver_register.html", {
                'error_message': "All required fields must be filled out.",
                "form_data": form_data
            })

        if pws != cpws:
            return render(request, 'pages/driver_register.html', {
                'error_message': 'Passwords do not match. Please try again.',
                'form_data': form_data
            })

        if len(pws) < 6:
            return render(request, 'pages/driver_register.html', {
                'error_message': 'Password must be at least 6 characters long.',
                'form_data': form_data
            })

        if Driver.objects.filter(email__iexact=email).exists():
            error_message = f'Email "{email}" is already registered with a driver account.'
        elif Driver.objects.filter(license_number__iexact=license_number).exists():
            error_message = f'License number "{license_number}" is already registered.'
        elif Driver.objects.filter(mobile=phone).exists():
            error_message = f'Phone number "{phone}" is already registered.'
        else:
            error_message = None

        if error_message:
            return render(request, 'pages/driver_register.html', {
                'error_message': error_message,
                'form_data': form_data
            })

        new_driver = Driver.objects.create(
            name=name,
            email=email,
            license_number=license_number,
            mobile=phone,
            vehicle_name=vehicle_name if vehicle_name else "Toyota Camry Hybrid",
            status="AVAILABLE",
            is_active=True
        )
        new_driver.set_password(pws)
        new_driver.save()

        return render(request, 'pages/driver_register.html', {
            'success_message': f'Driver account for "{name}" registered successfully! You can now join our active fleet.'
        })

    return render(request, 'pages/driver_register.html')

import random

def generate_user_otp():
    """Generate a 6-digit numeric OTP code."""
    return f"{random.randint(0, 999999):06d}"

def user_forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()

        if not email:
            return render(request, 'pages/forgot_password.html', {
                'error_message': 'Please enter a valid email address.',
                'email': email
            })

        user = User.objects.filter(email__iexact=email, is_active=True).first()
        if not user:
            user = Driver.objects.filter(email__iexact=email, is_active=True).first()

        if user:
            otp_code = generate_user_otp()
            request.session['user_reset_otp'] = otp_code
            request.session['user_reset_email'] = email
            print("Generated User Reset OTP:", otp_code)
            return render(request, 'pages/verify_otp.html', {
                'success_message': f'Password reset OTP code generated for "{email}". Please verify below.',
                'email': email
            })
        else:
            return render(request, 'pages/forgot_password.html', {
                'error_message': f'No registered account found with email address "{email}".',
                'email': email
            })

    return render(request, 'pages/forgot_password.html')

def user_verify_otp(request):
    reset_email = request.session.get('user_reset_email')
    expected_otp = request.session.get('user_reset_otp')

    if request.method == 'POST':
        otp_entered = request.POST.get('otp', '').strip()

        if not reset_email or not expected_otp:
            return render(request, 'pages/forgot_password.html', {
                'error_message': 'Session expired. Please request a new password reset OTP.'
            })

        if not otp_entered or len(otp_entered) != 6 or not otp_entered.isdigit():
            return render(request, 'pages/verify_otp.html', {
                'error_message': 'Please enter a valid 6-digit numeric OTP code.',
                'email': reset_email
            })

        if otp_entered != expected_otp:
            return render(request, 'pages/verify_otp.html', {
                'error_message': 'Invalid 6-digit OTP code. Please check and try again.',
                'email': reset_email
            })

        request.session['user_otp_verified'] = True

        return render(request, 'pages/reset_password.html', {
            'success_message': 'OTP verified successfully! Please enter your new password below.',
            'email': reset_email
        })

    return render(request, 'pages/verify_otp.html', {
        'email': reset_email
    })

def user_reset_password(request):
    reset_email = request.session.get('user_reset_email')
    otp_verified = request.session.get('user_otp_verified')

    if not reset_email or not otp_verified:
        return render(request, 'pages/forgot_password.html', {
            'error_message': 'Unauthorized request or session expired. Please verify OTP first.'
        })

    if request.method == 'POST':
        new_password = request.POST.get('new_password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()

        if not new_password or not confirm_password:
            return render(request, 'pages/reset_password.html', {
                'error_message': 'Please fill out both password fields.',
                'email': reset_email
            })

        if len(new_password) < 6:
            return render(request, 'pages/reset_password.html', {
                'error_message': 'Password must be at least 6 characters long.',
                'email': reset_email
            })

        if new_password != confirm_password:
            return render(request, 'pages/reset_password.html', {
                'error_message': 'New passwords do not match. Please try again.',
                'email': reset_email
            })

        user = User.objects.filter(email__iexact=reset_email, is_active=True).first()
        if not user:
            user = Driver.objects.filter(email__iexact=reset_email, is_active=True).first()

        if user:
            user.set_password(new_password)
            user.save()

            request.session.pop('user_reset_email', None)
            request.session.pop('user_reset_otp', None)
            request.session.pop('user_otp_verified', None)

            return render(request, 'pages/login.html', {
                'success_message': f'Password for "{user.name}" reset successfully! Please log in with your new password.',
                'email': user.email
            })
        else:
            return render(request, 'pages/forgot_password.html', {
                'error_message': 'Account not found. Please try again.'
            })

    return render(request, 'pages/reset_password.html', {
        'email': reset_email
    })


