from django.shortcuts import render,redirect,get_object_or_404
from django.utils.datastructures import MultiValueDictKeyError
from admin_panel.models import ServiceCategoryDb,BloodCategory
from webapp.models import UserRegistration,DonorRegistrationDb,ContactDb
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from datetime import date, timedelta
from django.core.files.storage import FileSystemStorage

#for email  sms and profile notifications

from .models import BloodRequest, UserRegistration
from Health_portal.notifications import notify_donors
from datetime import datetime


from .models import DonorNotification, DonorRegistrationDb






# Create your views here.

def home_page(request):
    services=ServiceCategoryDb.objects.all()
    return render(request,"Home.html",{"services":services})
def service_page(request):
    return render(request,"Services.html")
def donors_page(request):
    services = ServiceCategoryDb.objects.all()
    donors=DonorRegistrationDb.objects.all()
    locations = DonorRegistrationDb.objects.values_list("Location", flat=True).distinct()
    # Get unique blood groups
    blood_groups = DonorRegistrationDb.objects.values_list("BloodGroup", flat=True).distinct()
    return render(request,"Donors.html",{"services":services,"donors":donors,"locations":locations,"blood_groups":blood_groups})
def contact_page(request):
    return render(request,"Contact.html")
def about_page(request):
    return render(request,"About.html")
def signup_page(request):
    return render(request,"Signup_page.html")
def signin_page(request):
    return render(request,"Signin_page.html")

def user_signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if user already exists
        if UserRegistration.objects.filter(Email=email).exists():
            return redirect('signup_page')
        elif UserRegistration.objects.filter(Name=name).exists():
            return redirect('signup_page')
        elif password != confirm_password:
            return redirect('signup_page')
        else:
            # HASH THE PASSWORD
            hashed_password = make_password(password)

            user = UserRegistration(
                Name=name,
                Email=email,
                Phone=phone,
                Password=hashed_password,
                Confirm_password=hashed_password,
            )
            user.save()
            # print("User created successfully")
            return redirect('signin_page')

    return redirect('signup_page')




def user_login(request):
    if request.method == 'POST':
        un = request.POST.get('username')
        pswd = request.POST.get('password')

        try:
            user =UserRegistration.objects.get(Name=un)
        except UserRegistration.DoesNotExist:
            # print("Invalid credentials") using js
            return redirect('signin_page')

        # CHECK HASHED PASSWORD
        if check_password(pswd, user.Password):

            # Create session using user_id
            request.session['user_id'] = user.id
            request.session['Name'] = user.Name

            return redirect('Home')
        else:
            # print("Invalid credentials") using js
            return redirect('signin_page')

    return redirect('signin_page')

def user_logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    if 'Name' in request.session:
        del request.session['Name']

    return redirect('signin_page')


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

        # Validations
        if DonorRegistrationDb.objects.filter(Email=email).exists():
            # messages.error(request, "Email already exists")
            return redirect('donor_signup')
        elif password != confirm_password:
            # messages.error(request, "Passwords do not match")
            return redirect('donor_signup')

        # Hash password
        hashed_password = make_password(password)

        donor = DonorRegistrationDb(
            Name=name,
            Email=email,
            phone=phone,
            BloodGroup=blood_group,
            Location=location,
            Password=hashed_password,
            Confirm_password=hashed_password,
            Age=age,
            Gender=gender,
            Image=image,
            is_active=True
        )
        donor.save()
        # messages.success(request, "Donor registered successfully! Please login.")
        return redirect('donor_login_page')

    return redirect('donor_signup_page')



# Donor Login

def donor_login(request):
    if request.method == 'POST':
        email = request.POST.get('Email')  # Use Email instead of Name
        password = request.POST.get('Password')

        try:
            donor = DonorRegistrationDb.objects.get(Email=email)
        except DonorRegistrationDb.DoesNotExist:
            # messages.error(request, "Invalid credentials")
            return redirect('donor_login_page')

        # Check hashed password
        if check_password(password, donor.Password):
            # Save session (ID and Name)
            request.session['donor_id'] = donor.id
            request.session['donor_name'] = donor.Name
            return redirect('donor_profile')
        else:
            # messages.error(request, "Invalid credentials")
            return redirect('donor_login_page')

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
        'days_left': days_left
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
    if donor_id:
        donor = DonorRegistrationDb.objects.get(id=donor_id)
        donor.last_donation_date = date.today()
        donor.is_active = False
        donor.system_inactive = True
        donor.save()
    return redirect('donor_profile')


# filter donors based on location and blood group

def filtered_donors(request):
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
        "blood_groups":blood_groups

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

        patient_name = request.POST.get('patient_name') or user.Name
        blood_group = request.POST.get('blood_group')
        units = int(request.POST.get('units') or 1)
        location = request.POST.get('location')
        phone = request.POST.get('phone')
        needed_date = datetime.strptime(request.POST.get('needed_date'), "%Y-%m-%d").date()
        reason = request.POST.get('reason')

        # Create BloodRequest instance with all fields and save
        br = BloodRequest(
            requester=user,
            patient_name=patient_name,
            blood_group=blood_group,
            units=units,
            location=location,
            phone=phone,
            needed_date=needed_date,
            reason=reason
        )
        br.save()  # Save to database

        # Notify matching donors
        notify_donors(br)

        return redirect('blood_request_success')

    return redirect('blood_request_form')



def donor_notifications(request):
    if 'donor_id' not in request.session:
        return redirect('donor_login_page')

    donor = DonorRegistrationDb.objects.get(id=request.session['donor_id'])

    # Show notifications based on donor's blood group
    notifications = DonorNotification.objects.filter(
        blood_request__blood_group__iexact=donor.BloodGroup
    ).order_by('-created_at')

    return render(request, "Donor_notification.html", {
        "donor": donor,
        "notifications": notifications
    })


