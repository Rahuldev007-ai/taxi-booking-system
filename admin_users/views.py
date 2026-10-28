from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Driver, Taxi
from .forms import TaxiForm
from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse



def admin_users(request):
    users = User.objects.all()
    total_users = User.objects.count()
    search_query = request.GET.get('q')
    
    if search_query:
        search_name = User.objects.filter(
            Q(name__icontains = search_query)
            | Q(email__icontains = search_query)
        )
        total_users = search_name.count()
        context = {
            "users":search_name,
            "total_users":total_users,
            "search_query":search_query
        }
        return render(request, 'admin_pages/users.html',context)
        
    
    context = {
        "users":users,
        "total_users":total_users,
        "search_query":search_query
    }
    return render(request, 'admin_pages/users.html',context)

def admin_create_user(request):
    user_create = True 
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        
        exiting_user = User.objects.filter(
            Q(name=name) | Q(email=email) | Q(mobile=mobile)
        ).first()
        
        if exiting_user:
            if exiting_user.name == name:
                msg = "username alredy exit"
            elif exiting_user.email == email:
                msg = "Email already exit"
            elif len(password) < 6:
                msg = "Enter password of 6 charater"
            else:
                msg = "Mobie alreadt exit"
                
            return render(request,"admin_pages/user_forms.html",context={
                "error_message":msg,
                "typed_name":name,
                "typed_email":email,
                "typed_mobile":mobile
            }) 
        else:
            new_user = User.objects.create(
                name = name,
                email = email,
                mobile = mobile,
                is_active = True
            )
            new_user.set_password(password)
            new_user.save()
            if user_create:
                messages.success(request,"user create successfully")
                return redirect('admin_users')
            else:
                return render(request,"admin_pages/user_forms.html",context={
                                            "error_message":"Somthing went wrong"
                                        })
            
    context = {
        "user_create":user_create
    }
    return render(request,"admin_pages/user_forms.html",context)

def admin_edit_user(request,user_id):
    user_create = False
    user_obj = get_object_or_404(User, id=user_id)
    if request.method == "POST":  
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        is_active = request.POST.get('is_active') == 'on'
        
        exiting_user = User.objects.filter(
            (Q(name=name) | Q(email=email) | Q(mobile=mobile)) & ~Q(id=user_id)
        ).first()
        
        if exiting_user:
            if exiting_user.name == name:
                msg = "Username already exists."
            elif exiting_user.email == email:
                msg = "Email already exists."
            else:
                msg = "Mobile number already exists."
                
            return render(request, "admin_pages/user_forms.html", context={
                "error_message":msg,
                "user_create": False,
                "typed_name": name,
                "typed_email": email,
                "typed_mobile": mobile,
                "user_obj": user_obj,
                "user_create":user_create
            }) 
        try:
            user_obj.name = name
            user_obj.email = email
            user_obj.mobile = mobile
            user_obj.is_active = is_active
            
            if password and password.strip() != "":
                user_obj.set_password(password)
                
            user_obj.save()  
            
            messages.success(request, f"Account updates for '{name}' saved successfully!")
            return redirect('admin_users') 
        
        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")
            return render(request, "admin_pages/user_forms.html", context={
                "user_create": False,
                "typed_name": name,
                "typed_email": email,
                "typed_mobile": mobile,
                "user_obj": user_obj,
                "user_create":user_create
            })
            
    return render(request, "admin_pages/user_forms.html", context={
        "user_create": False,
        "typed_name": user_obj.name,
        "typed_email": user_obj.email,
        "typed_mobile": user_obj.mobile,
        "user_obj": user_obj,
        'user_create':user_create
    })

def admin_delete_user(request,user_id):
    user_obj = get_object_or_404(User, id=user_id)
    
    if request.method == "POST":
        deleted_name = user_obj.name
        
        user_obj.delete()
        
        messages.success(request, f"User account '{deleted_name}' has been successfully deleted.")
        return redirect('admin_users')
        
    return render(request, 'admin_pages/user_confirm_delete.html', {'user_obj': user_obj})

def admin_user_detail(request,user_id):
    user_obj = get_object_or_404(User, id=user_id)
    
    return render(request, 'admin_pages/user_detail.html', {
        'user_obj': user_obj
    })
    
