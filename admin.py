from django.contrib import admin
from .models import DonorProfile , PatientProfile, BloodStock, BloodRequest, DonationRequest

#Register admin here

@admin.register(DonorProfile)
class DonorAdmin(admin.ModelAdmin):
    list_display  = ['username', 'blood_group', 'phone', 'age', 'is_approved', 'created_at']
    list_filter   = ['blood_group', 'is_approved']
    search_fields = ['username', 'phone']

@admin.register(PatientProfile)
class PatientAdmin(admin.ModelAdmin):
    list_display  = ['username', 'blood_group', 'phone', 'hospital', 'doctor_name', 'created_at']
    list_filter   = ['blood_group']
    search_fields = ['username', 'phone', 'hospital']


@admin.register(BloodStock)
class BloodStockAdmin(admin.ModelAdmin):
    list_display  = ['blood_group', 'units', 'updated_at']


@admin.register(BloodRequest)
class BloodRequestAdmin(admin.ModelAdmin):
    list_display  = ['patient_username', 'blood_group', 'units_needed', 'urgency', 'status', 'date_requested']
    list_filter   = ['status', 'urgency', 'blood_group']
    search_fields = ['patient_username']


@admin.register(DonationRequest)
class DonationRequestAdmin(admin.ModelAdmin):
    list_display  = ['donor_username', 'blood_group', 'units', 'status', 'date_requested']
    list_filter   = ['status', 'blood_group']
    search_fields = ['donor_username']
    