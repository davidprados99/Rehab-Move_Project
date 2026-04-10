from PySide6.QtWidgets import  QCalendarWidget, QDialog, QTableWidgetItem, QMessageBox
from PySide6.QtCore import Qt
from views.appointment_view import AppointmentView

class AppointmentController:
    def __init__(self, api_client):
        self.api = api_client
        self.view = AppointmentView(self.api)
        self.role_handle()
        self.load_appointments()
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
            #TODO - Process appointments and update calendar markers
            pass
        else:
            print(f"Error al cargar citas: {appointments}")
            QMessageBox.critical(self.view, "Error", f"No se pudieron cargar las citas: {appointments}")
