from django.db import models


# Create your models here.
class Manager(models.Model):
    id = models.AutoField(primary_key=True)
    firstname = models.TextField(max_length=255)
    lastname = models.TextField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.TextField()
    address = models.TextField()
    dob = models.DateField()
    company = models.TextField(max_length=100)
    strip_id = models.TextField(blank=True)
    product_id = models.TextField(blank=True)
    subscription_id = models.TextField(blank=True)
