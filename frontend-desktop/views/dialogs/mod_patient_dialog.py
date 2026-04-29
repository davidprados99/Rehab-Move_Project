from PySide6.QtWidgets import QDialog, QMessageBox, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout
from PySide6.QtGui import QIcon
from utils import resource_path

class ModPatientDialog(QDialog):
    def __init__(self, patient_data=None, parent=None):
            super().__init__(parent)
            self.setWindowTitle("Modificar Paciente")
            self.setMinimumWidth(400)
            self.setWindowIcon(QIcon(resource_path("assets/logo_Rehab_Move.png")))
            self.init_ui()
            if patient_data:
                self.load_patient_data(patient_data)
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        title = QLabel("Datos del Paciente")
        title.setObjectName("QLabelFormTitle")
        layout.addWidget(title)

        self.form_layout = QFormLayout()
        self.form_layout.setSpacing(15)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nombre del paciente")
        
        self.surnames_input = QLineEdit()
        self.surnames_input.setPlaceholderText("Apellidos completos")
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("ejemplo@correo.com")

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Teléfono del paciente")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña segura")
        self.password_input.setEchoMode(QLineEdit.Password)


        self.form_layout.addRow("Nombre:", self.name_input)
        self.form_layout.addRow("Apellidos:", self.surnames_input)
        self.form_layout.addRow("Email:", self.email_input)
        self.form_layout.addRow("Teléfono:", self.phone_input)
        self.form_layout.addRow("Contraseña:", self.password_input)
        layout.addLayout(self.form_layout)

        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Guardar Paciente")
        self.save_btn.setObjectName("LoginBtn")
        
        self.cancel_btn = QPushButton("Cancelar")
        self.cancel_btn.setObjectName("CancelBtn")
        
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.save_btn)
        layout.addLayout(btn_layout)

        # Conexiones
        self.save_btn.clicked.connect(self.accept) # Close with accept code to indicate success
        self.cancel_btn.clicked.connect(self.reject) # Close with reject code to indicate cancellation

    def accept(self):
        """Override accept to validate input before closing the dialog."""
        #If the email field is not empty, validate it
        if self.email_input.text() and ("@" not in self.email_input.text() or "." not in self.email_input.text()):
            QMessageBox.critical(self, "Error", "El email no es válido.")
            self.email_input.setFocus()
            return
        #If the phone field is not empty, validate it
        if self.phone_input.text() and not self.phone_input.text().strip().isdigit():
            QMessageBox.critical(self, "Error", "El teléfono debe contener solo números.")
            self.phone_input.setFocus()
            return
        
        super().accept() # Call the base class accept to close the dialog
    
    def load_patient_data(self, patient_data):
        """Load existing patient data into the form."""
        self.name_input.setText(patient_data.get("name", ""))
        self.surnames_input.setText(patient_data.get("surnames", ""))
        self.email_input.setText(patient_data.get("email", ""))
        self.phone_input.setText(patient_data.get("phone", ""))
        # Password is not loaded for security reasons

    def get_data(self):
        """Return the data entered by the user as a dictionary."""
        return {
            "name": self.name_input.text().strip() if self.name_input.text().strip() else None,
            "surnames": self.surnames_input.text().strip() if self.surnames_input.text().strip() else None,
            "email": self.email_input.text().strip().lower() if self.email_input.text().strip() else None,
            "phone": self.phone_input.text().strip() if self.phone_input.text().strip() else None,
            "password": self.password_input.text().strip() if self.password_input.text().strip() else None,
            "start_date": None, 
            "id_physio": None
        }