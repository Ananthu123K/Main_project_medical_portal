from django.shortcuts import render,redirect
from admin_panel.models import ServiceCategoryDb
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from webapp.models import DonorRegistrationDb


# Create your views here.

def index_page(request):
    categories_count=ServiceCategoryDb.objects.count()
    return render(request,"index.html",{"categories_count":categories_count})
def add_service_category(request):
    return render(request,"Add_service_category.html")
def save_category(request):
    if request.method=="POST":
        service_name=request.POST.get('name')
        service_description=request.POST.get('description')
        service_image=request.FILES['image']

        obj=ServiceCategoryDb(
            name=service_name,
            description=service_description,
            image=service_image

        )
        obj.save()
        return redirect(add_service_category)

def display_service_category(request):
    categories=ServiceCategoryDb.objects.all()
    return render(request,"Display_service_category.html",{"categories":categories})

def edit_service_category(request,c_id):
    categories=ServiceCategoryDb.objects.get(id=c_id)
    return render(request,"Edit_service_category.html",{"categories":categories})

def update_service_category(request,c_id):
    if request.method == "POST":
        service_name = request.POST.get('name')
        service_description = request.POST.get('description')
        try:
            img= request.FILES['image']
            fs = FileSystemStorage()
            file = fs.save(img.name, img)
        except MultiValueDictKeyError:
            file = ServiceCategoryDb.objects.get(id=c_id).image
        ServiceCategoryDb.objects.filter(id=c_id).update(
            name=service_name,
            description=service_description,
            image=file

        )
        return redirect(display_service_category)

def delete_service_category(request,c_id):
    data=ServiceCategoryDb.objects.filter(id=c_id)
    data.delete()
    return redirect(display_service_category)


# admin login

def admin_login_page(request):
    return render(request,"Admin_login.html")

def admin_login(request):
    if request.method=="POST":
        un=request.POST.get('username')
        pswd=request.POST.get('password')
        if User.objects.filter(username__contains=un).exists():
            data=authenticate(username=un,password=pswd)
            if data is not None:
                login(request,data)
                #session setting
                request.session['username']=un
                request.session['password']=pswd
                return redirect(index_page)
            else:
                return redirect(admin_login_page)
        else:
            return redirect(admin_login_page)

def admin_logout(request):
    del request.session['username']
    del request.session['password']
    return redirect(admin_login_page)

#to display all Donors

def display_donors(request):
    donors=DonorRegistrationDb.objects.all()
    return render(request,"Display_donors.html",{"donors":donors})

def delete_donors(request,d_id):
    data=DonorRegistrationDb.objects.filter(id=d_id)
    data.delete()

