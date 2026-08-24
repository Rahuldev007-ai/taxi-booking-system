from django.shortcuts import render

# Create your views here.


def admin_users(request):
    return render(request, 'admin_pages/users.html')


def admin_create_user(request):
    return render(request,"admin_pages/user_forms.html")

def admin_edit_user(reqeust,user_id):
    return render(reqeust,"admin_pages/user_forms.html")

def admin_delete_user(request,user_id):
    return render(request, 'admin_pages/user_confirm_delete.html')

def admin_user_detail(request,user_id):
    return render(request, 'admin_pages/user_detail.html')