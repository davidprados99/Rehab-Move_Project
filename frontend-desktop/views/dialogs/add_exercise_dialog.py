from PySide6.QtWidgets import QDialog, QMessageBox, QTextEdit, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QDateEdit
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QIcon

class AddExerciseDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Añadir Nuevo Ejercicio")
        self.setMinimumWidth(400)
        self.setWindowIcon(QIcon("assets/logo_Rehab_Move.png"))
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        title = QLabel("Datos del Ejercicio")
        title.setObjectName("QLabelFormTitle")
        layout.addWidget(title)

        self.form_layout = QFormLayout()
        self.form_layout.setSpacing(15)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nombre del ejercicio")
        
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Descripción del ejercicio")
        
        self.video_url_input = QLineEdit()
        self.video_url_input.setPlaceholderText("URL del video del ejercicio")

        self.form_layout.addRow("Nombre:", self.name_input)
        self.form_layout.addRow("Descripción:", self.description_input)
        self.form_layout.addRow("URL del video:", self.video_url_input)
        layout.addLayout(self.form_layout)

        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Guardar Ejercicio")
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
            self.name_input.setFocus()
            return
        if not self.description_input.text().strip():
            QMessageBox.critical(self, "Error", "La descripción es obligatoria.")
            self.description_input.setFocus()
            return
        if not self.video_url_input.text().strip():
            QMessageBox.critical(self, "Error", "La URL del video es obligatoria.")
            self.video_url_input.setFocus()
            return
        if not (self.video_url_input.text().startswith("http://") or self.video_url_input.text().startswith("https://")):
            QMessageBox.critical(self, "Error", "La URL del video debe comenzar con http:// o https://.")
            self.video_url_input.setFocus()
            return
        super().accept() # Call the base class accept to close the dialog

    def get_data(self):
        """Return the data entered by the user as a dictionary."""
        return {
            "name": self.name_input.text().strip(),
            "description": self.description_input.toPlainText().strip(),
            "video_url": self.video_url_input.text().strip(),
            "active": True   
        }