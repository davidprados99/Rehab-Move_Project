from PySide6.QtWidgets import  QDialog, QHBoxLayout, QLabel, QMenu, QTableWidgetItem, QMessageBox, QWidget
from PySide6.QtCore import Qt

from views.dialogs.add_exercise_assig_dialog import AddExerciseAssigDialog
from views.exercises_dashboard import ExercisesDashboard
from views.dialogs.add_exercise_dialog import AddExerciseDialog
from views.dialogs.mod_exercise_dialog import ModExerciseDialog
from views.dialogs.video_dialog import VideoDialog
from PySide6.QtGui import QPixmap
from utils import resource_path

class ExercisesController:
    def __init__(self, api_client):
        self.api = api_client
        self.view = ExercisesDashboard(self.api)
        self.view.showMaximized()

        self.view.btn_add_exercise.clicked.connect(self.handle_add_exercise)
        self.view.btn_mod_exercise.clicked.connect(self.handle_mod_exercise)
        self.view.btn_delete_exercise.clicked.connect(self.handle_delete_exercise)
        self.view.btn_assign_exercise.clicked.connect(self.handle_assign_exercise)
        self.view.btn_back.clicked.connect(self.go_back)
        self.view.table.cellDoubleClicked.connect(self.show_video)
        self.load_exercises()

        self.view.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.view.table.customContextMenuRequested.connect(self.show_context_menu)

    
    def load_exercises(self):
        success, exercises = self.api.get_exercises()

        if success:
            self.view.table.setRowCount(0)  # Clear existing rows

            for row_number, exercise in enumerate(exercises):

                icon_item = QTableWidgetItem()

                self.view.table.insertRow(row_number)
                self.view.table.setItem(row_number, 0, QTableWidgetItem(str(exercise.get("id_exercise"))))
                self.view.table.setItem(row_number, 1, QTableWidgetItem(exercise.get("name", "N/A")))
                self.view.table.setItem(row_number, 2, QTableWidgetItem(exercise.get("description", "N/A")))
                self.view.table.setItem(row_number, 3, QTableWidgetItem(exercise.get("video_url", "N/A")))

                # Icon for active status
                container = QWidget()  # Create a container widget for the icon
                layout = QHBoxLayout(container)  # Create a horizontal layout for the container

                icon_label = QLabel()  # Create a label to hold the icon
                icon_path = resource_path("assets/done.png") if exercise.get("active") else resource_path("assets/noDone.png")

                original_pixmap = QPixmap(icon_path)
                icon_size = 15 if exercise.get("active") else 10  
                dpr = self.view.devicePixelRatioF() # Get the device pixel ratio for high-DPI scaling

                pixmap = original_pixmap.scaled(
                    icon_size * dpr, icon_size * dpr, Qt.KeepAspectRatio, Qt.SmoothTransformation
                )

                icon_label.setPixmap(pixmap)  # Set the pixmap to the label
                layout.addWidget(icon_label)  # Add the label to the layout
                layout.setAlignment(Qt.AlignCenter)  # Center the layout
                layout.setContentsMargins(0, 0, 0, 0)  # Remove margins to fit the icon properly

                self.view.table.setCellWidget(row_number, 4, container)  # Set the container as the cell widget
            

                for column in range(4):
                    self.view.table.item(row_number, column).setTextAlignment(Qt.AlignCenter)
        
        else:
            QMessageBox.critical(self.view, "Error", f"No se pudieron cargar los ejercicios: {exercises}")
        
    def handle_add_exercise(self):
        dialog = AddExerciseDialog()
        if dialog.exec() == QDialog.Accepted:
            exercise_data = dialog.get_data()
            success, message = self.api.add_exercise(exercise_data)
            if success:
                QMessageBox.information(self.view, "Éxito", "Ejercicio añadido correctamente.")
                self.load_exercises()  # Refresh the exercise list
            else:
                QMessageBox.critical(self.view, "Error", f"No se pudo añadir el ejercicio: {message}")

    def handle_mod_exercise(self):
        selected_items = self.view.table.selectedItems() if self.view.table.selectedItems() else []
        exercise_data = {
            "name": selected_items[1].text(),
            "description": selected_items[2].text(),
            "video_url": selected_items[3].text(),
            "active": True
        } if selected_items else None

        if not selected_items:
            QMessageBox.warning(self.view, "Advertencia", "Por favor, seleccione un ejercicio para modificar.")
            return
        id_exercise = selected_items[0].text()
        
        dialog = ModExerciseDialog(exercise_data=exercise_data)
        if dialog.exec() == QDialog.Accepted:
            exercise_data = dialog.get_data()
            final_data = {k: v for k, v in exercise_data.items() if v is not None}  # Filter out empty values
            final_data["id_exercise"] = id_exercise  # Set the exercise ID for the update
            success, message = self.api.update_exercise(id_exercise, final_data)
            if success:
                QMessageBox.information(self.view, "Éxito", "Ejercicio modificado correctamente.")
                self.load_exercises()  # Refresh the exercise list
            else:
                QMessageBox.critical(self.view, "Error", f"No se pudo modificar el ejercicio: {message}")

    def handle_delete_exercise(self):
        selected_items = self.view.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self.view, "Advertencia", "Por favor, seleccione un ejercicio para eliminar.")
            return
        
        id_exercise = selected_items[0].text()  
        confirm = QMessageBox.question(self.view, "Confirmar Eliminación", f"¿Está seguro de que desea eliminar el ejercicio con ID {id_exercise}?", QMessageBox.Yes | QMessageBox.No)
        
        if confirm == QMessageBox.Yes:
            success, message = self.api.delete_exercise(id_exercise)
            if success:
                QMessageBox.information(self.view, "Éxito", f"Ejercicio con ID {id_exercise} eliminado correctamente.")
                self.load_exercises()
            else:
                QMessageBox.critical(self.view, "Error", f"No se pudo eliminar el ejercicio con ID {id_exercise}: {message}")

    def handle_assign_exercise(self):
        dialog = AddExerciseAssigDialog(self.api)
        if dialog.exec() == QDialog.Accepted:
            assignment_data = dialog.get_data()
            success, message = self.api.create_exercise_assignment(assignment_data)
            if success:
                QMessageBox.information(self.view, "Éxito", "Ejercicio asignado correctamente.")
            else:
                QMessageBox.critical(self.view, "Error", f"No se pudo asignar el ejercicio: {message}")

    def go_back(self):
        self.view.close()
        from controllers.physio_controller import PhysioController
        self.physio_controller = PhysioController(self.api)
        self.physio_controller.view.show()
    
    def show_context_menu(self, pos):
        menu = QMenu(self.view)

        menu.addAction("Editar", self.handle_mod_exercise)
        menu.addAction("Eliminar", self.handle_delete_exercise)
        
        # If the user right-clicks outside of any valid row, we should not show the context menu
        index = self.view.table.indexAt(pos)
        if not index.isValid():
            return 

        global_pos = self.view.table.viewport().mapToGlobal(pos)
        menu.exec(global_pos)
    
    def show_video(self, video_url):
        selected_items = self.view.table.selectedItems()
        
        name = selected_items[1].text() if selected_items else "Ejercicio"
        description = selected_items[2].text() if selected_items else "N/A"
        video_url = selected_items[3].text() if selected_items else None

        if video_url and video_url != "N/A":
            self.video_dialog = VideoDialog(name, description, video_url)
            self.video_dialog.exec()
            if self.video_dialog.result() == QDialog.Accepted:
                self.video_dialog.close()
        else:
            QMessageBox.warning(self.view, "Advertencia", "No hay un video válido para este ejercicio.")
