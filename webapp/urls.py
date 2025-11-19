from django.urls import path
from webapp import views

urlpatterns=[
    path('Home/',views.home_page,name="Home"),
    path('Services/',views.service_page,name="Services"),
    path('Donors/',views.donors_page,name="Donors"),



]