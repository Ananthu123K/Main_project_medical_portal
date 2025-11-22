from django.urls import path
from webapp import views

urlpatterns=[
    path('Home/',views.home_page,name="Home"),
    path('Services/',views.service_page,name="Services"),
    path('Donors/',views.donors_page,name="Donors"),
    path('Contact/',views.contact_page,name="Contact"),
    path('About/',views.about_page,name="About"),
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
    path('toggle_donor_status/',views.toggle_donor_status,name="toggle_donor_status"),
    path('mark_donated/',views.mark_donated,name="mark_donated"),
]