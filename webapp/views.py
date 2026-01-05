from django.shortcuts import render,redirect
from django.utils.datastructures import MultiValueDictKeyError
from admin_panel.models import ServiceCategoryDb,BloodCategory
from webapp.models import *
from django.contrib.auth.hashers import make_password    #for hashing and reset
from django.contrib.auth.hashers import check_password
from datetime import date, timedelta
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from twilio.rest import Client
from django.conf import settings
from django.http import HttpResponse
from .utils import is_strong_password
import uuid
from django.utils import timezone
from django.db import transaction
from django.db.models import Sum







#for email  sms and profile notifications

from .models import BloodRequest, UserRegistration
from datetime import datetime


from .models import DonorNotification, DonorRegistrationDb



# Create your views here.

def home_page(request):
    services=ServiceCategoryDb.objects.all()
    return render(request,"Home.html",{"services":services})
def service_page(request):
    services=ServiceCategoryDb.objects.all()
    return render(request,"Services.html",{"services":services})
def donors_page(request):
    services = ServiceCategoryDb.objects.all()
    donors=DonorRegistrationDb.objects.all()
    locations = DonorRegistrationDb.objects.values_list("Location", flat=True).distinct()
    # Get unique blood groups
    blood_groups = DonorRegistrationDb.objects.values_list("BloodGroup", flat=True).distinct()
    return render(request,"Donors.html",{"services":services,"donors":donors,"locations":locations,"blood_groups":blood_groups})
def contact_page(request):
    services = ServiceCategoryDb.objects.all()
    return render(request,"Contact.html",{'services':services})
def about_page(request):
    services = ServiceCategoryDb.objects.all()
    return render(request,"About.html",{'services':services})
def signup_page(request):
    return render(request,"Signup_page.html")
def signin_page(request):
    return render(request,"Signin_page.html")
def service_detail(request, service_id):
    services = ServiceCategoryDb.objects.all()
    service = ServiceCategoryDb.objects.filter(id=service_id).first()

    return render(request, 'Service_detail.html', {'services':services,
        'service': service
    })




