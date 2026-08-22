from django.shortcuts import render, redirect
from .models import AdminUser
import random
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
                print("Generated OTP:", otp_code)
                request.session['reset_otp'] = random.randint(100000, 999999)
                return render(request, 'admin_pages/forgot_password.html', {
                    'success_message': f'Password reset instructions have been sent to "{email}". Please check your inbox.',
                    'email': email
                })
            else:
                return render(request, 'admin_pages/forgot_password.html', {
                    'error_message': f'No registered admin account found with email address "{email}".',
                    'email': email
                })
    
    return render(request, 'admin_pages/forgot_password.html')

