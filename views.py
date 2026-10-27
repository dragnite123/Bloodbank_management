
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import DonorProfile, PatientProfile, BloodStock, BloodRequest, DonationRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import DonorSerializer, PatientSerializer, BloodStockSerializer, BloodRequestSerializer, DonationRequestSerializer
from django.core.mail import send_mail
from django.http import HttpResponse

def home(request):
    blood_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
    return render(request, 'home.html', {'blood_groups': blood_groups})

def about(request):
    return render(request,'about.html')

def blood_types(request):
    return render(request,'blood_types.html')

def find_blood(request):
    return render(request, 'find_blood.html')

def contact(request):
    return render(request,'contact.html')

def register_donor(request):
    if request.method == 'POST':
        username         = request.POST.get('username')
        first_name       = request.POST.get('first_name')
        last_name        = request.POST.get('last_name')
        email            = request.POST.get('email')
        password         = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        blood_group      = request.POST.get('blood_group')
        phone            = request.POST.get('phone')
        address          = request.POST.get('address')
        age              = request.POST.get('age')
        weight           = request.POST.get('weight')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('register_donor')
        if DonorProfile.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return redirect('register_donor')

        DonorProfile.objects.create(
            username    = username,
            full_name   = first_name + ' ' + last_name,
            email       = email,
            password    = password,
            blood_group = blood_group,
            phone       = phone,
            address     = address,
            age         = age,
            weight      = weight,
        )
        messages.success(request, 'Donor registered! Wait for admin approval.')
        return redirect('login')
    return render(request, 'register_donor.html')