def user_signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # PASSWORD STRENGTH CHECK
        valid, error = is_strong_password(password)
        if not valid:
            messages.error(request, error)
            return redirect('signup_page')

        # Email already exists
        if UserRegistration.objects.filter(Email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('signup_page')

        # Name already exists
        if UserRegistration.objects.filter(Name=name).exists():
            messages.error(request, "Name already exists")
            return redirect('signup_page')

        # Password mismatch
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('signup_page')

        # HASH PASSWORD
        hashed_password = make_password(password)

        user = UserRegistration(
            Name=name,
            Email=email,
            Phone=phone,
            Password=hashed_password,
            Confirm_password=hashed_password,
        )
        user.save()

        messages.success(request, "Registration successful. Please login.")
        return redirect('signin_page')

    return redirect('signup_page')








def user_login(request):
    if request.method == 'POST':
        un = request.POST.get('username')
        pswd = request.POST.get('password')

        try:
            user = UserRegistration.objects.get(Name=un)
        except UserRegistration.DoesNotExist:
            messages.error(request, "Invalid username or password")
            return redirect('signin_page')

        # CHECK HASHED PASSWORD
        if check_password(pswd, user.Password):

            # Create session
            request.session['user_id'] = user.id
            request.session['Name'] = user.Name

            return redirect('Home')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('signin_page')

    return redirect('signin_page')


def user_logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    if 'Name' in request.session:
        del request.session['Name']

    return redirect('signin_page')




# -----------------------------
# Blood donation View
# -----------------------------


#Donor registration and login


def donor_signup_page(request):
    return render(request,"Donor_signup.html")

def donor_login_page(request):
    return render(request,"Donor_signin.html")





# Donor Signup

def donor_signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        blood_group = request.POST.get('bloodgroup')
        location = request.POST.get('location')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        image = request.FILES.get('image')

        #  Password match check
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect(request.META.get("HTTP_REFERER", "donor_signup"))

        #  Password strength check
        valid, error = is_strong_password(password)
        if not valid:
            messages.error(request, error)
            return redirect(request.META.get("HTTP_REFERER", "donor_signup"))

        # Email uniqueness check
        if DonorRegistrationDb.objects.filter(Email=email).exists():
            messages.error(request, "Email already exists")
            return redirect(request.META.get("HTTP_REFERER", "donor_signup"))

        # 4. Hash password
        hashed_password = make_password(password)

        # 5. Save donor
        donor = DonorRegistrationDb(
            Name=name,
            Email=email,
            phone=phone,
            BloodGroup=blood_group,
            Location=location,
            Password=hashed_password,
            Age=age,
            Gender=gender,
            Image=image,
            is_active=True
        )
        donor.save()

        messages.success(request, "Donor registered successfully! Please login.")
        return redirect('Home')

    return redirect('Home')




# Donor Login

def donor_login(request):
    if request.method == 'POST':
        email = request.POST.get('Email')  # Use Email instead of Name
        password = request.POST.get('Password')

        try:
            donor = DonorRegistrationDb.objects.get(Email=email)
        except DonorRegistrationDb.DoesNotExist:
            messages.error(request, "Invalid credentials")
            return redirect('donor_login_page')

        # Check hashed password
        if check_password(password, donor.Password):
            # Save session (ID and Name)
            request.session['donor_id'] = donor.id
            request.session['donor_name'] = donor.Name
            messages.success(request,"Login Successful")
            return redirect('donor_profile')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('Home')

    return redirect('donor_login_page')


# Donor Logout

def donor_logout(request):
    if 'donor_id' in request.session:
        del request.session['donor_id']
    if 'donor_name' in request.session:
        del request.session['donor_name']
    return redirect('donor_login')



def edit_donor_profile(request, donor_id):
    donor = DonorRegistrationDb.objects.get(id=donor_id)
    return render(request, "Edit_donor_profile.html", {"donor": donor})




def update_donor_profile(request, donor_id):
    if request.method == "POST":
        # Get form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        bloodgroup = request.POST.get('bloodgroup')
        location = request.POST.get('location')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        donor = DonorRegistrationDb.objects.get(id=donor_id)

        # Handle image upload

        try:
            img = request.FILES['image']  # may raise MultiValueDictKeyError
            fs = FileSystemStorage()
            file = fs.save(img.name, img)
        except MultiValueDictKeyError:
            # No new image uploaded, keep old image
            file=donor.Image


        # Handle password
        if password:
            if password == confirm_password:
                hashed_password = make_password(password)
            else:
                #  JS to show "Passwords do not match"
                return redirect('edit_donor_profile', donor_id=donor_id)
        else:
            hashed_password = donor.Password  # keep old password

        # Update donor record
        DonorRegistrationDb.objects.filter(id=donor_id).update(
            Name=name,
            Email=email,
            phone=phone,
            BloodGroup=bloodgroup,
            Location=location,
            Age=age,
            Gender=gender,
            Image=file,
            Password=hashed_password
        )

        #  Use JS to show "Profile updated successfully"
        return redirect('donor_profile')

    # If not POST, redirect to edit page
    return redirect('edit_donor_profile', donor_id=donor_id)








#Donor profile and active view code



COOLDOWN_DAYS = 90  # Cooldown period after donation (e.g., 90 days)

# -----------------------------
# Donor Profile
# -----------------------------
def donor_profile(request):
    donor_id = request.session.get('donor_id')
    if not donor_id:
        return redirect('donor_login_page')  # Ensure donor is logged in

    donor = DonorRegistrationDb.objects.get(id=donor_id)

    # -----------------------------
    # Check cooldown period
    # -----------------------------
    if donor.last_donation_date:
        cooldown_end = donor.last_donation_date + timedelta(days=COOLDOWN_DAYS)
        if date.today() < cooldown_end:
            donor.system_inactive = True
            donor.is_active = False  # enforce inactive
            days_left = (cooldown_end - date.today()).days
        else:
            donor.system_inactive = False
            days_left = 0
    else:
        donor.system_inactive = False
        days_left = 0

    donor.save()

    return render(request, 'Donor_profile.html', {
        'donor': donor,
        'days_left': days_left,

    })



# -----------------------------
# Toggle Active/Inactive (manual)
# Only allowed if not in cooldown
# -----------------------------
def toggle_donor_status(request):
    donor_id = request.session.get('donor_id')
    if donor_id:
        donor = DonorRegistrationDb.objects.get(id=donor_id)
        if not donor.system_inactive:
            donor.is_active = not donor.is_active
            donor.save()
    return redirect('donor_profile')


# -----------------------------
# Mark as Donated
# Sets last donation date and disables account for cooldown
# -----------------------------
def mark_donated(request):
    donor_id = request.session.get('donor_id')
    if not donor_id:
        return redirect('donor_login_page')

    donor = DonorRegistrationDb.objects.get(id=donor_id)

    # Only allow donation if ACTIVE
    if donor.is_active and not donor.system_inactive:
        donor.last_donation_date = date.today()
        donor.is_active = False
        donor.system_inactive = True

        # increase the lifesaving count by 1
        donor.life_saved = (donor.life_saved or 0) + 1

        donor.save()

    return redirect('donor_profile')


# filter donors based on location and blood group

def filtered_donors(request):
    services = ServiceCategoryDb.objects.all()
    location = request.GET.get("location")
    blood = request.GET.get("blood")

    donors = DonorRegistrationDb.objects.all()
    locations = DonorRegistrationDb.objects.values_list("Location", flat=True).distinct()


    # Get unique blood groups
    blood_groups = DonorRegistrationDb.objects.values_list("BloodGroup", flat=True).distinct()

    if location and location != "":
        donors = donors.filter(Location=location)

    if blood and blood != "":
        donors = donors.filter(BloodGroup=blood)


    return render(request, "Filter_donors.html", {
        "donors": donors,
        "location": location,
        "blood": blood,
        "locations":locations,
        "blood_groups":blood_groups,
        "services":services

    })


#save user messages
def save_contact(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        subject=request.POST.get('subject')
        message=request.POST.get('message')

        obj=ContactDb(User_name=name,User_email=email,Subject=subject,Message=message)
        obj.save()
        return redirect(contact_page)


#notifications sms/email and message in donor profile

def blood_request_form(request):
    return render(request,"Blood_request_form.html")


def blood_request_success(request):
    return render(request, "Blood_request_success.html")



def request_blood(request):
    if 'user_id' not in request.session:
        return redirect('signin_page')

    if request.method == "POST":
        user = get_object_or_404(UserRegistration, id=request.session['user_id'])

        br = BloodRequest.objects.create(
            requester=user,
            patient_name=request.POST.get('patient_name') or user.Name,
            blood_group=request.POST.get('blood_group'),
            units=int(request.POST.get('units') or 1),
            location=request.POST.get('location'),
            phone=request.POST.get('phone'),
            needed_date=request.POST.get('needed_date'),
            reason=request.POST.get('reason'),
        )

        #  FIND MATCHING DONORS
        donors = DonorRegistrationDb.objects.filter(
            BloodGroup__iexact=br.blood_group,
            Location__iexact=br.location,
            is_active=True
        )

        for donor in donors:
            # Create assignment
            BloodAssignment.objects.create(
                blood_request=br,
                donor=donor
            )

            # SEND EMAIL
            if donor.Email:
                subject = "🩸 Urgent Blood Donation Request"
                message = f"""
Dear {donor.Name},

A blood donation request matches your profile.

🩸 Blood Group: {br.blood_group}
📍 Location: {br.location}
📅 Needed Date: {br.needed_date}

Please log in to your donor dashboard to accept or reject the request.

Thank you for saving lives ❤️
LifeLink Health Portal
"""
                try:
                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        [donor.Email],
                        fail_silently=False
                    )
                except Exception as e:
                    print("Email error:", e)

        return redirect('blood_request_success')

    return redirect('blood_request_form')


def donor_notifications(request):
    if 'donor_id' not in request.session:
        return redirect('donor_login_page')

    donor = get_object_or_404(
        DonorRegistrationDb,
        id=request.session['donor_id'],
        is_active=True
    )

    assignments = BloodAssignment.objects.filter(
        donor=donor,
        status='waiting'
    ).select_related('blood_request')

    return render(request, "Donor_notification.html", {
        "assignments": assignments
    })





def accept_blood_request(request, request_id):
    donor = get_object_or_404(DonorRegistrationDb, id=request.session['donor_id'])
    blood_request = get_object_or_404(BloodRequest, id=request_id)

    assignment = BloodAssignment.objects.get(
        donor=donor,
        blood_request=blood_request
    )

    assignment.status = 'accepted'
    assignment.responded_at = timezone.now()
    assignment.save()

    blood_request.is_fulfilled = True
    blood_request.save()

    # Reject others
    BloodAssignment.objects.filter(
        blood_request=blood_request
    ).exclude(donor=donor).update(status='rejected')

    # Remove notifications
    DonorNotification.objects.filter(blood_request=blood_request).delete()

    donor.life_saved += 1
    donor.save()

    #  Email to requester
    send_mail(
        "🩸 Blood Request Accepted",
        f"""
Dear {blood_request.requester.Name},

Your blood request has been ACCEPTED.

Donor Name: {donor.Name}
Blood Group: {donor.BloodGroup}
Phone: {donor.phone}

Please contact immediately.

LifeLink Health Portal
""",
        settings.DEFAULT_FROM_EMAIL,
        [blood_request.requester.Email],
        fail_silently=True
    )

    messages.success(request, "You have accepted the request")
    return redirect('donor_notifications')






def reject_blood_request(request, request_id):
    donor = get_object_or_404(DonorRegistrationDb, id=request.session['donor_id'])
    blood_request = get_object_or_404(BloodRequest, id=request_id)

    assignment = BloodAssignment.objects.get(
        donor=donor,
        blood_request=blood_request
    )

    assignment.status = 'rejected'
    assignment.responded_at = timezone.now()
    assignment.save()

    DonorNotification.objects.filter(
        donor=donor,
        blood_request=blood_request
    ).delete()

    messages.info(request, "You rejected the request")
    return redirect('donor_notifications')











# -----------------------------
# Service views
# -----------------------------

#Ambulance

def ambulance_driver_registration(request):
    return render(request,"Ambulance_registration.html")

def service_registration(request):
    services=ServiceCategoryDb.objects.all()
    return render(request,"Registrations.html",{"services":services})

def ambulance_service_page(request):
    services=ServiceCategoryDb.objects.all()
    return render(request,"Ambulance.html",{"services":services})

def ambulance_register(request):
    if request.method == 'POST':
        driver_name = request.POST.get('driver_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        license_number = request.POST.get('license_number')
        ambulance_number = request.POST.get('ambulance_number')
        address = request.POST.get('address')
        username = request.POST.get('username')
        password = request.POST.get('password')
        driver_photo = request.FILES.get('driver_photo')

        # PASSWORD STRENGTH CHECK (added)
        valid, error = is_strong_password(password)
        if not valid:
            messages.error(request, error)
            return redirect(request.META.get('HTTP_REFERER'))

        # Check if email or username or license or ambulance number already exists
        if AmbulanceDriver.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect(request.META.get('HTTP_REFERER'))

        if AmbulanceDriver.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect(request.META.get('HTTP_REFERER'))

        if AmbulanceDriver.objects.filter(license_number=license_number).exists():
            messages.error(request, "License number already exists!")
            return redirect(request.META.get('HTTP_REFERER'))

        if ambulance_number and AmbulanceDriver.objects.filter(ambulance_number=ambulance_number).exists():
            messages.error(request, "Ambulance number already exists!")
            return redirect(request.META.get('HTTP_REFERER'))

        # Create model instance
        obj = AmbulanceDriver(
            driver_name=driver_name,
            email=email,
            phone=phone,
            license_number=license_number,
            ambulance_number=ambulance_number,
            address=address,
            username=username,
            password=password,
            driver_photo=driver_photo,
            is_available=True,
            is_active=True
        )

        obj.save()
        messages.success(request, "Ambulance registered successfully!")
        return redirect(request.META.get('HTTP_REFERER'))

    return redirect('Home')



def ambulance_driver_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            driver = AmbulanceDriver.objects.get(email=email, password=password, is_active=True)

            # store driver session
            request.session['driver_id'] = driver.id
            request.session['driver_name'] = driver.driver_name

            messages.success(request, "Login successful")
            return redirect('driver_dashboard')

        except AmbulanceDriver.DoesNotExist:
            messages.error(request, "Invalid email or password")
            return redirect(request.META.get('HTTP_REFERER'))

    return redirect('Home')


def driver_logout(request):
    request.session.flush()
    messages.success(request, "Logged out successfully")
    return redirect('Home')





def check_request_status(request):
    req_id = request.session.get('request_id')

    if not req_id:
        return redirect('Home')

    req = AmbulanceRequest.objects.get(id=req_id)

    if req.status == 'accepted':
        messages.success(request, " Ambulance accepted! Driver is on the way.")
        del request.session['request_id']

    elif req.status == 'rejected':
        messages.error(request, " No ambulance accepted your request.")
        del request.session['request_id']

    return redirect('Home')





# --------------------------------------------------
# Twilio Client
# --------------------------------------------------
twilio_client = Client(
    settings.TWILIO_ACCOUNT_SID,
    settings.TWILIO_AUTH_TOKEN
)


# --------------------------------------------------
# SIMPLE NOTIFICATION HELPERS
# --------------------------------------------------
def send_sms(phone, message):
    try:
        twilio_client.messages.create(
            body=message,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone
        )
    except Exception as e:
        print("SMS Error:", e)


def send_email(subject, message, to_email):
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [to_email],
            fail_silently=False
        )
    except Exception as e:
        print("Email Error:", e)


# ==================================================
# 1️ USER REQUESTS AMBULANCE
# ==================================================
def request_ambulance(request):
    if request.method == "POST":

        print("🚀 Ambulance request received")

        ambulance_request = AmbulanceRequest.objects.create(
            patient_name=request.POST.get("patient_name"),
            contact_number=request.POST.get("contact_number"),
            contact_email=request.POST.get("contact_email"),
            pickup_location=request.POST.get("pickup_location"),
            emergency_note=request.POST.get("emergency_note", ""),
            status="pending"
        )

        drivers = AmbulanceDriver.objects.filter(
            is_available=True,
            is_active=True
        )

        print("👨‍✈️ Drivers found:", drivers.count())

        for driver in drivers:
            print("📧 Sending email to:", driver.email)

            AmbulanceAssignment.objects.create(
                request=ambulance_request,
                driver=driver
            )

            subject = "🚑 New Ambulance Request"

            message = f"""
Hello {driver.driver_name},

You have received a new emergency ambulance request.

Patient Name : {ambulance_request.patient_name}
Pickup Location : {ambulance_request.pickup_location}
Contact Number : {ambulance_request.contact_number}

Please login and accept or reject the request.

– LifeLink Health Portal
"""

            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [driver.email],
                    fail_silently=False
                )
                print("✅ Email sent successfully")

            except Exception as e:
                print("❌ Email error:", e)

        messages.success(request, "Ambulance request sent! Drivers notified.")
        return redirect("Home")

    return redirect("Home")


