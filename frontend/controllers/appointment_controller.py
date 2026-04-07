from PySide6.QtWidgets import  QDialog, QTableWidgetItem, QMessageBox
from PySide6.QtCore import Qt
from views.appointment_view import AppointmentView



class AppointmentController:
    def __init__(self, api_client):
        self.api = api_client
        self.view = AppointmentView(self.api)
        self.load_future_appointments()
        self.view.btn_back.clicked.connect(self.go_back)

    def go_back(self):
        self.view.close()
        # Logic to return to the previous dashboard (physio or patient) based on user role
        if self.api.user_role == "physio":
            from controllers.physio_controller import PhysioController
            physio_controller = PhysioController(self.api)
            physio_controller.view.show()
        else:
            from controllers.patient_controller import PatientController
            patient_controller = PatientController(self.api)
            patient_controller.view.show()

    def load_future_appointments(self):
        success, appointments = self.api.get_appointments(id=self.api.user_id)
        if success:
            self.view.future_table.setRowCount(0)  # Clear existing rows
            for row_number, appointment in enumerate(appointments):
                self.view.future_table.insertRow(row_number)
                self.view.future_table.setItem(row_number, 0, QTableWidgetItem(appointment.get("date", "N/A")))
                self.view.future_table.setItem(row_number, 1, QTableWidgetItem(appointment.get("patient_name", "N/A")))
                # Add action buttons (e.g., view details, cancel) as needed
        else:
            print(f"Error al cargar citas: {appointments}")
            QMessageBox.critical(self.view, "Error", f"No se pudieron cargar las citas: {appointments}")