from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/',views.about, name='about'),
    path('blood_types/',views.blood_types, name='blood_types'),
    path('find-blood/', views.find_blood, name='find_blood'),
    path('contact/',views.contact, name='contact'),
    path('register/donor/', views.register_donor, name='register_donor'),
    path('register/patient/', views.register_patient, name='register_patient'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Admin
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('management/donors/', views.admin_donors, name='admin_donors'),
    path('management/donors/approve/<int:pk>/', views.approve_donor, name='approve_donor'),
    path('management/donors/delete/<int:pk>/', views.delete_donor, name='delete_donor'),
    path('management/donors/edit/<int:pk>/', views.edit_donor, name='edit_donor'),
    path('management/donors/reject/<int:pk>/', views.reject_donor, name='reject_donor'),
    path('management/patients/', views.admin_patients, name='admin_patients'),
    path('management/patients/delete/<int:pk>/', views.delete_patient, name='delete_patient'),
    path('management/patients/edit/<int:pk>/', views.edit_patient, name='edit_patient'),
    path('management/blood-stock/', views.admin_blood_stock, name='admin_blood_stock'),
    path('management/blood-stock/update/', views.update_blood_stock, name='update_blood_stock'),
    path('management/blood-requests/', views.admin_blood_requests, name='admin_blood_requests'),
    path('management/blood-requests/<int:pk>/<str:action>/', views.handle_blood_request, name='handle_blood_request'),
    path('management/donation-requests/', views.admin_donation_requests, name='admin_donation_requests'),
    path('management/donation-requests/<int:pk>/<str:action>/', views.handle_donation_request, name='handle_donation_request'),

    # Donor
    path('donor-dashboard/', views.donor_dashboard, name='donor_dashboard'),

    # Patient
    path('patient-dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('patient/request-blood/', views.request_blood, name='request_blood'),
    path('patient/my-requests/', views.my_blood_requests, name='my_blood_requests'),
    path('patient/profile/', views.patient_profile, name='patient_profile'),

      # Donor
    path('donor-dashboard/', views.donor_dashboard, name='donor_dashboard'),
    path('donor/donate/', views.submit_donation, name='submit_donation'),
    path('donor/my-donations/', views.my_donations, name='my_donations'),
    path('donor/profile/', views.donor_profile, name='donor_profile'),

     # DRF APIs
    path('api/donors/', views.api_donors, name='api_donors'),
    path('api/patients/', views.api_patients, name='api_patients'),
    path('api/blood-stock/', views.api_blood_stock, name='api_blood_stock'),
    path('api/blood-requests/', views.api_blood_requests, name='api_blood_requests'),
    path('api/donation-requests/', views.api_donation_requests, name='api_donation_requests'),
    
    path('donor/change-password/', views.donor_change_password, name='donor_change_password'),
    path('patient/change-password/', views.patient_change_password, name='patient_change_password'),

    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('send_email/', views.send_email, name='sendemail'),

]