def admin_drivers(request):
    Driver_details = Driver.objects.all()
    q = request.GET.get('q')
    total_count = Driver_details.count()
    
    if q:
        Driver_details = Driver.objects.filter(
            Q(name__icontains = q) |
            Q(email__icontains=q) |
            Q(mobile__icontains=q) |
            Q(license_number__icontains=q))
        total_count = Driver_details.count()
        
    context = {
        "driver":Driver_details,
        "search_query":q,
        "total":total_count,
    }
    return render(request, 'admin_pages/drivers.html',context)

def admin_driver_detail(request,driver_id):
    driver_obj = get_object_or_404(Driver,id = driver_id)
    context = {
        "driver_obj":driver_obj,
    }
    return render(request,"admin_pages/driver_detail.html",context)

def admin_delete_driver(request,driver_id):
    driver_obj = get_object_or_404(Driver,id = driver_id)
    if request.method == "POST":
        driver_obj.delete()
        messages.success(request,"Delete driver successfully..")
        return redirect('admin_drivers')
            
    context = {
        "driver_obj":driver_obj,
    }
    return render(request,"admin_pages/driver_confirm_delete.html",context)

def admin_create_driver(request):
    driver_create = True
    if request.method == "POST":
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        license_number = request.POST.get('license_number', '').strip().upper()
        mobile = request.POST.get('mobile', '').strip()
        vehicle_name = request.POST.get('vehicle_name', '').strip()
        status = request.POST.get('status', 'AVAILABLE').strip()
        password = request.POST.get('password', '').strip()

        form_context = {
            "driver_create": True,
            "admin_full_name": request.session.get('admin_full_name', 'Administrator'),
            "typed_name": name,
            "typed_email": email,
            "typed_license": license_number,
            "typed_mobile": mobile,
            "typed_vehicle": vehicle_name,
            "typed_status": status,
        }

        if not name or not email or not license_number or not mobile or not password:
            form_context["error_message"] = "All required fields must be filled out."
            return render(request, "admin_pages/driver_forms.html", form_context)

        if len(password) < 6:
            form_context["error_message"] = "Password must be at least 6 characters long."
            return render(request, "admin_pages/driver_forms.html", form_context)

        existing_driver = Driver.objects.filter(
            Q(email__iexact=email) | Q(license_number__iexact=license_number) | Q(mobile=mobile)
        ).first()

        if existing_driver:
            if existing_driver.email.lower() == email.lower():
                msg = f"Email '{email}' is already registered."
            elif existing_driver.license_number.upper() == license_number.upper():
                msg = f"License number '{license_number}' already exists."
            else:
                msg = f"Mobile number '{mobile}' already exists."

            form_context["error_message"] = msg
            return render(request, "admin_pages/driver_forms.html", form_context)

        new_driver = Driver.objects.create(
            name=name,
            email=email,
            license_number=license_number,
            mobile=mobile,
            vehicle_name=vehicle_name if vehicle_name else "Toyota Camry Hybrid",
            status=status,
            is_active=True
        )
        new_driver.set_password(password)
        new_driver.save()

        messages.success(request, f"Driver '{name}' registered successfully.")
        return redirect('admin_drivers')

    return render(request, "admin_pages/driver_forms.html", {
        "driver_create": True,
        "admin_full_name": request.session.get('admin_full_name', 'Administrator'),
    })

