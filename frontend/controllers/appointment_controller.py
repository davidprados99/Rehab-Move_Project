from PySide6.QtWidgets import  QCalendarWidget, QDialog, QTableWidgetItem, QMessageBox
from PySide6.QtCore import Qt
from views.dialogs.add_appt_dialog import AddApptDialog
from views.dialogs.hour_selection_dialog import HourSelectionDialog
from views.appointment_view import AppointmentView

class AppointmentController:
    def __init__(self, api_client):
        self.api = api_client
        self.view = AppointmentView(self.api)
        self.all_appointments = []  # Appointments cache
        self.role_handle()
        self.load_appointments()
        self.view.calendar.clicked.connect(self.handle_date_clicked)
        self.view.btn_back.clicked.connect(self.go_back)

    def role_handle(self):
        if self.api.user_role != "physio":
            self.view.calendar.setSelectionMode(QCalendarWidget.NoSelection)  
        else:
            self.view.calendar.setSelectionMode(QCalendarWidget.SingleSelection) 

    def go_back(self):
        self.view.close()
        # Logic to return to the previous dashboard (physio or patient) based on user role
        if self.api.user_role == "physio":
            from controllers.physio_controller import PhysioController
            self.physio_controller = PhysioController(self.api)
            self.physio_controller.view.show()
        else:
            from controllers.patient_controller import PatientController
            self.patient_controller = PatientController(self.api)
            self.patient_controller.view.show()
    
    def load_appointments(self):
        id_user = self.api.user_id
        success, appointments = self.api.get_appointments(id=id_user)
        if success:
            self.all_appointments = appointments  # Update the cache
            self.view.update_calendar_markers(appointments)
        else:
            print(f"Error al cargar citas: {appointments}")
            QMessageBox.critical(self.view, "Error", f"No se pudieron cargar las citas: {appointments}")
    
    def handle_date_clicked(self, qdate):
        # Only physios can manage appointments
        if self.api.user_role != "physio":
            return
        
        date_iso = qdate.toString("yyyy-MM-dd")
        appts_today = [a for a in self.all_appointments if a["date"].startswith(date_iso)]

        # Open the dialog
        dialog = HourSelectionDialog(qdate, appts_today, self.view)
        if dialog.exec() == QDialog.Accepted:
            if dialog.action_type == "ADD":
                self.open_add_appointment_form(qdate, dialog.selected_hour)
            elif dialog.action_type == "DELETE":
                self.confirm_delete_appointment(dialog.appointment_id)

    def open_add_appointment_form(self, qdate, hour_str):
        dialog = AddApptDialog(self.view)
        dialog.date_str = f"{qdate.toString('yyyy-MM-dd')}T{hour_str}:00"  # Set the date for the new appointment
        if dialog.exec() == QDialog.Accepted:
            data = dialog.get_data()
            data["id_physio"] = self.api.user_id  # Set the physio ID to the logged-in user
            success, message = self.api.create_appointment(data)
            if success:
                QMessageBox.information(self.view, "Éxito", "Cita creada exitosamente.")
                self.load_appointments() # Recargar para refrescar colores
            else:
                QMessageBox.critical(self.view, "Error", f"No se pudo crear la cita: {message}")

    def confirm_delete_appointment(self, appt_id):
        reply = QMessageBox.question(self.view, "Confirmar", "¿Deseas eliminar esta cita?", 
                                    QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            success, message = self.api.delete_appointment(appt_id)
            if success:
                QMessageBox.information(self.view, "Éxito", "Cita eliminada.")
                self.load_appointments() # Recargar para refrescar colores
            else:
                QMessageBox.critical(self.view, "Error", message)
