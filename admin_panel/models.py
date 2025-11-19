from django.db import models

# Create your models here.


class ServiceCategoryDb(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='category_image/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

from django.db import models

class BloodCategory(models.Model):
    BLOOD_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
    ]
    name = models.CharField(max_length=3, choices=BLOOD_CHOICES, unique=True)

    def __str__(self):
        return self.name




