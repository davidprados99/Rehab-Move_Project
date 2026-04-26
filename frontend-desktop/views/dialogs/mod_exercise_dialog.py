from PySide6.QtWidgets import QCheckBox, QDialog, QTextEdit,QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout
from PySide6.QtGui import QIcon

class ModExerciseDialog(QDialog):

    def __init__(self, exercise_data=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Modificar Ejercicio")
        self.setMinimumWidth(400)
        self.setWindowIcon(QIcon("assets/logo_Rehab_Move.png"))
        self.init_ui()
        if exercise_data:
            self.load_exercise_data(exercise_data)
        
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

        self.active_checkbox = QCheckBox()
        self.active_checkbox.setChecked(True)  # Default to active, can be changed when loading exercise data

        self.form_layout.addRow("Nombre:", self.name_input)
        self.form_layout.addRow("Descripción:", self.description_input)
        self.form_layout.addRow("URL del video:", self.video_url_input)
        self.form_layout.addRow("Activo:", self.active_checkbox)
        layout.addLayout(self.form_layout)

        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Guardar Cambios")
        self.save_btn.setObjectName("LoginBtn")
        
        self.cancel_btn = QPushButton("Cancelar")
        self.cancel_btn.setObjectName("CancelBtn")
        
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.save_btn)
        layout.addLayout(btn_layout)

        # Conexiones
        self.save_btn.clicked.connect(self.accept) # Close with accept code to indicate success
        self.cancel_btn.clicked.connect(self.reject) # Close with reject code to indicate cancellation

    def load_exercise_data(self, exercise_data):
        """Load existing exercise data into the form."""
        self.name_input.setText(exercise_data.get("name", ""))
        self.description_input.setText(exercise_data.get("description", ""))
        self.video_url_input.setText(exercise_data.get("video_url", ""))
        self.active_checkbox.setChecked(exercise_data.get("active", True))

    def get_data(self):
        """Return the data entered by the user as a dictionary."""
        return {
            "name": self.name_input.text().strip() if self.name_input.text().strip() else None,
            "description": self.description_input.text().strip() if self.description_input.text().strip() else None,
            "video_url": self.video_url_input.text().strip() if self.video_url_input.text().strip() else None,
            "active": self.active_checkbox.isChecked()
        }