from PySide6.QtWidgets import QDialog, QHBoxLayout, QLabel, QMenu, QTableWidgetItem, QMessageBox, QWidget
from views.dialogs.add_exercise_assig_dialog import AddExerciseAssigDialog
from views.exercises_assigned_dashboard import ExercisesAssignedDashboard
from views.dialogs.mod_exercise_assig_dialog import ModExerciseAssigDialog
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from utils import resource_path

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
        self.load_exercises_done_today()
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
    
    def load_exercises_done_today(self):
        success, exercises_done = self.api.get_exercises_done_today(self.id_patient)
        # This method will mark the exercises that have been done today in the table.
        if success:
            exercises_done_dict = {exercise_done["id_assignment"]: exercise_done for exercise_done in exercises_done}
            for row in range(self.view.table.rowCount()):

                id_assignment = int(self.view.table.item(row, 0).text())

                # Icon for active status
                container = QWidget()  # Create a container widget for the icon
                layout = QHBoxLayout(container)  # Create a horizontal layout for the container

                icon_label = QLabel()  # Create a label to hold the icon
                icon_path = resource_path("assets/done.png") if id_assignment in exercises_done_dict else resource_path("assets/noDone.png")

                original_pixmap = QPixmap(icon_path)
                icon_size = 15 if id_assignment in exercises_done_dict else 10  
                
                dpr = self.view.devicePixelRatioF() # Get the device pixel ratio for high-DPI scaling

                pixmap = original_pixmap.scaled(
                    icon_size * dpr, icon_size * dpr, Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
                icon_label.setPixmap(pixmap)  # Set the pixmap to the label

                layout.addWidget(icon_label)  # Add the label to the layout
                layout.setAlignment(Qt.AlignCenter)  # Center the layout
                layout.setContentsMargins(0, 0, 0, 0)  # Remove margins to fit the icon properly
                self.view.table.setCellWidget(row, 7, container)
        else:
            QMessageBox.critical(self.view, "Error", f"No se pudieron cargar los ejercicios hechos hoy: {exercises_done}")
    
    def handle_assign_exercise(self):
        dialog = AddExerciseAssigDialog(self.api)
        dialog.load_data_api()
        if dialog.exec() == QDialog.Accepted:
            assignment_data = dialog.get_data()
            success, message = self.api.create_exercise_assignment(assignment_data)
            if success:
                QMessageBox.information(self.view, "Éxito", "Ejercicio asignado correctamente.")
                self.load_exercises_assigned()
                self.load_exercises_done_today()
            else:
                QMessageBox.critical(self.view, "Error", f"No se pudo asignar el ejercicio: {message}")
    
    def handle_edit_exercise_assign(self):
        selected_items = self.view.table.selectedItems() if self.view.table.selectedItems() else []
        id_exercise_assignment = selected_items[0].text() if selected_items else None
        if not selected_items:
            QMessageBox.warning(self.view, "Advertencia", "Por favor, seleccione un ejercicio asignado para editar.")
            return
        exercise_assignment_data = {
            "id_patient": self.id_patient,
            "name_exercise": selected_items[6].text(),
            "weekly_frequency": selected_items[1].text(),
            "series": selected_items[2].text(),
            "repetitions": selected_items[3].text(),
            "start_date": selected_items[4].text(),
            "end_date": selected_items[5].text()
        }
        dialog = ModExerciseAssigDialog(self.api, exercise_assignment_data=exercise_assignment_data)
        if dialog.exec() == QDialog.Accepted:
            exercise_data = dialog.get_data()
            final_data = {k: v for k, v in exercise_data.items() if v}  # Filter out empty values
            final_data["id_exercise_assignment"] = id_exercise_assignment # Set the exercise ID for the update
            success, message = self.api.update_exercise_assignment(id_exercise_assignment, final_data)
            if success:
                QMessageBox.information(self.view, "Éxito", "Ejercicio modificado correctamente.")
                self.load_exercises_assigned()  # Refresh the exercise list
                self.load_exercises_done_today()  # Refresh the exercises done today
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
                self.load_exercises_done_today()  # Refresh the exercises done today
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