from PySide6.QtWidgets import QDialog, QFormLayout, QHBoxLayout, QLineEdit, QMessageBox, QPushButton, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

class AddApptDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Agregar Cita")
        self.setWindowIcon(QIcon("assets/logo_Rehab&Move.png"))
        self.resize(350, 500)
        self.init_ui()
        
    def init_ui(self):

        layout = QVBoxLayout(self)

        title = QLabel("Nueva Cita")
        title.setObjectName("QLabelFormTitle")
        layout.addWidget(title)

        self.form_layout = QFormLayout()
        self.form_layout.setSpacing(15)

        self.id_patient_input = QLineEdit()
        self.id_patient_input.setPlaceholderText("ID del paciente")

        self.notes_input = QLineEdit()
        self.notes_input.setPlaceholderText("Notas adicionales para la cita")

        self.form_layout.addRow("ID Paciente:", self.id_patient_input)
        self.form_layout.addRow("Notas:", self.notes_input)
        layout.addLayout(self.form_layout)

        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Guardar Cita")
        self.save_btn.setObjectName("LoginBtn")
        self.cancel_btn = QPushButton("Cancelar") 
        self.cancel_btn.setObjectName("CancelBtn")
        
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.cancel_btn)

        layout.addLayout(btn_layout)

        self.save_btn.clicked.connect(self.accept) # Close with accept code to indicate success
        self.cancel_btn.clicked.connect(self.reject) # Close with reject code to indicate cancellation
    
    def accept(self):
        # Basic validation: Ensure patient ID is entered and is a number
        if not self.id_patient_input.text().strip():
            QMessageBox.critical(self, "Error", "El ID del paciente es obligatorio.")
            self.id_patient_input.setFocus()
            return
        if not self.id_patient_input.text().strip().isdigit():
            QMessageBox.critical(self, "Error", "El ID del paciente debe ser un número.")
            self.id_patient_input.setFocus()
            return
        
        super().accept()  # Call the base class accept to close the dialog with success code

    def get_data(self):
        """Return the data entered by the user as a dictionary."""
        return {
            "date": self.date_str,  # This should be set when opening the dialog
            "state": "pendiente",  # Default state for new appointments
            "notes": self.notes_input.text().strip() if self.notes_input.text().strip() else None,
            "id_patient": int(self.id_patient_input.text().strip()),
            "id_physio": None  # This should be set by the controller based on the logged-in physio
        }