def register_patient(request):
    if request.method == 'POST':
        username         = request.POST.get('username')
        first_name       = request.POST.get('first_name')
        last_name        = request.POST.get('last_name')
        email            = request.POST.get('email')
        password         = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        blood_group      = request.POST.get('blood_group')
        phone            = request.POST.get('phone')
        address          = request.POST.get('address')
        age              = request.POST.get('age')
        doctor_name      = request.POST.get('doctor_name')
        hospital         = request.POST.get('hospital')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('register_patient')
        if PatientProfile.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return redirect('register_patient')

        PatientProfile.objects.create(
            username    = username,
            full_name   = first_name + ' ' + last_name,
            email       = email,
            password    = password,
            blood_group = blood_group,
            phone       = phone,
            address     = address,
            age         = age,
            doctor_name = doctor_name,
            hospital    = hospital,
        )
        messages.success(request, 'Patient registered successfully!')
        return redirect('login')
    return render(request, 'register_patient.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == 'admin' and password == 'admin123':
            request.session['user'] = 'admin'
            request.session['username'] = username
            return redirect('admin_dashboard')

        donor = DonorProfile.objects.filter(username=username, password=password).first()
        if donor:
            if not donor.is_approved:
                messages.error(request, 'Your account is not approved by admin yet.')
                return redirect('login')
            request.session['user'] = 'donor'
            request.session['username'] = username
            return redirect('donor_dashboard')

        patient = PatientProfile.objects.filter(username=username, password=password).first()
        if patient:
            request.session['user'] = 'patient'
            request.session['username'] = username
            return redirect('patient_dashboard')

        messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

def logout_view(request):
    request.session.flush()
    return redirect('login')

# ─── ADMIN VIEWS ───────────────────────────────────────────

def admin_dashboard(request):
    if request.session.get('user') != 'admin':
        return redirect('login')
    context = {
        'total_donors'              : DonorProfile.objects.count(),
        'approved_donors'           : DonorProfile.objects.filter(is_approved=True).count(),
        'pending_donors'            : DonorProfile.objects.filter(is_approved=False).count(),
        'total_patients'            : PatientProfile.objects.count(),
        'blood_stock'               : BloodStock.objects.all(),
        'pending_blood_requests'    : BloodRequest.objects.filter(status='Pending').count(),
        'pending_donation_requests' : DonationRequest.objects.filter(status='Pending').count(),
        'recent_blood_requests'     : BloodRequest.objects.order_by('-date_requested')[:5],
        'recent_donations'          : DonationRequest.objects.order_by('-date_requested')[:5],
        'low_stock'                 : BloodStock.objects.filter(units__lt=5).exclude(units=0),
        'out_of_stock'              : BloodStock.objects.filter(units=0),
    }
    return render(request, 'admin_dashboard.html', context)


def admin_donors(request):
    if request.session.get('user') != 'admin':
        return redirect('login')
    donors = DonorProfile.objects.all().order_by('-created_at')
    return render(request, 'admin_donors.html', {'donors': donors})

def approve_donor(request, pk):
    if request.session.get('user') != 'admin':
        return redirect('login')
    donor = get_object_or_404(DonorProfile, pk=pk)
    donor.is_approved = True
    donor.save()
    send_email(
        subject  = 'Your Donor Account Has Been Approved — LifeServe',
        message  = f"""Dear {donor.full_name},

We are pleased to inform you that your donor account on LifeServe Blood Bank has been approved.

You can now log in and submit blood donation requests. Your contribution helps save lives every day.

Account Details:
- Username: {donor.username}
- Blood Group: {donor.blood_group}

Thank you for being a lifesaver.

Warm regards,
LifeServe Blood Bank Team""",
        recipient_email = donor.email
    )
    messages.success(request, f'{donor.username} approved successfully.')
    return redirect('admin_donors')

def delete_donor(request, pk):
    if request.session.get('user') != 'admin':
        return redirect('login')
    donor = get_object_or_404(DonorProfile, pk=pk)
    donor.delete()
    messages.success(request, 'Donor deleted.')
    return redirect('admin_donors')

def edit_donor(request, pk):
    if request.session.get('user') != 'admin':
        return redirect('login')
    donor = get_object_or_404(DonorProfile, pk=pk)
    if request.method == 'POST':
        donor.full_name   = request.POST.get('full_name')
        donor.email       = request.POST.get('email')
        donor.phone       = request.POST.get('phone')
        donor.blood_group = request.POST.get('blood_group')
        donor.age         = request.POST.get('age')
        donor.weight      = request.POST.get('weight')
        donor.address     = request.POST.get('address')
        donor.save()
        messages.success(request, 'Donor profile updated.')
        return redirect('admin_donors')
    return render(request, 'edit_donor.html', {'donor': donor})

def reject_donor(request, pk):
    if request.session.get('user') != 'admin':
        return redirect('login')
    donor = get_object_or_404(DonorProfile, pk=pk)
    send_email(
        subject  = 'Your Donor Account Application — LifeServe',
        message  = f"""Dear {donor.full_name},

Thank you for registering on LifeServe Blood Bank.

After reviewing your application, we regret to inform you that your donor account could not be approved at this time.

This may be due to eligibility criteria or incomplete information. You are welcome to register again with updated details.

If you have any questions, please contact us.

Warm regards,
LifeServe Blood Bank Team""",
        recipient_email = donor.email
    )
    donor.delete()
    messages.success(request, 'Donor rejected and removed.')
    return redirect('admin_donors')

def admin_patients(request):
    if request.session.get('user') != 'admin':
        return redirect('login')
    patients = PatientProfile.objects.all().order_by('-created_at')
    return render(request, 'admin_patients.html', {'patients': patients})

def delete_patient(request, pk):
    if request.session.get('user') != 'admin':
        return redirect('login')
    patient = get_object_or_404(PatientProfile, pk=pk)
    patient.delete()
    messages.success(request, 'Patient deleted.')
    return redirect('admin_patients')

def edit_patient(request, pk):
    if request.session.get('user') != 'admin':
        return redirect('login')
    patient = get_object_or_404(PatientProfile, pk=pk)
    if request.method == 'POST':
        patient.full_name   = request.POST.get('full_name')
        patient.email       = request.POST.get('email')
        patient.phone       = request.POST.get('phone')
        patient.blood_group = request.POST.get('blood_group')
        patient.age         = request.POST.get('age')
        patient.doctor_name = request.POST.get('doctor_name')
        patient.hospital    = request.POST.get('hospital')
        patient.address     = request.POST.get('address')
        patient.save()
        messages.success(request, 'Patient profile updated.')
        return redirect('admin_patients')
    return render(request, 'edit_patient.html', {'patient': patient})

def admin_blood_stock(request):
    if request.session.get('user') != 'admin':
        return redirect('login')
    stocks = BloodStock.objects.all().order_by('blood_group')
    return render(request, 'admin_blood_stock.html', {'stocks': stocks})

def update_blood_stock(request):
    if request.session.get('user') != 'admin':
        return redirect('login')
    if request.method == 'POST':
        blood_group = request.POST.get('blood_group')
        units       = request.POST.get('units')
        action      = request.POST.get('action')
        stock, created = BloodStock.objects.get_or_create(blood_group=blood_group)
        if action == 'add':
            stock.units += int(units)
        elif action == 'set':
            stock.units = int(units)
        stock.save()
        messages.success(request, f'Blood stock for {blood_group} updated.')
    return redirect('admin_blood_stock')

def admin_blood_requests(request):
    if request.session.get('user') != 'admin':
        return redirect('login')
    requests_list = BloodRequest.objects.all().order_by('-date_requested')
    return render(request, 'admin_blood_requests.html', {'requests': requests_list})

def handle_blood_request(request, pk, action):
    if request.session.get('user') != 'admin':
        return redirect('login')
    blood_req = get_object_or_404(BloodRequest, pk=pk)
    if action == 'approve':
        stock = BloodStock.objects.filter(blood_group=blood_req.blood_group).first()
        if stock and stock.units >= blood_req.units_needed:
            stock.units -= blood_req.units_needed
            stock.save()
            blood_req.status = 'Approved'
            patient = PatientProfile.objects.filter(username=blood_req.patient_username).first()
            if patient:
                send_email(
                    subject  = 'Your Blood Request Has Been Approved — LifeServe',
                    message  = f"""Dear {patient.full_name},

We are pleased to inform you that your blood request has been approved.

Request Details:
- Blood Group: {blood_req.blood_group}
- Units: {blood_req.units_needed}
- Hospital: {blood_req.hospital}
- Doctor: {blood_req.doctor_name}

Please contact your hospital to proceed with the next steps.

Wishing you a speedy recovery.

Warm regards,
LifeServe Blood Bank Team""",
                    recipient_email = patient.email
                )
            messages.success(request, 'Blood request approved and stock updated.')
        else:
            messages.error(request, 'Not enough blood stock to approve this request.')
            return redirect('admin_blood_requests')
    elif action == 'reject':
        blood_req.status = 'Rejected'
        patient = PatientProfile.objects.filter(username=blood_req.patient_username).first()
        if patient:
            send_email(
                subject  = 'Update on Your Blood Request — LifeServe',
                message  = f"""Dear {patient.full_name},

We regret to inform you that your blood request could not be fulfilled at this time.

Request Details:
- Blood Group: {blood_req.blood_group}
- Units Requested: {blood_req.units_needed}

This may be due to insufficient stock. Please contact your hospital and try again or reach out to us directly for urgent assistance.

We apologize for the inconvenience.

Warm regards,
LifeServe Blood Bank Team""",
                recipient_email = patient.email
            )
        messages.success(request, 'Blood request rejected.')
    blood_req.save()
    return redirect('admin_blood_requests')


def admin_donation_requests(request):
    if request.session.get('user') != 'admin':
        return redirect('login')
    donations = DonationRequest.objects.all().order_by('-date_requested')
    return render(request, 'admin_donation_requests.html', {'donations': donations})

def handle_donation_request(request, pk, action):
    if request.session.get('user') != 'admin':
        return redirect('login')
    donation = get_object_or_404(DonationRequest, pk=pk)
    if action == 'approve':
        stock, created = BloodStock.objects.get_or_create(blood_group=donation.blood_group)
        stock.units += donation.units
        stock.save()
        donation.status = 'Approved'
        from datetime import date
        donor = DonorProfile.objects.filter(username=donation.donor_username).first()
        if donor:
            donor.last_donated = date.today()
            donor.save()
            send_email(
                subject  = 'Thank You for Your Donation — LifeServe',
                message  = f"""Dear {donor.full_name},

Thank you for your generous blood donation. Your contribution makes a real difference.

Donation Details:
- Blood Group: {donation.blood_group}
- Units Donated: {donation.units}
- Date: {date.today().strftime('%d %B %Y')}

Your donation has been added to our blood stock and will help save lives.

You are a true hero.

Warm regards,
LifeServe Blood Bank Team""",
                recipient_email = donor.email
            )
        messages.success(request, 'Donation approved and stock updated.')
    elif action == 'reject':
        donation.status = 'Rejected'
        donor = DonorProfile.objects.filter(username=donation.donor_username).first()
        if donor:
            send_email(
                subject  = 'Update on Your Donation Request — LifeServe',
                message  = f"""Dear {donor.full_name},

Thank you for your willingness to donate blood.

Unfortunately, your donation request could not be accepted at this time. This may be due to eligibility or scheduling reasons.

We encourage you to try again after some time. Your generosity is truly appreciated.

Warm regards,
LifeServe Blood Bank Team""",
                recipient_email = donor.email
            )
        messages.success(request, 'Donation rejected.')
    donation.save()
    return redirect('admin_donation_requests')

# ─── DONOR & PATIENT ───────────────────────────────────────

def donor_dashboard(request):
    if request.session.get('user') != 'donor':
        return redirect('login')
    username = request.session.get('username')
    donor = DonorProfile.objects.get(username=username)
    return render(request, 'donor_dashboard.html', {'donor': donor})

def patient_dashboard(request):
    if request.session.get('user') != 'patient':
        return redirect('login')
    username = request.session.get('username')
    patient  = PatientProfile.objects.get(username=username)
    my_requests = BloodRequest.objects.filter(patient_username=username).order_by('-date_requested')
    context = {
        'patient'            : patient,
        'total_requests'     : my_requests.count(),
        'pending_requests'   : my_requests.filter(status='Pending').count(),
        'approved_requests'  : my_requests.filter(status='Approved').count(),
        'rejected_requests'  : my_requests.filter(status='Rejected').count(),
        'recent_requests'    : my_requests[:5],
        'blood_stock'        : BloodStock.objects.all(),
    }
    return render(request, 'patient_dashboard.html', context)

def request_blood(request):
    if request.session.get('user') != 'patient':
        return redirect('login')
    username = request.session.get('username')
    patient  = PatientProfile.objects.get(username=username)
    if request.method == 'POST':
        blood_group  = request.POST.get('blood_group')
        units_needed = request.POST.get('units_needed')
        urgency      = request.POST.get('urgency')
        reason       = request.POST.get('reason')
        doctor_name  = request.POST.get('doctor_name')
        hospital     = request.POST.get('hospital')

        BloodRequest.objects.create(
            patient_username = username,
            blood_group      = blood_group,
            units_needed     = units_needed,
            urgency          = urgency,
            reason           = reason,
            doctor_name      = doctor_name,
            hospital         = hospital,
        )
        messages.success(request, 'Blood request submitted successfully!')
        return redirect('my_blood_requests')
    return render(request, 'requests_blood.html', {'patient': patient})

def my_blood_requests(request):
    if request.session.get('user') != 'patient':
        return redirect('login')
    username    = request.session.get('username')
    patient     = PatientProfile.objects.get(username=username)
    my_requests = BloodRequest.objects.filter(patient_username=username).order_by('-date_requested')
    return render(request, 'my_blood_requests.html', {'patient': patient, 'requests': my_requests})

def patient_profile(request):
    if request.session.get('user') != 'patient':
        return redirect('login')
    username = request.session.get('username')
    patient  = PatientProfile.objects.get(username=username)
    if request.method == 'POST':
        patient.full_name   = request.POST.get('full_name')
        patient.email       = request.POST.get('email')
        patient.phone       = request.POST.get('phone')
        patient.address     = request.POST.get('address')
        patient.doctor_name = request.POST.get('doctor_name')
        patient.hospital    = request.POST.get('hospital')
        patient.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('patient_profile')
    return render(request, 'patient_profile.html', {'patient': patient})

# ─── DONOR VIEWS ───────────────────────────────────────────

def donor_dashboard(request):
    if request.session.get('user') != 'donor':
        return redirect('login')
    username  = request.session.get('username')
    donor     = DonorProfile.objects.get(username=username)
    my_donations = DonationRequest.objects.filter(donor_username=username).order_by('-date_requested')
    context = {
        'donor'               : donor,
        'total_donations'     : my_donations.count(),
        'pending_donations'   : my_donations.filter(status='Pending').count(),
        'approved_donations'  : my_donations.filter(status='Approved').count(),
        'rejected_donations'  : my_donations.filter(status='Rejected').count(),
        'recent_donations'    : my_donations[:5],
        'blood_stock'         : BloodStock.objects.all(),
    }
    return render(request, 'donor_dashboard.html', context)

def submit_donation(request):
    if request.session.get('user') != 'donor':
        return redirect('login')
    username = request.session.get('username')
    donor    = DonorProfile.objects.get(username=username)
    if request.method == 'POST':
        blood_group = request.POST.get('blood_group')
        units       = request.POST.get('units')

        DonationRequest.objects.create(
            donor_username = username,
            blood_group    = blood_group,
            units          = units,
        )
        messages.success(request, 'Donation request submitted successfully!')
        return redirect('my_donations')
    return render(request, 'submit_donation.html', {'donor': donor})

def my_donations(request):
    if request.session.get('user') != 'donor':
        return redirect('login')
    username     = request.session.get('username')
    donor        = DonorProfile.objects.get(username=username)
    my_donations = DonationRequest.objects.filter(donor_username=username).order_by('-date_requested')
    return render(request, 'my_donations.html', {'donor': donor, 'donations': my_donations})

def donor_profile(request):
    if request.session.get('user') != 'donor':
        return redirect('login')
    username = request.session.get('username')
    donor    = DonorProfile.objects.get(username=username)
    if request.method == 'POST':
        donor.full_name = request.POST.get('full_name')
        donor.email     = request.POST.get('email')
        donor.phone     = request.POST.get('phone')
        donor.address   = request.POST.get('address')
        donor.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('donor_profile')
    return render(request, 'donor_profile.html', {'donor': donor})

@api_view(['GET'])
def api_donors(request):
    donors = DonorProfile.objects.all()
    serializer = DonorSerializer(donors, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def api_patients(request):
    patients = PatientProfile.objects.all()
    serializer = PatientSerializer(patients, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def api_blood_stock(request):
    stock = BloodStock.objects.all()
    serializer = BloodStockSerializer(stock, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def api_blood_requests(request):
    requests = BloodRequest.objects.all()
    serializer = BloodRequestSerializer(requests, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def api_donation_requests(request):
    donations = DonationRequest.objects.all()
    serializer = DonationRequestSerializer(donations, many=True)
    return Response(serializer.data)

def donor_change_password(request):
    if request.session.get('user') != 'donor':
        return redirect('login')
    username = request.session.get('username')
    donor    = DonorProfile.objects.get(username=username)
    if request.method == 'POST':
        current = request.POST.get('current_password')
        new     = request.POST.get('new_password')
        confirm = request.POST.get('confirm_password')
        if donor.password != current:
            messages.error(request, 'Current password is incorrect.')
            return redirect('donor_change_password')
        if new != confirm:
            messages.error(request, 'New passwords do not match.')
            return redirect('donor_change_password')
        if len(new) < 6:
            messages.error(request, 'Password must be at least 6 characters.')
            return redirect('donor_change_password')
        donor.password = new
        donor.save()
        messages.success(request, 'Password changed successfully!')
        return redirect('donor_dashboard')
    return render(request, 'change_password.html', {'user': donor, 'back_url': '/donor-dashboard/'})

def patient_change_password(request):
    if request.session.get('user') != 'patient':
        return redirect('login')
    username = request.session.get('username')
    patient  = PatientProfile.objects.get(username=username)
    if request.method == 'POST':
        current = request.POST.get('current_password')
        new     = request.POST.get('new_password')
        confirm = request.POST.get('confirm_password')
        if patient.password != current:
            messages.error(request, 'Current password is incorrect.')
            return redirect('patient_change_password')
        if new != confirm:
            messages.error(request, 'New passwords do not match.')
            return redirect('patient_change_password')
        if len(new) < 6:
            messages.error(request, 'Password must be at least 6 characters.')
            return redirect('patient_change_password')
        patient.password = new
        patient.save()
        messages.success(request, 'Password changed successfully!')
        return redirect('patient_dashboard')
    return render(request, 'change_password.html', {'user': patient, 'back_url': '/patient-dashboard/'})

def forgot_password(request):
    if request.method == 'POST':
        username    = request.POST.get('username')
        email       = request.POST.get('email')
        new_password    = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('forgot_password')
        if len(new_password) < 6:
            messages.error(request, 'Password must be at least 6 characters.')
            return redirect('forgot_password')

        # Check donor
        donor = DonorProfile.objects.filter(username=username, email=email).first()
        if donor:
            donor.password = new_password
            donor.save()
            messages.success(request, 'Password reset successfully! Please login.')
            return redirect('login')

        # Check patient
        patient = PatientProfile.objects.filter(username=username, email=email).first()
        if patient:
            patient.password = new_password
            patient.save()
            messages.success(request, 'Password reset successfully! Please login.')
            return redirect('login')

        messages.error(request, 'No account found with this username and email.')
    return render(request, 'forgot_password.html')

def send_email(request):
    try:
        send_mail(
            'Lifeserve Blood Bank',
            'your request for blood is accepted...',
            'anothera2914@gmail.com',
            ['anothera2914@gmail.com'],
            fail_silently=False,
        )
        return HttpResponse("Email Sent ✅")
    except Exception as e:
        return HttpResponse(f"Error: {e}")


   