def admin_edit_driver(request, driver_id):
    driver_obj = get_object_or_404(Driver, id=driver_id)
    if request.method == "POST":
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        license_number = request.POST.get('license_number', '').strip().upper()
        mobile = request.POST.get('mobile', '').strip()
        vehicle_name = request.POST.get('vehicle_name', '').strip()
        status = request.POST.get('status', 'AVAILABLE').strip()
        password = request.POST.get('password', '').strip()
        is_active = request.POST.get('is_active') == 'on'

        form_context = {
            "driver_create": False,
            "admin_full_name": request.session.get('admin_full_name', 'Administrator'),
            "driver_obj": driver_obj,
            "typed_name": name,
            "typed_email": email,
            "typed_license": license_number,
            "typed_mobile": mobile,
            "typed_vehicle": vehicle_name,
            "typed_status": status,
        }

        if not name or not email or not license_number or not mobile:
            form_context["error_message"] = "Name, email, license number, and mobile are required."
            return render(request, "admin_pages/driver_forms.html", form_context)

        existing_driver = Driver.objects.filter(
            (Q(email__iexact=email) | Q(license_number__iexact=license_number) | Q(mobile=mobile)) & ~Q(id=driver_id)
        ).first()

        if existing_driver:
            if existing_driver.email.lower() == email.lower():
                msg = "Email already exists."
            elif existing_driver.license_number.upper() == license_number.upper():
                msg = "License number already exists."
            else:
                msg = "Mobile number already exists."

            form_context["error_message"] = msg
            return render(request, "admin_pages/driver_forms.html", form_context)

        driver_obj.name = name
        driver_obj.email = email
        driver_obj.license_number = license_number
        driver_obj.mobile = mobile
        if vehicle_name:
            driver_obj.vehicle_name = vehicle_name
        driver_obj.status = status
        driver_obj.is_active = is_active
        if password:
            if len(password) < 6:
                form_context["error_message"] = "Password must be at least 6 characters long."
                return render(request, "admin_pages/driver_forms.html", form_context)
            driver_obj.set_password(password)
        driver_obj.save()

        messages.success(request, f"Driver '{name}' updated successfully.")
        return redirect('admin_drivers')

    return render(request, "admin_pages/driver_forms.html", {
        "driver_create": False,
        "admin_full_name": request.session.get('admin_full_name', 'Administrator'),
        "driver_obj": driver_obj,
        "typed_name": driver_obj.name,
        "typed_email": driver_obj.email,
        "typed_license": driver_obj.license_number,
        "typed_mobile": driver_obj.mobile,
        "typed_vehicle": driver_obj.vehicle_name,
        "typed_status": driver_obj.status,
    })


def admin_taxis(request):
    if request.method == "POST" and request.POST.get('action') == 'toggle_availability':
        taxi_id = request.POST.get('taxi_id')
        taxi = get_object_or_404(Taxi, id=taxi_id)
        taxi.availability = not taxi.availability
        taxi.save()
        status_str = "Available" if taxi.availability else "Unavailable"

        is_ajax = (
            request.headers.get('x-requested-with') == 'XMLHttpRequest' or
            'application/json' in request.headers.get('Accept', '') or
            request.POST.get('is_ajax') == 'true'
        )
        if is_ajax:
            all_taxis = Taxi.objects.all()
            return JsonResponse({
                'success': True,
                'taxi_id': taxi.id,
                'taxi_number': taxi.number,
                'availability': taxi.availability,
                'status_label': status_str,
                'total_count': all_taxis.count(),
                'available_count': all_taxis.filter(availability=True).count(),
                'unavailable_count': all_taxis.filter(availability=False).count(),
                'message': f"Taxi '{taxi.number}' is now marked as {status_str}."
            })

        messages.success(request, f"Taxi '{taxi.number}' is now marked as {status_str}.")
        return redirect('admin_taxis')

    all_taxis = Taxi.objects.select_related('driver').all()

    total_fleet = all_taxis.count()
    available_count = all_taxis.filter(availability=True).count()
    unavailable_count = all_taxis.filter(availability=False).count()
    sedan_count = all_taxis.filter(type__iexact='SEDAN').count()
    suv_count = all_taxis.filter(type__iexact='SUV').count()
    hatchback_count = all_taxis.filter(type__iexact='HATCHBACK').count()
    premium_count = all_taxis.filter(type__iexact='PREMIUM').count()

    sources = sorted(list(set([s for s in all_taxis.values_list('source', flat=True) if s])))
    destinations = sorted(list(set([d for d in all_taxis.values_list('destination', flat=True) if d])))

    taxis = all_taxis.order_by('-created_at')

    q = request.GET.get('q', '').strip()
    taxi_number = request.GET.get('taxi_number', '').strip()
    source = request.GET.get('source', '').strip()
    destination = request.GET.get('destination', '').strip()
    filter_status = request.GET.get('status', '').strip().lower()
    filter_type = request.GET.get('type', '').strip().upper()

    if q:
        taxis = taxis.filter(
            Q(number__icontains=q) |
            Q(source__icontains=q) |
            Q(destination__icontains=q) |
            Q(type__icontains=q) |
            Q(driver__name__icontains=q) |
            Q(driver__email__icontains=q)
        )
    if taxi_number:
        taxis = taxis.filter(number__icontains=taxi_number)
    if source:
        taxis = taxis.filter(source__icontains=source)
    if destination:
        taxis = taxis.filter(destination__icontains=destination)
    if filter_status == 'available':
        taxis = taxis.filter(availability=True)
    elif filter_status == 'unavailable':
        taxis = taxis.filter(availability=False)
    if filter_type in ['SEDAN', 'SUV', 'HATCHBACK', 'PREMIUM']:
        taxis = taxis.filter(type__iexact=filter_type)

    is_filtered = bool(q or taxi_number or source or destination or filter_status or filter_type)
    total_count = taxis.count()

    context = {
        "taxis": taxis,
        "search_query": q,
        "taxi_number": taxi_number,
        "source": source,
        "destination": destination,
        "filter_status": filter_status,
        "filter_type": filter_type,
        "is_filtered": is_filtered,
        "total": total_fleet,
        "filtered_total": total_count,
        "available_count": available_count,
        "unavailable_count": unavailable_count,
        "sedan_count": sedan_count,
        "suv_count": suv_count,
        "hatchback_count": hatchback_count,
        "premium_count": premium_count,
        "sources": sources,
        "destinations": destinations,
        "admin_full_name": request.session.get('admin_full_name', 'Administrator'),
    }
    return render(request, 'admin_pages/taxis.html', context)

