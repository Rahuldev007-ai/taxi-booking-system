from django.shortcuts import render, redirect
from .models import AdminUser

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
            return render(request, 'pages/register.html', {
                'error_message': 'All required fields must be filled out.',
                'form_data': form_data
            })

        if password != confirm_password:
            return render(request, 'pages/register.html', {
                'error_message': 'Passwords do not match. Please try again.',
                'form_data': form_data
            })

        if len(password) < 6:
            return render(request, 'pages/register.html', {
                'error_message': 'Password must be at least 6 characters long.',
                'form_data': form_data
            })

        if AdminUser.objects.filter(username__iexact=username).exists():
            return render(request, 'pages/register.html', {
                'error_message': f'Username "{username}" is already registered.',
                'form_data': form_data
            })

        if AdminUser.objects.filter(email__iexact=email).exists():
            return render(request, 'pages/register.html', {
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

        return render(request, 'pages/login.html', {
            'success_message': f'Admin account for "{full_name}" registered successfully! Please sign in below.',
            'username': username
        })

    return render(request, 'pages/register.html')


def admin_login(request):
   
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        if not username or not password:
            return render(request, 'pages/login.html', {
                'error_message': 'Please enter both username and password.',
                'username': username
            })

        admin_user = AdminUser.objects.filter(username__iexact=username, is_active=True).first()

        if admin_user and admin_user.check_password(password):
            request.session['admin_user_id'] = admin_user.id
            request.session['admin_username'] = admin_user.username
            request.session['admin_full_name'] = admin_user.full_name
            request.session['admin_role'] = admin_user.role

            return render(request, 'pages/dashboard.html', {
                'admin_user': admin_user
            })
        else:
            return render(request, 'pages/login.html', {
                'error_message': 'Invalid administrator credentials or inactive account.',
                'username': username
            })

    return render(request, 'pages/login.html')


def admin_logout(request):
    request.session.flush()
    return render(request, 'pages/login.html', {
        'success_message': 'You have been logged out successfully.'
    })
