from django.urls import path
from webapp import views


urlpatterns=[
    path('Home/',views.home_page,name="Home"),
    path('Services/',views.service_page,name="Services"),
    path('Donors/',views.donors_page,name="Donors"),
    path('Contact/',views.contact_page,name="Contact"),
    path('About/',views.about_page,name="About"),
    path('service_detail/<int:service_id>/',views.service_detail,name="service_detail"),
    path('signup_page/',views.signup_page,name="signup_page"),
    path('signin_page/',views.signin_page,name="signin_page"),
    path('user_signup/',views.user_signup,name="user_signup"),
    path('user_login/',views.user_login,name="user_login"),
    path('user_logout/',views.user_logout,name="user_logout"),
    path('donor_signup_page/',views.donor_signup_page,name="donor_signup_page"),
    path('donor_login_page/',views.donor_login_page,name="donor_login_page"),
    path('donor_signup/',views.donor_signup,name="donor_signup"),
    path('donor_login/',views.donor_login,name="donor_login"),
    path('donor_logout/',views.donor_logout,name="donor_logout"),
    path('donor_profile/',views.donor_profile,name="donor_profile"),
    path('edit_donor_profile/<int:donor_id>/', views.edit_donor_profile, name='edit_donor_profile'),
    path('update_donor_profile/<int:donor_id>/', views.update_donor_profile, name='update_donor_profile'),
    path('toggle_donor_status/',views.toggle_donor_status,name="toggle_donor_status"),
    path('mark_donated/',views.mark_donated,name="mark_donated"),
    path('filtered_donors/',views.filtered_donors,name="filtered_donors"),
    path('save_contact/',views.save_contact,name="save_contact"),
    path('blood_request_form/',views.blood_request_form,name="blood_request_form"),
    path('blood_request_success/',views.blood_request_success,name="blood_request_success"),
    path('request_blood/',views.request_blood,name="request_blood"),
    path('donor/notifications/', views.donor_notifications, name='donor_notifications'),
    path('blood-request/accept/<int:request_id>/', views.accept_blood_request, name='accept_blood_request' ),
    path('blood-request/reject/<int:request_id>/',views.reject_blood_request,name='reject_blood_request'),


    # Ambulance
    path('ambulance_driver_registration/',views.ambulance_driver_registration,name="ambulance_driver_registration"),
    path('service_registration/',views.service_registration,name="service_registration"),
    path('ambulance_service_page/',views.ambulance_service_page,name="ambulance_service_page"),
    path('ambulance_register/',views.ambulance_register,name="ambulance_register"),
    path('driver_login/',views.ambulance_driver_login,name="driver_login"),
    path('driver_dashboard/',views.driver_dashboard,name="driver_dashboard"),
    path('driver_logout/',views.driver_logout,name="driver_logout"),
    path('request_ambulance/', views.request_ambulance, name='request_ambulance'),
    path('driver_dashboard/', views.driver_dashboard, name='driver_dashboard'),
    path('accept_request/<int:req_id>/', views.accept_request, name='accept_request'),
    path('reject_request/<int:assignment_id>/', views.reject_request, name='reject_request'),
    path('check_request_status/', views.check_request_status, name='check_request_status'),
    path('test_driver_email/', views.test_driver_email),

    #password reset
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<str:token>/', views.reset_password, name='reset_password'),




    #Hospital
    path('hospital_staff_login_page/',views.hospital_staff_login_page,name='hospital_staff_login_page'),
    path('hospital_staff_login/',views.hospital_staff_login,name='hospital_staff_login'),
    path('hospital_dashboard/',views.hospital_dashboard,name='hospital_dashboard'),
    path('manage_beds/',views.manage_beds,name='manage_beds'),
    path('save_bed/',views.save_bed,name='save_bed'),
    path('approve_booking/<int:booking_id>',views.approve_booking,name='approve_booking'),
    path('reject_booking/<int:booking_id>',views.reject_booking,name='reject_booking'),
    path('book_bed_page/',views.book_bed_page,name='book_bed_page'),
    path('user_book_bed_page/<int:hospital_id>',views.user_book_bed_page,name='user_book_bed_page'),
    path('submit_bed_booking/<int:hospital_id>',views.submit_bed_booking,name='submit_bed_booking'),
    path('cancel_bed_booking/<int:booking_id>',views.cancel_bed_booking,name='cancel_bed_booking'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('contact_admin/', views.contact_admin, name='contact_admin'),


    # Map
    path("hospitals/map/",views.hospital_map, name="hospital_map"),





]