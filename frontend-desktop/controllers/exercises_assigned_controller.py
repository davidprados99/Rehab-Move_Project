from PySide6.QtWidgets import QDialog, QMenu, QTableWidgetItem, QMessageBox
from views.dialogs.add_exercise_assig_dialog import AddExerciseAssigDialog
from views.exercises_assigned_dashboard import ExercisesAssignedDashboard
from views.dialogs.mod_exercise_assig_dialog import ModExerciseAssigDialog
from PySide6.QtCore import Qt

class ExercisesAssignedController:
    def __init__(self, api, id_patient):
        self.api = api
        self.id_patient = id_patient
        self.view = ExercisesAssignedDashboard(api, id_patient)
        self.view.showMaximized()

        self.view.btn_assign_exercise.clicked.connect(self.handle_assign_exercise)
        self.view.btn_edit_exercise.clicked.connect(self.handle_edit_exercise_assign)
        self.view.btn_delete_exercise_assign.clicked.connect(self.handle_delete_exercise_assign)
        self.view.btn_back.clicked.connect(self.go_back)
        self.load_exercises_assigned()
        self.view.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.view.table.customContextMenuRequested.connect(self.show_context_menu)

    def load_exercises_assigned(self):
        success, exercises = self.api.get_exercise_assignments(self.id_patient)

        if success:
            self.view.table.setRowCount(0)  # Clear existing rows

            for row_number, exercise_assign in enumerate(exercises):
                exercise_name = exercise_assign.get("exercise", {}).get("name", "N/A") if exercise_assign.get("exercise") else "N/A"
                self.view.table.insertRow(row_number)
                self.view.table.setItem(row_number, 0, QTableWidgetItem(str(exercise_assign.get("id_assignment"))))
                self.view.table.setItem(row_number, 1, QTableWidgetItem(str(exercise_assign.get("weekly_frequency", "N/A"))))
                self.view.table.setItem(row_number, 2, QTableWidgetItem(str(exercise_assign.get("series", "N/A"))))
                self.view.table.setItem(row_number, 3, QTableWidgetItem(str(exercise_assign.get("repetitions", "N/A"))))
                self.view.table.setItem(row_number, 4, QTableWidgetItem(str(exercise_assign.get("start_date", "N/A"))))
                self.view.table.setItem(row_number, 5, QTableWidgetItem(str(exercise_assign.get("end_date", "N/A"))))
                self.view.table.setItem(row_number, 6, QTableWidgetItem(str(exercise_name)))

                for column in range(7):
                    self.view.table.item(row_number, column).setTextAlignment(Qt.AlignCenter)
                
        else:
            QMessageBox.critical(self.view, "Error", f"No se pudieron cargar los ejercicios: {exercises}")
    
    def handle_assign_exercise(self):
        dialog = AddExerciseAssigDialog(self.api)
        dialog.load_data_api()
        if dialog.exec() == QDialog.Accepted:
            assignment_data = dialog.get_data()
            success, message = self.api.create_exercise_assignment(assignment_data)
            if success:
                QMessageBox.information(self.view, "Éxito", "Ejercicio asignado correctamente.")
                self.load_exercises_assigned()
            else:
                QMessageBox.critical(self.view, "Error", f"No se pudo asignar el ejercicio: {message}")
    
    def handle_edit_exercise_assign(self):
        selected_items = self.view.table.selectedItems() if self.view.table.selectedItems() else []
        id_exercise_assignment = selected_items[0].text() if selected_items else None
        if not selected_items:
            QMessageBox.warning(self.view, "Advertencia", "Por favor, seleccione un ejercicio asignado para editar.")
            return
        dialog = ModExerciseAssigDialog(self.api)
        dialog.load_data_api()
        if dialog.exec() == QDialog.Accepted:
            exercise_data = dialog.get_data()
            final_data = {k: v for k, v in exercise_data.items() if v}  # Filter out empty values
            final_data["id_exercise"] = id_exercise_assignment # Set the exercise ID for the update
            success, message = self.api.update_exercise_assignment(id_exercise_assignment, final_data)
            if success:
                QMessageBox.information(self.view, "Éxito", "Ejercicio modificado correctamente.")
                self.load_exercises_assigned()  # Refresh the exercise list
            else:
                QMessageBox.critical(self.view, "Error", f"No se pudo modificar el ejercicio: {message}")

    
    def handle_delete_exercise_assign(self):
        selected_items = self.view.table.selectedItems() if self.view.table.selectedItems() else []
        id_exercise_assignment = selected_items[0].text() if selected_items else None
        if not selected_items:
            QMessageBox.warning(self.view, "Advertencia", "Por favor, seleccione un ejercicio asignado para eliminar.")
            return
        confirm = QMessageBox.question(self.view, "Confirmar Eliminación", f"¿Está seguro de que desea eliminar el ejercicio asignado con ID {id_exercise_assignment}?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            success, message = self.api.delete_exercise_assignment(id_exercise_assignment)
            if success:
                QMessageBox.information(self.view, "Éxito", f"Ejercicio asignado con ID {id_exercise_assignment} eliminado correctamente.")
                self.load_exercises_assigned()  # Refresh the list after deletion
            else:
                QMessageBox.critical(self.view, "Error", f"No se pudo eliminar el ejercicio: {message}")


    def go_back(self):
        self.view.close()
        from controllers.physio_controller import PhysioController
        self.physio_controller = PhysioController(self.api)
        self.physio_controller.view.showMaximized()

    def show_context_menu(self, pos):
        menu = QMenu(self.view)

        menu.addAction("Editar", self.handle_edit_exercise_assign)
        menu.addAction("Eliminar", self.handle_delete_exercise_assign)
        
        # If the user right-clicks outside of any valid row, we should not show the context menu
        index = self.view.table.indexAt(pos)
        if not index.isValid():
            return 

        global_pos = self.view.table.viewport().mapToGlobal(pos)
        menu.exec(global_pos)