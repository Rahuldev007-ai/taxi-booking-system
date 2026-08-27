from django.shortcuts import render
from admin_users.models import User
from django.db.models import Q

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
    return render(request,"pages/login.html")