from django.shortcuts import render,redirect,get_object_or_404
from admin_panel.models import ServiceCategoryDb
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.contrib import messages
from webapp.models import *
from webapp.models import Hospital
from django.contrib.auth.hashers import make_password




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
        messages.success(request, "Service Added Successfully")
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
        messages.success(request, "Service Updated Successfully")
        return redirect(display_service_category)

def delete_service_category(request,c_id):
    data=ServiceCategoryDb.objects.filter(id=c_id)
    data.delete()
    messages.success(request, "Service Deleted Successfully")
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
    messages.success(request, "Donor Deleted Successfully")
    return render(request,"Display_donors.html",{"donors":donors})

def delete_donors(request,d_id):
    data=DonorRegistrationDb.objects.filter(id=d_id)
    data.delete()
    return redirect('display_donors')

def display_messages(request):
    messages=ContactDb.objects.all()
    return render(request,"Display_messages.html",{"messages":messages})

def display_drivers(request):
    drivers=AmbulanceDriver.objects.all()
    return render(request,"Display_drivers.html",{"drivers":drivers})

def display_requests(request):
    requests=AmbulanceRequest.objects.all()
    return render(request,"Display_request.html",{"requests":requests})

def delete_drivers(request,d_id):
    data=AmbulanceDriver.objects.filter(id=d_id)
    data.delete()
    return redirect('display_drivers')

def delete_requests(request,r_id):
    data=AmbulanceRequest.objects.filter(id=r_id)
    data.delete()
    return redirect('display_requests')

def add_hospitals(request):
    return render(request,"Add_Hospitals.html")


def save_hospital(request):
    if request.method == "POST":
        name = request.POST.get('name')
        registration_number = request.POST.get('registration_number')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        district = request.POST.get('district')
        state = request.POST.get('state')
        is_verified = request.POST.get('is_verified') == 'on'
        image = request.FILES.get('image')

        obj = Hospital(
            name=name,
            registration_number=registration_number,
            phone=phone,
            email=email,
            address=address,
            city=city,
            district=district,
            state=state,
            is_verified=is_verified,
            image=image
        )
        obj.save()

        messages.success(request, "Hospital added successfully!")
        return redirect('add_hospitals')

    return redirect('add_hospitals')

def display_hospitals(request):
    hospitals = Hospital.objects.all()
    return render(request, 'Display_Hospitals.html', {'hospitals': hospitals})

def edit_hospitals(request, h_id):
    hospital = Hospital.objects.get(id=h_id)
    return render(request, "Edit_hospitals.html", {'hospital': hospital})


def update_hospital(request, h_id):
    if request.method == "POST":
        name = request.POST.get('name')
        registration_number = request.POST.get('registration_number')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        district = request.POST.get('district')
        state = request.POST.get('state')
        is_verified = request.POST.get('is_verified') == 'on'

        # Handle image upload
        try:
            img = request.FILES['image']
            fs = FileSystemStorage()
            file = fs.save(img.name, img)
        except MultiValueDictKeyError:
            # If no new image uploaded, keep the old one
            file = Hospital.objects.get(id=h_id).image

        # Update hospital using .update()
        Hospital.objects.filter(id=h_id).update(
            name=name,
            registration_number=registration_number,
            phone=phone,
            email=email,
            address=address,
            city=city,
            district=district,
            state=state,
            is_verified=is_verified,
            image=file
        )

        messages.success(request, "Hospital Updated Successfully")
        return redirect('display_hospitals')

def delete_hospital(request, h_id):
    hospital = Hospital.objects.get( id=h_id)
    hospital.delete()
    messages.success(request, "Hospital deleted successfully!")
    return redirect('display_hospitals')





def hospital_staff_signup_page(request):
    hospitals = Hospital.objects.all()
    return render(request, 'Hospitalstaff_signup.html', {
        'hospitals': hospitals
    })

def hospital_staff_signup(request):
    if request.method == "POST":
        hospital_id = request.POST.get('hospital')
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = make_password(request.POST.get('password'))

        HospitalStaff.objects.create(
            hospital_id=hospital_id,
            name=name,
            email=email,
            password=password,
            is_active=True
        )

        messages.success(request, "Hospital staff account created successfully")
        return redirect('hospital_staff_signup_page')


def staff_list(request):
    staff = HospitalStaff.objects.select_related('hospital').all()
    return render(request, 'Display_hospitalstaff.html', {'staff': staff})


def delete_staff(request, staff_id):
    staff = get_object_or_404(HospitalStaff, id=staff_id)
    staff.delete()
    return redirect('staff_list')

def bed_booking_list(request):
    bookings = BedBooking.objects.all()   # admin
    # bookings = BedBooking.objects.filter(hospital=request.user.hospital)  # for hospital
    return render(request, 'Bed_booking_list.html', {'bookings': bookings})


def delete_bed_booking(request, booking_id):
    booking = get_object_or_404(BedBooking, id=booking_id)
    booking.delete()
    return redirect('bed_booking_list')