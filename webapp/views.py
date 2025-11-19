from django.shortcuts import render

# Create your views here.

def home_page(request):
    return render(request,"Home.html")
def service_page(request):
    return render(request,"Services.html")
def donors_page(request):
    return render(request,"Donors.html")