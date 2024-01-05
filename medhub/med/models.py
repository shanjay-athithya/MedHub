# med/models.py
from django.db import models
from django.contrib.auth.models import User

class Doctor(models.Model):
    username = models.CharField(default='unique_default_value', max_length=50, unique=True)
    password = models.CharField(default='t1o2u3r4', max_length=50)
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Patient(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.name

class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    # Add more fields as needed

    def __str__(self):
        return f"{self.patient.name}'s appointment with Dr. {self.doctor.name} on {self.date} at {self.time}"

class Disease(models.Model):
    name = models.CharField(max_length=255)

    def apply_to_patient(self, patient):
        pass

class Patients(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    diseases = models.ManyToManyField(Disease)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)  # Add null=True here

    def add_disease(self, disease):
        disease.apply_to_patient(self)

class ColdDisease(Disease):
    def apply_to_patient(self, patient):
        patient.diseases.add(self)

class FluDisease(Disease):
    def apply_to_patient(self, patient):
        patient.diseases.add(self)
        
class BloodPressureDisease(Disease):
    def apply_to_patient(self, patient):
        patient.diseases.add(self)

class HerniaDisease(Disease):
    def apply_to_patient(self, patient):
        patient.diseases.add(self)
        
class PatientHistoryIterator:
    def __init__(self, patient_records):
        self.patient_records = patient_records
        self.index = 0

    def has_next(self):
        return self.index < len(self.patient_records)

    def next(self):
        if self.has_next():
            patient_record = self.patient_records[self.index]
            self.index += 1
            return patient_record
        else:
            raise StopIteration
