from django.db import models
from django.utils import timezone

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

    life_saved = models.PositiveIntegerField(default=0)#to store life saved count

    def __str__(self):
        return self.Name

class ContactDb(models.Model):
    User_name = models.CharField(max_length=100, null=True, blank=True)
    User_email = models.EmailField(null=True, blank=True)
    Subject = models.CharField(max_length=100, null=True, blank=True)
    Message = models.TextField(null=True, blank=True)

class BloodRequest(models.Model):
    requester = models.ForeignKey('UserRegistration', on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=150, null=True, blank=True)
    blood_group = models.CharField(max_length=10)
    units = models.PositiveIntegerField(default=1)
    location = models.CharField(max_length=250)
    phone = models.CharField(max_length=20)
    reason = models.TextField(null=True, blank=True)
    needed_date = models.DateField()  # IMPORTANT
    is_fulfilled = models.BooleanField(default=False)  # IMPORTANT

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient_name} - {self.blood_group}"

class DonorNotification(models.Model):
    donor = models.ForeignKey('DonorRegistrationDb', on_delete=models.CASCADE)
    blood_request = models.ForeignKey(BloodRequest, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    is_seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def should_delete(self):
        """Delete if request is fulfilled OR needed date is over."""
        if self.blood_request:
            if self.blood_request.is_fulfilled:
                return True
            if timezone.now().date() > self.blood_request.needed_date:
                return True
        return False

    def __str__(self):
        return f"Notif -> {self.donor.Name} ({'seen' if self.is_seen else 'new'})"
