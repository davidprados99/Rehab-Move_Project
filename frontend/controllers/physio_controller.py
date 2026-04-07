
from PySide6.QtWidgets import  QDialog, QTableWidgetItem, QMessageBox
from PySide6.QtCore import Qt
from controllers.appointment_controller import AppointmentController
from views.physio_dashboard import PhysioDashboard
from views.add_patient_dialog import AddPatientDialog

class PhysioController:

    def __init__(self, api_client):
        self.api = api_client
        self.view = PhysioDashboard(self.api)

        self.view.btn_exercises.clicked.connect(self.handle_dashboard_exercises)
        self.view.btn_add.clicked.connect(self.handle_add_patient)
        self.view.btn_delete.clicked.connect(self.handle_delete_patient)
        self.view.btn_appointments.clicked.connect(self.handle_appointments)
        self.view.btn_pain_records.clicked.connect(self.handle_pain_records)
        self.view.btn_exercise_plan.clicked.connect(self.handle_exercises_assigned)
        self.view.btn_logout.clicked.connect(self.close_sesion)
        self.load_patients()

    def load_patients(self):
            id_physio = self.api.user_id  # Assuming the user role contains the physio ID, adjust as needed
            success, patients = self.api.get_patients(id_physio=id_physio)
            if success:
                self.view.table.setRowCount(0)  # Clear existing rows

                for row_number, patient in enumerate(patients):
                    self.view.table.insertRow(row_number)
                    self.view.table.setItem(row_number, 0, QTableWidgetItem(str(patient.get("id_patient"))))
                    self.view.table.setItem(row_number, 1, QTableWidgetItem(patient.get("name", "N/A")))
                    self.view.table.setItem(row_number, 2, QTableWidgetItem(patient.get("surnames", "N/A")))
                    self.view.table.setItem(row_number, 3, QTableWidgetItem(patient.get("mail", "N/A")))
                    self.view.table.setItem(row_number, 4, QTableWidgetItem(patient.get("start_date", "N/A")))

                    self.view.table.item(row_number, 0).setTextAlignment(Qt.AlignCenter)
            else:
                print(f"Error al cargar pacientes: {patients}")
                QMessageBox.critical(self.view, "Error", f"No se pudieron cargar los pacientes: {patients}")
    
    def handle_dashboard_exercises(self):
        # Logic to open the exercise management dialog and handle the process
        pass

    def handle_add_patient(self):
            dialog = AddPatientDialog()
            if dialog.exec() == QDialog.Accepted:
                patient_data = dialog.get_data()
                patient_data["id_physio"] = self.api.user_id  # Set the physio ID for the new patient
                success, message = self.api.add_patient(patient_data)
                if success:
                    QMessageBox.information(self.view, "Éxito", "Paciente añadido correctamente.")
                    self.load_patients()  # Refresh the patient list
                else:
                    QMessageBox.critical(self.view, "Error", f"No se pudo añadir el paciente: {message}")

    def handle_delete_patient(self):
        selected_items = self.view.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self.view, "Advertencia", "Por favor, seleccione un paciente para eliminar.")
            return
        
        id_patient = selected_items[0].text()  
        confirm = QMessageBox.question(self.view, "Confirmar Eliminación", f"¿Está seguro de que desea eliminar al paciente con ID {id_patient}?", QMessageBox.Yes | QMessageBox.No)
        
        if confirm == QMessageBox.Yes:
            success, message = self.api.delete_patient(id_patient)
            if success:
                QMessageBox.information(self.view, "Éxito", f"Paciente con ID {id_patient} eliminado correctamente.")
                self.load_patients()
            else:
                QMessageBox.critical(self.view, "Error", f"No se pudo eliminar el paciente: {message}")
    
    def handle_appointments(self):
        self.view.close()  # Close the current dashboard view
        appointment_controller = AppointmentController(self.api)
        appointment_controller.view.show()

    def handle_pain_records(self):
        # Logic to open pain records management dialog and handle the process
        pass

    def handle_exercises_assigned(self):
        # Logic to open exercise management dialog and handle the process
        pass
    
    def close_sesion(self):
        confirm = QMessageBox.question(self.view, "Confirmar Cierre de Sesión", "¿Está seguro de que desea cerrar sesión?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.api.logout()
            self.view.close()