# ==================================================
# 2️ DRIVER DASHBOARD
# ==================================================

def driver_dashboard(request):
    driver_id = request.session.get('driver_id')

    if not driver_id:
        return redirect('driver_login')

    # Logged-in driver
    current_driver = get_object_or_404(
        AmbulanceDriver,
        id=driver_id,
        is_active=True
    )

    # Show only waiting requests assigned to this driver
    waiting_assignments = AmbulanceAssignment.objects.filter(
        driver=current_driver,
        status='waiting',
        request__status='pending'   # IMPORTANT
    ).select_related('request')

    return render(request, 'Driver_dashboard.html', {
        'current_driver': current_driver,
        'waiting_assignments': waiting_assignments
    })



# ==================================================
# 3️ DRIVER ACCEPTS REQUEST
# =================================================
def accept_request(request, req_id):
    driver_id = request.session.get('driver_id')
    if not driver_id:
        return redirect('driver_login')

    driver = get_object_or_404(AmbulanceDriver, id=driver_id, is_active=True)

    # Get the waiting assignment for this driver
    try:
        assignment = AmbulanceAssignment.objects.get(
            request_id=req_id,
            driver=driver,
            status='waiting'
        )
    except AmbulanceAssignment.DoesNotExist:
        messages.error(request, "No pending assignment found for you.")
        return redirect('driver_dashboard')
    except AmbulanceAssignment.MultipleObjectsReturned:
        # pick the first waiting assignment
        assignment = AmbulanceAssignment.objects.filter(
            request_id=req_id,
            driver=driver,
            status='waiting'
        ).first()

    ambulance_request = assignment.request

    # Prevent multiple acceptance
    if ambulance_request.status == 'accepted':
        messages.error(request, "This request is already accepted by another driver.")
        return redirect('driver_dashboard')

    # Update assignment
    assignment.status = 'accepted'
    assignment.save()

    # Update request
    ambulance_request.status = 'accepted'
    ambulance_request.assigned_driver = driver
    ambulance_request.save()

    # Reject all other drivers for this request
    AmbulanceAssignment.objects.filter(
        request=ambulance_request
    ).exclude(id=assignment.id).update(status='rejected')

    # Send email to user
    if ambulance_request.contact_email:
        subject = "🚑 Ambulance Request Accepted"
        message = f"""
Dear {ambulance_request.patient_name},

Your ambulance request has been ACCEPTED.

🚑 Driver Details:
Name  : {driver.driver_name}
Phone : {driver.phone}

📍 Pickup Location:
{ambulance_request.pickup_location}

The driver will contact you shortly.

Thank you for using LifeLink Health Portal.
"""
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [ambulance_request.contact_email],
                fail_silently=False
            )
            print(" User email sent successfully")
        except Exception as e:
            print(" Email error:", e)

    messages.success(request, "Request accepted and user notified.")
    return redirect('driver_dashboard')




