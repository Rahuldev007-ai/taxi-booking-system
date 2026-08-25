from django.shortcuts import render,redirect,get_object_or_404
from .models import User,Driver
from django.db.models import Q
from django.contrib import messages



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
    
# Driver view 
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
    
 