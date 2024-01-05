# command_pattern.py
from abc import ABC, abstractmethod

# Command interface
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

# Concrete command for removing a patient
class RemovePatientCommand(Command):
    def __init__(self, patient):
        self.patient = patient

    def execute(self):
        # Logic to remove the patient (e.g., delete from the database)
        self.patient.delete()

# Concrete command for removing an appointment
class RemoveAppointmentCommand(Command):
    def __init__(self, appointment):
        self.appointment = appointment

    def execute(self):
        # Logic to remove the appointment (e.g., delete from the database)
        self.appointment.delete()
