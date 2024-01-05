# med/urls.py
from django.urls import path
from .views import home, doctor_directory, patient_list, appointment_list, schedule_appointment
from .views import doctor_patient_list, doctor_appointment_list,  doctor_verification, doctor_home, new_patient, admin_patient_history
from .views import remove_patient, remove_appointment
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', home, name='home'),
    path('doctor-directory/', doctor_directory, name='doctor_directory'),
    path('admin-patient-history/', admin_patient_history, name='admin_patient_history'),
    path('patient-list/', patient_list, name='patient_list'),
    path('appointment-list/', appointment_list, name='appointment_list'),
    path('schedule-appointment/', schedule_appointment, name='schedule_appointment'),
    path('doctor-home/', doctor_home, name='doctor_home'),
    path('doctor-verification/', doctor_verification, name='doctor_verification'),
    path('doctor/patient-list/', doctor_patient_list, name='doctor_patient_list'),
    path('doctor/appointment-list/', doctor_appointment_list, name='doctor_appointment_list'),
    path('new-patient/', new_patient, name='new_patient'),
    path('remove-patient/<int:patient_id>/', remove_patient, name='remove_patient'),
    path('remove-appointment/<int:appointment_id>/', remove_appointment, name='remove_appointment'),
    path('doctor-login/', LoginView.as_view(template_name='doctor_ verification.html'), name='doctor_login'),

]
