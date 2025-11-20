from django.shortcuts import render
from admin_panel.models import ServiceCategoryDb,BloodCategory

# Create your views here.

def home_page(request):
    services=ServiceCategoryDb.objects.all()
    return render(request,"Home.html",{"services":services})
def service_page(request):
    return render(request,"Services.html")
def donors_page(request):
    services = ServiceCategoryDb.objects.all()
    return render(request,"Donors.html",{"services":services})
def contact_page(request):
    return render(request,"Contact.html")
def about_page(request):
    return render(request,"About.html")