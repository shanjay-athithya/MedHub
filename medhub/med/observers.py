# med/observers.py

class AppointmentObserver:
    def update(self, appointment):
        # Implement the logic to send notifications (e.g., emails) here
        print(f"Notification: New appointment scheduled - {appointment}")
