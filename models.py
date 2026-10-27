from django.db import models

# Create your models here.
class DonorProfile(models.Model):
    username     = models.CharField(max_length=100)
    email        = models.CharField(max_length=100)
    password     = models.CharField(max_length=100)
    full_name    = models.CharField(max_length=100)
    blood_group  = models.CharField(max_length=5)
    phone        = models.CharField(max_length=15)
    address      = models.TextField()
    age          = models.IntegerField()
    weight       = models.FloatField()
    last_donated = models.DateField(null=True, blank=True)
    is_approved  = models.BooleanField(default=False)
    created_at   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} - {self.blood_group}"

class PatientProfile(models.Model):
    username    = models.CharField(max_length=100)
    email       = models.CharField(max_length=100)
    password    = models.CharField(max_length=100)
    full_name   = models.CharField(max_length=100)
    blood_group = models.CharField(max_length=5)
    phone       = models.CharField(max_length=15)
    address     = models.TextField()
    age         = models.IntegerField()
    doctor_name = models.CharField(max_length=100)
    hospital    = models.CharField(max_length=150)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} - {self.blood_group}"

class BloodStock(models.Model):
    blood_group = models.CharField(max_length=5)
    units       = models.IntegerField(default=0)
    updated_at  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.blood_group} - {self.units} units"

class BloodRequest(models.Model):
    patient_username = models.CharField(max_length=100)
    blood_group      = models.CharField(max_length=5)
    units_needed     = models.IntegerField()
    urgency          = models.CharField(max_length=10)
    doctor_name      = models.CharField(max_length=100)
    hospital         = models.CharField(max_length=150)
    reason           = models.TextField()
    status           = models.CharField(max_length=10, default='Pending')
    admin_note       = models.TextField(null=True, blank=True)
    date_requested   = models.DateTimeField(auto_now_add=True)
    date_updated     = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.patient_username} - {self.blood_group} - {self.status}"

class DonationRequest(models.Model):
    donor_username = models.CharField(max_length=100)
    blood_group    = models.CharField(max_length=5)
    units          = models.IntegerField()
    status         = models.CharField(max_length=10, default='Pending')
    admin_note     = models.TextField(null=True, blank=True)
    date_requested = models.DateTimeField(auto_now_add=True)
    date_updated   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.donor_username} - {self.blood_group} - {self.status}"
