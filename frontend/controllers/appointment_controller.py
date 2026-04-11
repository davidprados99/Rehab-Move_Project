from PySide6.QtWidgets import  QCalendarWidget, QDialog, QTableWidgetItem, QMessageBox
from PySide6.QtCore import Qt
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
        
        if self.api.user_role != "physio":
            self.view.btn_add_appointment.hide()
            self.view.btn_mod_appointment.hide()
            self.view.btn_del_appointment.hide()

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

        date_str = qdate.toString("yyyy-MM-dd")
        
        # Filter appointments of the day from the cache
        appts_today = [a for a in self.all_appointments if date_str in a["date"]]

        # Open the dialog
        dialog = HourSelectionDialog(date_str, appts_today, self.view)
        if dialog.exec() == QDialog.Accepted:
            if dialog.action_type == "ADD":
                self.open_add_appointment_form(date_str, dialog.selected_hour)
            elif dialog.action_type == "DELETE":
                self.confirm_delete_appointment(dialog.appointment_id)

    def open_add_appointment_form(self, date_str, hour_str):
        # TODO - Open a form to select patient and confirm creation of the appointment at the selected date and hour
        pass

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