# ==================================================
# 4️ DRIVER REJECTS REQUEST
# ==================================================
def reject_request(request, assignment_id):
    assignment = get_object_or_404(AmbulanceAssignment, id=assignment_id)

    if assignment.status != "waiting":
        messages.error(request, "This request has already been handled.")
        return redirect('driver_dashboard')

    # Mark this driver's assignment as rejected
    assignment.status = "rejected"
    assignment.save()

    # Keep the main request pending for other drivers
    ambulance_request = assignment.request
    ambulance_request.status = "pending"
    ambulance_request.assigned_driver = None
    ambulance_request.save()

    messages.success(request, "You rejected this request. It is now available for other drivers.")
    return redirect('driver_dashboard')



#test email only for testing
def test_driver_email(request):
    driver = AmbulanceDriver.objects.first()

    send_mail(
        "Test Driver Email",
        "Email sending is working",
        settings.DEFAULT_FROM_EMAIL,
        [driver.email],
        fail_silently=False
    )

    return HttpResponse("Driver email sent")



#password reset for user






def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = UserRegistration.objects.get(Email=email)
        except UserRegistration.DoesNotExist:
            messages.error(request, "Email not registered")
            return redirect('forgot_password_page')

        # Generate token
        reset_token = str(uuid.uuid4())
        PasswordReset.objects.create(user=user, token=reset_token)

        # Create reset link
        reset_link = f"http://127.0.0.1:8000/health_service_portal/reset-password/{reset_token}/"

        # Send email
        send_mail(
            subject="Reset your password",
            message=f"Click this link to reset your password: {reset_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )

        messages.success(request, "Reset link sent to your email")
        return redirect('signin_page')

    return render(request, 'Forgot_password.html')





def reset_password(request, token):
    try:
        reset = PasswordReset.objects.get(token=token)
    except PasswordReset.DoesNotExist:
        messages.error(request, "Invalid or expired reset link")
        return redirect('signin_page')

    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect(request.path)

        reset.user.Password = make_password(password)
        reset.user.Confirm_password = reset.user.Password
        reset.user.save()
        reset.delete()  # one-time use

        messages.success(request, "Password reset successful. Please login.")
        return redirect('signin_page')

    return render(request, 'Reset_password.html', {'token': token})



# ==================================================
# Hospital service views
# ==================================================


def hospital_staff_login_page(request):
    return render(request, 'Hospital_staff_login.html')




def hospital_staff_login_page(request):
    return render(request, 'Hospital_staff_login.html')

def hospital_staff_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        referer = request.META.get('HTTP_REFERER', '/')

        try:
            staff = HospitalStaff.objects.get(email=email)

            if check_password(password, staff.password):
                request.session.flush()

                request.session['hospital_staff_id'] = staff.id
                request.session['hospital_id'] = staff.hospital.id

                return redirect('hospital_dashboard')
            else:
                messages.error(request, "Invalid password")

        except HospitalStaff.DoesNotExist:
            messages.error(request, "Hospital staff not found")

        return redirect(referer)




def hospital_dashboard(request):
    staff_id = request.session.get('hospital_staff_id')
    hospital_id = request.session.get('hospital_id')

    if not staff_id or not hospital_id:
        return redirect('/')

    # Validate staff belongs to hospital
    staff = HospitalStaff.objects.filter(
        id=staff_id,
        hospital_id=hospital_id
    ).first()

    if not staff:
        request.session.flush()
        return redirect('/')

    hospital = staff.hospital

    beds = Bed.objects.filter(hospital=hospital)
    bookings = BedBooking.objects.filter(hospital=hospital)

    return render(request, 'Hospital_dashboard.html', {
        'hospital': hospital,
        'staff': staff,
        'beds': beds,
        'bookings': bookings
    })





def manage_beds(request):
    if 'hospital_staff_id' not in request.session:
        return redirect('/')

    hospital_id = request.session['hospital_id']
    beds = Bed.objects.filter(hospital_id=hospital_id)

    return render(request, 'Manage_beds.html', {'beds': beds})







def save_bed(request):
    if request.method == "POST":

        # 1. Check hospital staff login
        hospital_id = request.session.get('hospital_id')
        if not hospital_id:
            return redirect('/')

        # 2. Get form data
        bed_type = request.POST.get('bed_type')
        total_beds = int(request.POST.get('total_beds'))
        available_beds = int(request.POST.get('available_beds'))
        price = request.POST.get('price')

        # 3. Validation
        if available_beds > total_beds:
            messages.error(request, "Available beds cannot be more than total beds")
            return redirect('manage_beds')

        # 4. Check if bed already exists for this hospital
        try:
            bed = Bed.objects.get(
                hospital_id=hospital_id,
                bed_type=bed_type
            )

            # 5. Update existing bed
            bed.total_beds = total_beds
            bed.available_beds = available_beds
            bed.price_per_day = price
            bed.save()

            messages.success(request, "Bed details updated successfully")

        except Bed.DoesNotExist:
            # 6. Create new bed
            bed = Bed(
                hospital_id=hospital_id,
                bed_type=bed_type,
                total_beds=total_beds,
                available_beds=available_beds,
                price_per_day=price
            )
            bed.save()

            messages.success(request, "Bed added successfully")


        return redirect('manage_beds')





def approve_booking(request, booking_id):
    # Fetch booking safely
    booking = get_object_or_404(BedBooking, id=booking_id)

    # Prevent approving past-date bookings
    if booking.booking_date < date.today():
        messages.error(request, "Cannot approve a booking for a past date.")
        return redirect('hospital_dashboard')

    #  Prevent double approval
    if booking.status == 'APPROVED':
        messages.warning(request, "This booking is already approved.")
        return redirect('hospital_dashboard')

    bed = booking.bed
    booking_date = booking.booking_date

    # 🔒 Atomic transaction (real-world safety)
    with transaction.atomic():
        approved_count = BedBooking.objects.select_for_update().filter(
            bed=bed,
            booking_date=booking_date,
            status='APPROVED'
        ).count()

        # ❌ No availability
        if approved_count >= bed.total_beds:
            messages.error(
                request,
                f"No {bed.bed_type} beds available on {booking_date}"
            )
            return redirect('hospital_dashboard')

        # ✅ Approve booking
        booking.status = 'APPROVED'
        booking.decision_at = timezone.now()
        booking.save()

    # 📧 Send Email Notification
    subject = "Your Bed Booking is Approved"
    message = f"""
Hello {booking.patient_name},

Your bed booking has been APPROVED ✅

Hospital: {booking.hospital.name}
Bed Type: {booking.bed.bed_type}
Booking Date: {booking.booking_date}

Patient Name: {booking.patient_name}
Age: {booking.patient_age}
Emergency: {"Yes" if booking.is_emergency else "No"}

Please reach the hospital on the booked date.

Thank you for using LifeLink Health Services.
"""

    send_mail(
        subject,
        message,
        'noreply@lifelink.com',
        [booking.user.Email],
        fail_silently=False
    )

    messages.success(request, "Booking approved successfully and email sent.")
    return redirect('hospital_dashboard')






def reject_booking(request, booking_id):
    booking = get_object_or_404(BedBooking, id=booking_id)

    # Prevent re-processing
    if booking.status != 'PENDING':
        messages.warning(request, "This booking has already been processed.")
        return redirect('hospital_dashboard')

    booking.status = 'REJECTED'
    booking.decision_at = timezone.now()
    booking.save()

    messages.success(request, "Booking rejected successfully.")
    return redirect('hospital_dashboard')





def get_available_beds(bed, booking_date):
    """
    Returns the number of available beds of this type on a given date.
    """
    booked_count = BedBooking.objects.filter(
        bed=bed,
        booking_date=booking_date,
        status__in=['PENDING', 'APPROVED']
    ).aggregate(
        total=Sum('beds_required')
    )['total'] or 0

    return max(bed.total_beds - booked_count, 0)




def book_bed_page(request):
    services = ServiceCategoryDb.objects.all()
    query = request.GET.get('q', '')

    hospitals = Hospital.objects.filter(is_verified=True)
    if query:
        hospitals = hospitals.filter(
            name__icontains=query
        ) | hospitals.filter(
            city__icontains=query
        ) | hospitals.filter(
            state__icontains=query
        )

    today = date.today()

    # Attach available beds count per hospital
    for hospital in hospitals:
        beds = Bed.objects.filter(hospital=hospital)
        hospital.available_beds_today = sum(get_available_beds(bed, today) for bed in beds)

    return render(request, 'Hospital_bed_booking.html', {
        'services':services,
        'hospitals': hospitals,
        'query': query
    })






def user_book_bed_page(request, hospital_id):
    services=ServiceCategoryDb.objects.all()

    if 'user_id' not in request.session:
        messages.error(request, "Please log in to book a bed.")
        return redirect('Home')

    hospital = get_object_or_404(Hospital, id=hospital_id)
    beds = Bed.objects.filter(hospital=hospital)

    today = date.today()

    # Attach availability per bed
    for bed in beds:
        bed.available_today = get_available_beds(bed, today)

    return render(request, 'User_book_bed.html', {
        'services':services,
        'hospital': hospital,
        'beds': beds,
        'today_date': today
    })










def submit_bed_booking(request, hospital_id):
    if 'user_id' not in request.session:
        messages.error(request, "Please log in to book a bed.")
        return redirect('Home')

    if request.method != "POST":
        return redirect('user_book_bed_page', hospital_id=hospital_id)

    user_id = request.session['user_id']
    bed_id = request.POST.get('bed_id')
    patient_name = request.POST.get('patient_name')
    patient_age = request.POST.get('patient_age')
    is_emergency = 'is_emergency' in request.POST
    booking_date = request.POST.get('booking_date')
    beds_required = int(request.POST.get('beds_required', 1))

    if not booking_date:
        messages.error(request, "Please select a booking date.")
        return redirect('user_book_bed_page', hospital_id=hospital_id)

    booking_date = date.fromisoformat(booking_date)
    if booking_date < date.today():
        messages.error(request, "You cannot book beds for past dates.")
        return redirect('user_book_bed_page', hospital_id=hospital_id)

    hospital = get_object_or_404(Hospital, id=hospital_id)
    bed = get_object_or_404(Bed, id=bed_id, hospital=hospital)
    user = get_object_or_404(UserRegistration, id=user_id)

    # SIMPLE PRICE CALCULATION
    total_price = bed.price_per_day * beds_required

    # UPDATED DUPLICATE CHECK (CANCELLED BOOKINGS IGNORED)
    if BedBooking.objects.filter(
        user=user,
        bed=bed,
        booking_date=booking_date,
        status__in=['PENDING', 'APPROVED']
    ).exists():
        messages.warning(
            request,
            "You have already booked this bed for the selected date."
        )
        return redirect('user_book_bed_page', hospital_id=hospital_id)

    # CHECK AVAILABILITY USING SUM
    booked_count = BedBooking.objects.filter(
        bed=bed,
        booking_date=booking_date,
        status__in=['PENDING', 'APPROVED']
    ).aggregate(
        total=Sum('beds_required')
    )['total'] or 0

    available = bed.total_beds - booked_count

    if beds_required > available:
        messages.error(
            request,
            f"Only {available} {bed.bed_type} beds available on {booking_date}."
        )
        return redirect('user_book_bed_page', hospital_id=hospital_id)

    # CREATE BOOKING
    BedBooking.objects.create(
        user=user,
        hospital=hospital,
        bed=bed,
        patient_name=patient_name,
        patient_age=patient_age,
        is_emergency=is_emergency,
        booking_date=booking_date,
        beds_required=beds_required,
        total_price=total_price,
        status='PENDING'
    )

    messages.success(request, "Booking request submitted successfully!")
    return redirect('user_dashboard')








# User dashboard


def user_dashboard(request):
    services=ServiceCategoryDb.objects.all()

    if 'user_id' not in request.session:
        messages.error(request, "Please log in.")
        return redirect('Home')

    user_id = request.session['user_id']
    today = date.today()

    bookings = BedBooking.objects.filter(
        user_id=user_id,
        booking_date__gte=today
    ).exclude(
        status__in=['CANCELLED', 'REJECTED']
    ).select_related(
        'hospital', 'bed'
    ).order_by('booking_date')

    return render(request, 'user_dashboard.html', {
        'services':services,
        'bookings': bookings,
        'today': today
    })









def cancel_bed_booking(request, booking_id):
    if 'user_id' not in request.session:
        messages.error(request, "Please log in.")
        return redirect('Home')

    booking = get_object_or_404(
        BedBooking,
        id=booking_id,
        user_id=request.session['user_id']
    )

    # Cannot cancel on or after booking date
    if booking.booking_date <= date.today():
        messages.error(request, "You cannot cancel on or after the booking date.")
        return redirect('user_dashboard')

    if booking.status == 'CANCELLED':
        messages.warning(request, "Booking already cancelled.")
        return redirect('user_dashboard')

    booking.status = 'CANCELLED'
    booking.save()

    messages.success(request, "Booking cancelled successfully. You can rebook on the same date.")
    return redirect('user_dashboard')



# HospitalJoinRequest

def contact_admin(request):
    if request.method == "POST":
        hospital_name = request.POST.get('hospital_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        HospitalJoinRequest.objects.create(
            hospital_name=hospital_name,
            email=email,
            phone=phone,
            message=message
        )

        messages.success(
            request,
            "Your request has been sent to the admin. We will contact you soon."
        )

    return redirect('service_registration')




def hospital_map(request):
    hospitals = Hospital.objects.filter(is_active=True)
    return render(request, "Hospital_map.html", {
        "hospitals": hospitals
    })