def admin_taxi_detail(request, taxi_id):
    taxi_obj = get_object_or_404(Taxi.objects.select_related('driver'), id=taxi_id)
    return render(request, 'admin_pages/taxi_detail.html', {
        'taxi_obj': taxi_obj,
        'admin_full_name': request.session.get('admin_full_name', 'Administrator'),
    })


def admin_create_taxi(request):
    taxi_create = True
    drivers = Driver.objects.all().order_by('name')

    if request.method == "POST":
        form = TaxiForm(request.POST)
        if form.is_valid():
            taxi_obj = form.save()
            messages.success(request, f"Taxi '{taxi_obj.number}' created and added to fleet successfully.")
            return redirect('admin_taxis')
        else:
            return render(request, "admin_pages/taxi_forms.html", {
                "taxi_create": taxi_create,
                "form": form,
                "drivers": drivers,
                "admin_full_name": request.session.get('admin_full_name', 'Administrator'),
            })

    form = TaxiForm()
    return render(request, "admin_pages/taxi_forms.html", {
        "taxi_create": taxi_create,
        "form": form,
        "drivers": drivers,
        "admin_full_name": request.session.get('admin_full_name', 'Administrator'),
    })


def admin_edit_taxi(request, taxi_id):
    taxi_obj = get_object_or_404(Taxi, id=taxi_id)
    taxi_create = False
    drivers = Driver.objects.all().order_by('name')

    if request.method == "POST":
        form = TaxiForm(request.POST, instance=taxi_obj)
        if form.is_valid():
            taxi_obj = form.save()
            messages.success(request, f"Taxi '{taxi_obj.number}' updated successfully.")
            return redirect('admin_taxis')
        else:
            return render(request, "admin_pages/taxi_forms.html", {
                "taxi_create": taxi_create,
                "taxi_obj": taxi_obj,
                "form": form,
                "drivers": drivers,
                "admin_full_name": request.session.get('admin_full_name', 'Administrator'),
            })

    form = TaxiForm(instance=taxi_obj)
    return render(request, "admin_pages/taxi_forms.html", {
        "taxi_create": taxi_create,
        "taxi_obj": taxi_obj,
        "form": form,
        "drivers": drivers,
        "admin_full_name": request.session.get('admin_full_name', 'Administrator'),
    })


def admin_delete_taxi(request, taxi_id):
    taxi_obj = get_object_or_404(Taxi, id=taxi_id)
    if request.method == "POST":
        taxi_number = taxi_obj.number
        taxi_obj.delete()
        messages.success(request, f"Taxi '{taxi_number}' deleted successfully.")
        return redirect('admin_taxis')

    return render(request, "admin_pages/taxi_confirm_delete.html", {
        "taxi_obj": taxi_obj,
        "admin_full_name": request.session.get('admin_full_name', 'Administrator'),
    })
