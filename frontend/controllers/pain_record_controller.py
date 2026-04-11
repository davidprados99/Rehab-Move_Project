from PySide6.QtWidgets import  QDialog, QMenu, QTableWidgetItem, QMessageBox
from PySide6.QtCore import Qt
from views.pain_record_view import PainRecordView

class PainRecordController:
    def __init__(self, api_client, id_patient):
        self.api = api_client
        self.id_patient = id_patient
        self.view = PainRecordView(api_client, id_patient)
        self.view.btn_back.clicked.connect(self.go_back)
    
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
        