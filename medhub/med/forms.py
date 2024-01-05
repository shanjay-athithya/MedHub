from django import forms
from .models import Appointment, Doctor, Patients
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomDateInput(forms.DateInput):
    input_type = 'date'

class CustomTimeInput(forms.TimeInput):
    input_type = 'time'

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'time']
        widgets = {
            'date': CustomDateInput(),
            'time': CustomTimeInput(),
        }

    patient_name = forms.CharField(max_length=100, label='Patient Name')
    patient_age = forms.IntegerField(label='Patient Age')
    patient_email = forms.EmailField(label='Patient Email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Update the queryset for the doctor field
        self.fields['doctor'].queryset = Doctor.objects.all()

        # Set custom widgets for date and time fields
        self.fields['date'].widget = CustomDateInput()
        self.fields['time'].widget = CustomTimeInput()

class DoctorCreationForm(UserCreationForm):
    name = forms.CharField(max_length=100, required=True)
    specialty = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'name', 'specialty')
        
class NewPatientForm(forms.ModelForm):
    class Meta:
        model = Patients
        fields = ['name', 'age', 'diseases', 'doctor']

class DoctorVerificationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
