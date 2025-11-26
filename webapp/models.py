from django.db import models

# Create your models here.

class UserRegistration(models.Model):
    Name = models.CharField(max_length=100, null=True, blank=True)
    Email = models.EmailField(unique=True, null=True, blank=True)
    Phone = models.CharField(max_length=15, null=True, blank=True)
    Password = models.CharField(max_length=200, null=True, blank=True)   # store hashed
    Confirm_password = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.Name

class DonorRegistrationDb(models.Model):
    Name = models.CharField(max_length=100, null=True, blank=True)
    Email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    BloodGroup = models.CharField(max_length=10, null=True, blank=True)
    Location = models.CharField(max_length=200, null=True, blank=True)
    Password = models.CharField(max_length=100, null=True, blank=True)
    Confirm_password = models.CharField(max_length=100, null=True, blank=True)
    Age = models.IntegerField(null=True, blank=True)
    Gender = models.CharField(max_length=10, null=True, blank=True)
    Image = models.ImageField(upload_to='donor_images/', null=True, blank=True)

    # active or inactive
    is_active = models.BooleanField(default=True)
    system_inactive = models.BooleanField(default=False)
    # Track last donation date
    last_donation_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.Name

class ContactDb(models.Model):
    User_name = models.CharField(max_length=100, null=True, blank=True)
    User_email = models.EmailField(null=True, blank=True)
    Subject = models.CharField(max_length=100, null=True, blank=True)
    Message = models.TextField(null=True, blank=True)

