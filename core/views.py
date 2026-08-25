from django.shortcuts import render, redirect
from .models import AdminUser
import random
from django.contrib import messages

def admin_register(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip().lower()
        phone = request.POST.get('phone', '').strip()
        role = request.POST.get('role', 'SUPER_ADMIN')
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        form_data = {
            'full_name': full_name,
            'username': username,
            'email': email,
            'phone': phone,
            'role': role,
        }

        if not full_name or not username or not email or not password or not confirm_password:
            return render(request, 'admin_pages/register.html', {
                'error_message': 'All required fields must be filled out.',
                'form_data': form_data
            })

        if password != confirm_password:
            return render(request, 'admin_pages/register.html', {
                'error_message': 'Passwords do not match. Please try again.',
                'form_data': form_data
            })

        if len(password) < 6:
            return render(request, 'admin_pages/register.html', {
                'error_message': 'Password must be at least 6 characters long.',
                'form_data': form_data
            })

        if AdminUser.objects.filter(username__iexact=username).exists():
            return render(request, 'admin_pages/register.html', {
                'error_message': f'Username "{username}" is already registered.',
                'form_data': form_data
            })

        if AdminUser.objects.filter(email__iexact=email).exists():
            return render(request, 'admin_pages/register.html', {
                'error_message': f'Email address "{email}" is already in use.',
                'form_data': form_data
            })

        new_admin = AdminUser(
            full_name=full_name,
            username=username,
            email=email,
            phone=phone,
            role=role,
        )
        new_admin.set_password(password)
        new_admin.save()

        return render(request, 'admin_pages/login.html', {
            'success_message': f'Admin account for "{full_name}" registered successfully! Please sign in below.',
            'username': username
        })

    return render(request, 'admin_pages/register.html')


def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        if not username or not password:
            return render(request, 'admin_pages/login.html', {
                'error_message': 'Please enter both username and password.',
                'username': username
            })

        admin_user = AdminUser.objects.filter(username__iexact=username, is_active=True).first()

        if admin_user and admin_user.check_password(password):
            request.session['admin_user_id'] = admin_user.id
            request.session['admin_username'] = admin_user.username
            request.session['admin_full_name'] = admin_user.full_name
            request.session['admin_role'] = admin_user.role

            messages.success(request,"login successfully..")
            return redirect('admin_dashboard')
        else:
            return render(request, 'admin_pages/login.html', {
                'error_message': 'Invalid administrator credentials or inactive account.',
                'username': username
            })

    return render(request, 'admin_pages/login.html')


def admin_dashboard(request):
    return render(request,'admin_pages/dashboard.html')


def admin_logout(request):
    request.session.flush()
    return render(request, 'admin_pages/login.html', {
        'success_message': 'You have been logged out successfully.'
    })
    

def generate_otp():
    """Generate a 6-digit numeric OTP using the random library."""
    return f"{random.randint(0, 999999):06d}"

def admin_forgot_password(request):
    if request.method == 'POST':
            email = request.POST.get('email', '').strip().lower()
    
            if not email:
                return render(request, 'admin_pages/forgot_password.html', {
                    'error_message': 'Please enter a valid email address.',
                    'email': email
                })
    
            admin_user = AdminUser.objects.filter(email__iexact=email, is_active=True).first()
    
            if admin_user:
                otp_code = generate_otp()
                request.session['reset_otp'] = otp_code
                request.session['reset_email'] = email
                print("Generated OTP:", otp_code)
                return render(request, 'admin_pages/verify_otp.html', {
                    'success_message': f'Password reset instructions have been sent to "{email}". Please check your inbox.',
                    'email': email
                })
            else:
                return render(request, 'admin_pages/forgot_password.html', {
                    'error_message': f'No registered admin account found with email address "{email}".',
                    'email': email
                })
    
    return render(request, 'admin_pages/forgot_password.html')


def admin_verify_otp(request):
    reset_email = request.session.get('reset_email')
    expected_otp = request.session.get('reset_otp')

    if request.method == 'POST':
        otp_entered = request.POST.get('otp', '').strip()

        if not reset_email or not expected_otp:
            return render(request, 'admin_pages/forgot_password.html', {
                'error_message': 'Session expired. Please request a new password reset OTP.'
            })

        if otp_entered != expected_otp:
            return render(request, 'admin_pages/verify_otp.html', {
                'error_message': 'Invalid 6-digit OTP code.',
                'email': reset_email
            })

       
        request.session['otp_verified'] = True

        return render(request, 'admin_pages/reset_password.html', {
            'success_message': 'OTP Verified successfully! Please enter your new password below.',
            'email': reset_email
        })

    return render(request, 'admin_pages/verify_otp.html', {
        'email': reset_email
    })


def admin_reset_password(request):
    reset_email = request.session.get('reset_email')
    otp_verified = request.session.get('otp_verified')

    if not reset_email or not otp_verified:
        return render(request, 'admin_pages/forgot_password.html', {
            'error_message': 'Unauthorized reset request or session expired. Please request an OTP first.'
        })

    if request.method == 'POST':
        new_password = request.POST.get('new_password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if new_password != confirm_password:
            return render(request, 'admin_pages/reset_password.html', {
                'error_message': 'New passwords do not match. Please try again.',
                'email': reset_email
            })

        if len(new_password) < 6:
            return render(request, 'admin_pages/reset_password.html', {
                'error_message': 'Password must be at least 6 characters long.',
                'email': reset_email
            })

        admin_user = AdminUser.objects.filter(email__iexact=reset_email, is_active=True).first()

        if admin_user:
            admin_user.set_password(new_password)
            admin_user.save()

            # Clear reset session tokens
            request.session.pop('reset_email', None)
            request.session.pop('reset_otp', None)
            request.session.pop('otp_verified', None)

            return render(request, 'admin_pages/login.html', {
                'success_message': f'Password for "{admin_user.full_name}" reset successfully! Please sign in with your new password.',
                'username': admin_user.username
            })
        else:
            return render(request, 'admin_pages/forgot_password.html', {
                'error_message': 'Admin account not found. Please try again.'
            })

    return render(request, 'admin_pages/reset_password.html', {
        'email': reset_email
    })

def admin_drivers(request):
     return render(request, 'admin_pages/drivers.html')
 
def admin_bookings(request):
    return render(request, 'admin_pages/bookings.html')
