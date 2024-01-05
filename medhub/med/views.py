# med/views.py
from django.shortcuts import render, redirect, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist  # Import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from django.http import HttpResponse, Http404

from .models import Patients, Disease, Doctor, Patient, Appointment, ColdDisease, FluDisease  # Import other disease classes as needed
from .forms import AppointmentForm, NewPatientForm, DoctorVerificationForm
from .observers import AppointmentObserver
from .utils import DatabaseConnection
from .iterator_pattern import PatientHistory
from .command_pattern import RemovePatientCommand, RemoveAppointmentCommand

observer = AppointmentObserver()
database_connection = DatabaseConnection()
patient_history = PatientHistory()

def home(request):
    # Call the correct method to get the status
    connection_status = database_connection.get_connection_status()
    
    # Fetch some data from the database (example: fetching all doctors)
    doctors = Doctor.objects.all()
    
    try:
        # Example: Fetching the latest appointment
        latest_appointment = Appointment.objects.latest('date')
    except ObjectDoesNotExist:
        latest_appointment = None  # Handle the case where no appointments exist
    
    return render(request, 'home.html', {
        'connection_status': connection_status,
        'doctors': doctors,
        'latest_appointment': latest_appointment,
    })
    
def doctor_directory(request):
    doctors = Doctor.objects.all()
    return render(request, 'doctor_directory.html', {'doctors': doctors})

def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'patient_list.html', {'patients': patients})

def appointment_list(request):
    # Fetch all doctors
    doctors = Doctor.objects.all()

    # Create a dictionary to store appointments for each doctor
    doctor_appointments = {doctor: [] for doctor in doctors}

    # Fetch all appointments along with related doctor and patient information
    appointments = Appointment.objects.select_related('doctor', 'patient').all()

    # Organize appointments by doctor
    for appointment in appointments:
        doctor_appointments[appointment.doctor].append(appointment)

    return render(request, 'appointment_list.html', {'doctor_appointments': doctor_appointments})

def schedule_appointment(request):
    doctors = Doctor.objects.all()

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            doctor = form.cleaned_data['doctor']
            patient_name = form.cleaned_data['patient_name']
            patient_age = form.cleaned_data['patient_age']
            patient_email = form.cleaned_data['patient_email']
            date = form.cleaned_data['date']
            time = form.cleaned_data['time']

            # Create or get the patient from the database
            patient, created = Patient.objects.get_or_create(
                doctor=doctor,  # Add the associated doctor
                name=patient_name,
                age=patient_age,
                email=patient_email,
            )

            # Create the appointment in the database
            appointment = Appointment.objects.create(
                doctor=doctor,
                patient=patient,
                date=date,
                time=time,
            )

            # Notify observers
            observer.update(appointment)

            # Add success message
            messages.success(request, 'Appointment scheduled successfully.')

            # Redirect to a success page or any other desired page
            return redirect('appointment_list')
    else:
        form = AppointmentForm()

    return render(request, 'schedule_appointment.html', {'form': form, 'doctors': doctors})

def doctor_verification(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Custom authentication
        doctor = authenticate_doctor(username, password)

        if doctor is not None:
            # Login the doctor (using Django's built-in login method)
            request.session['doctor_id'] = doctor.id
            messages.success(request, f"Welcome, Dr. {doctor.name}!")
            return redirect('doctor_home')  # Replace with your actual URL

        # Invalid username or password
        error_message = 'Invalid username or password. Please try again.'
        messages.error(request, error_message)
        return render(request, 'doctor_verification.html', {'error_message': error_message})

    return render(request, 'doctor_verification.html')

def authenticate_doctor(username, password):
    try:
        doctor = Doctor.objects.get(username=username, password=password)
        return doctor
    except Doctor.DoesNotExist:
        return None

@login_required(login_url='doctor_login')
def doctor_home(request):
    # Retrieve the logged-in doctor
    doctor_id = request.session.get('doctor_id')
    if doctor_id is not None:
        doctor = Doctor.objects.get(id=doctor_id)
        return render(request, 'doctor_home.html', {'doctor_name': doctor.name})
    else:
        # Redirect to the login page if not logged in
        return redirect('doctor_login')

@login_required(login_url='doctor_login')
def doctor_patient_list(request):
    # Retrieve the logged-in doctor
    doctor = Doctor.objects.get(id=request.session['doctor_id'])

    patients = Patients.objects.filter(doctor=doctor)
    return render(request, 'doctor_patient_list.html', {'patients': patients})

@login_required(login_url='doctor_login')
def doctor_appointment_list(request):
    # Retrieve the logged-in doctor
    doctor_id = request.session.get('doctor_id')

    if doctor_id is not None:
        try:
            doctor = Doctor.objects.get(id=doctor_id)
            # Fetch the list of appointments assigned to the logged-in doctor
            appointments = Appointment.objects.filter(doctor=doctor)
            return render(request, 'doctor_appointment_list.html', {'appointments': appointments})
        except Doctor.DoesNotExist:
            # Handle the case where the doctor is not found
            return render(request, 'error.html', {'message': 'Doctor not found'})
    else:
        # Redirect to the login page if not logged in
        return redirect('doctor_verification')

@login_required(login_url='doctor_login')
def new_patient(request):
    if request.method == 'POST':
        form = NewPatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            
            # Retrieve the logged-in doctor
            doctor = Doctor.objects.get(id=request.session['doctor_id'])

            # Associate the patient with the doctor
            patient.doctor = doctor
            patient.save()

            # Process diseases
            diseases = request.POST.getlist('diseases')
            patient.diseases.set(diseases)

            return redirect('doctor_patient_list')

    else:
        form = NewPatientForm()

    return render(request, 'new_patient.html', {'form': form})
    
@user_passes_test(lambda u: u.is_superuser, login_url='home')
def admin_patient_history(request):
    patient_history = PatientHistory()
    patient_iterator = patient_history.create_iterator()
    patient_records = list(patient_iterator)
    return render(request, 'admin_patient_history.html', {'patient_records': patient_records})

@login_required(login_url='doctor_login')
def remove_patient(request, patient_id):
    # Assuming the doctor is associated with the logged-in user
    doctor = Doctor.objects.get(id=request.session['doctor_id'])

    # Retrieve the patient from the doctor's patient list
    patient = get_object_or_404(Patients, id=patient_id, doctor=doctor)

    # Delete the patient
    patient.delete()

    return redirect('doctor_patient_list')

def remove_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    remove_appointment_command = RemoveAppointmentCommand(appointment)
    remove_appointment_command.execute()
    return redirect('appointment_list')
