from PySide6.QtWidgets import  QDialog, QMenu, QTableWidgetItem, QMessageBox
from PySide6.QtCore import Qt
from controllers.appointment_controller import AppointmentController
from views.physio_dashboard import PhysioDashboard
from views.dialogs.add_patient_dialog import AddPatientDialog
from views.dialogs.mod_patient_dialog import ModPatientDialog
from controllers.pain_record_controller import PainRecordController
from controllers.exercises_controller import ExercisesController
from controllers.exercises_assigned_controller import ExercisesAssignedController

class PhysioController:

    def __init__(self, api_client):
        self.api = api_client
        self.view = PhysioDashboard(self.api)
        self.view.showMaximized()


        self.view.btn_exercises.clicked.connect(self.handle_dashboard_exercises)
        self.view.btn_add.clicked.connect(self.handle_add_patient)
        self.view.btn_mod.clicked.connect(self.handle_mod_patient)
        self.view.btn_delete.clicked.connect(self.handle_delete_patient)
        self.view.btn_appointments.clicked.connect(self.handle_appointments)
        self.view.btn_pain_records.clicked.connect(self.handle_pain_records)
        self.view.btn_assign_exercises.clicked.connect(self.handle_exercises_assigned)
        self.view.btn_logout.clicked.connect(self.close_sesion)
        self.load_patients()

        self.view.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.view.table.customContextMenuRequested.connect(self.show_context_menu)


    def load_patients(self):
            id_physio = self.api.user_id  # Assuming the user role contains the physio ID, adjust as needed
            success, patients = self.api.get_patients_by_physio(id_physio=id_physio)

            if success:
                self.view.table.setRowCount(0)  # Clear existing rows

                for row_number, patient in enumerate(patients):
                    self.view.table.insertRow(row_number)
                    self.view.table.setItem(row_number, 0, QTableWidgetItem(str(patient.get("id_patient"))))
                    self.view.table.setItem(row_number, 1, QTableWidgetItem(patient.get("name", "N/A")))
                    self.view.table.setItem(row_number, 2, QTableWidgetItem(patient.get("surnames", "N/A")))
                    self.view.table.setItem(row_number, 3, QTableWidgetItem(patient.get("email", "N/A")))
                    self.view.table.setItem(row_number, 4, QTableWidgetItem(patient.get("phone","N/A")))
                    self.view.table.setItem(row_number, 5, QTableWidgetItem(patient.get("start_date", "N/A")))

                    for column in range(6):
                        self.view.table.item(row_number, column).setTextAlignment(Qt.AlignCenter)
                
            else:
                QMessageBox.critical(self.view, "Error", f"No se pudieron cargar los pacientes: {patients}")


    def handle_dashboard_exercises(self):
        self.view.close()
        self.exercises_controller = ExercisesController(self.api)


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


    def handle_mod_patient(self):
        selected_items = self.view.table.selectedItems() if self.view.table.selectedItems() else []
        if not selected_items:
            QMessageBox.warning(self.view, "Advertencia", "Por favor, seleccione un paciente para modificar.")
            return
        id_patient = selected_items[0].text()
        
        dialog = ModPatientDialog()
        if dialog.exec() == QDialog.Accepted:
            patient_data = dialog.get_data()
            final_data = {k: v for k, v in patient_data.items() if v}  # Filter out empty values
            final_data["id_patient"] = id_patient  # Set the patient ID for the update
            success, message = self.api.update_patient(id_patient, final_data)
            if success:
                QMessageBox.information(self.view, "Éxito", "Paciente modificado correctamente.")
                self.load_patients()  # Refresh the patient list
            else:
                QMessageBox.critical(self.view, "Error", f"No se pudo modificar el paciente: {message}")


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
        self.view.close()   
        self.appointment_controller = AppointmentController(self.api)
        self.appointment_controller.view.showMaximized()


    def handle_pain_records(self):
        selected_items = self.view.table.selectedItems() if self.view.table.selectedItems() else []
        if not selected_items:
            QMessageBox.warning(self.view, "Advertencia", "Por favor, seleccione un paciente para ver sus registros de dolor.")
            return
        id_patient = selected_items[0].text()
        self.view.close()
        self.pain_record_controller = PainRecordController(self.api, id_patient)
        self.pain_record_controller.view.showMaximized()
    
    def handle_exercises_assigned(self):
        selected_items = self.view.table.selectedItems() if self.view.table.selectedItems() else []
        if not selected_items:
            QMessageBox.warning(self.view, "Advertencia", "Por favor, seleccione un paciente para ver sus ejercicios asignados.")
            return
        id_patient = selected_items[0].text()
        self.view.close()
        self.exercises_assigned_controller = ExercisesAssignedController(self.api, id_patient)
        self.exercises_assigned_controller.view.showMaximized()


    def close_sesion(self):
        confirm = QMessageBox.question(self.view, "Confirmar Cierre de Sesión", "¿Está seguro de que desea cerrar sesión?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.api.logout()
            self.view.close()
    
    def show_context_menu(self, pos):
        menu = QMenu(self.view)

        menu.addAction("Editar", self.handle_mod_patient)
        menu.addAction("Eliminar", self.handle_delete_patient)
        menu.addAction("Ver Registros de Dolor", self.handle_pain_records)
        
        # If the user right-clicks outside of any valid row, we should not show the context menu
        index = self.view.table.indexAt(pos)
        if not index.isValid():
            return 

        global_pos = self.view.table.viewport().mapToGlobal(pos)
        menu.exec(global_pos)