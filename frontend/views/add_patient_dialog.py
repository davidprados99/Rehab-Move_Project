from PySide6.QtWidgets import QDialog, QMessageBox, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QDateEdit
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QIcon

class AddPatientDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Añadir Nuevo Paciente")
        self.setMinimumWidth(400)
        self.setWindowIcon(QIcon("assets/logo_Rehab&Move.png"))
        self.init_ui()
        
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
        self.form_layout.addRow("email:", self.email_input)
        self.form_layout.addRow("Teléfono", self.phone_input)
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
        if not self.name_input.text().strip():
            QMessageBox.critical(self, "Error", "El nombre es obligatorio.")
            return
        if not self.surnames_input.text().strip():
            QMessageBox.critical(self, "Error", "Los apellidos son obligatorios.")
            return
        if not self.email_input.text().strip():
            QMessageBox.critical(self, "Error", "El email es obligatorio.")
            return
        if "@" not in self.email_input.text() or "." not in self.email_input.text():
            QMessageBox.critical(self, "Error", "El email no es válido.")
            return
        if not self.phone_input.text().strip():
            QMessageBox.critical(self, "Error", "El teléfono es obligatorio.")
            return
        if not self.password_input.text().strip():
            QMessageBox.critical(self, "Error", "La contraseña es obligatoria.")
            return
        
        super().accept() # Call the base class accept to close the dialog

    def get_data(self):
        """Return the data entered by the user as a dictionary."""
        return {
            "name": self.name_input.text().strip(),
            "surnames": self.surnames_input.text().strip(),
            "email": self.email_input.text().strip().lower(),
            "phone": self.phone_input.text().strip(),
            "password": self.password_input.text().strip(),
            "start_date": QDate.currentDate().toString("yyyy-MM-dd"),
            "id_physio": None # This will be set in the API call based on the logged-in physio's ID   
        }