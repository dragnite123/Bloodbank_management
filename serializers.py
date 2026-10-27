from rest_framework import serializers
from .models import DonorProfile, PatientProfile, BloodStock, BloodRequest, DonationRequest

class DonorSerializer(serializers.ModelSerializer):
    class Meta:
        model  = DonorProfile
        fields = ['id', 'username', 'full_name', 'email', 'blood_group', 'phone', 'address', 'age', 'weight', 'is_approved', 'created_at']

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model  = PatientProfile
        fields = ['id', 'username', 'full_name', 'email', 'blood_group', 'phone', 'address', 'age', 'doctor_name', 'hospital', 'created_at']

class BloodStockSerializer(serializers.ModelSerializer):
    class Meta:
        model  = BloodStock
        fields = ['id', 'blood_group', 'units', 'updated_at']

class BloodRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model  = BloodRequest
        fields = ['id', 'patient_username', 'blood_group', 'units_needed', 'urgency', 'doctor_name', 'hospital', 'reason', 'status', 'date_requested']

class DonationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model  = DonationRequest
        fields = ['id', 'donor_username', 'blood_group', 'units', 'status', 'date_requested']

