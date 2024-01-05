"""# iterator_pattern.py

class Iterator:
    def next(self):
        pass

    def has_next(self):
        pass

class Aggregate:
    def create_iterator(self):
        pass

class PatientHistoryIterator(Iterator):
    def __init__(self, patient_records):
        self.patient_records = patient_records
        self.index = 0

    def next(self):
        if self.has_next():
            patient = self.patient_records[self.index]
            self.index += 1
            return patient
        else:
            return None

    def has_next(self):
        return self.index < len(self.patient_records)

class PatientHistory(Aggregate):
    def __init__(self):
        self.patient_records = []

    def add_patient_record(self, patient_record):
        self.patient_records.append(patient_record)

    def create_iterator(self):
        return PatientHistoryIterator(self.patient_records)
"""
# iterator_pattern.py
from .models import Patients

# iterator_pattern.py

class PatientHistoryIterator:
    def __init__(self, patient_records):
        self.patient_records = patient_records
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.patient_records):
            patient = self.patient_records[self.index]
            self.index += 1
            return patient
        else:
            raise StopIteration

class PatientHistory:
    def __init__(self):
        # Fetch all patients from the database during initialization
        self.patient_records = list(Patients.objects.all())

    def create_iterator(self):
        return PatientHistoryIterator(self.patient_records)
