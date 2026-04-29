from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from utils import resource_path

class PatientDashboard(QWidget):
    def __init__(self, user_name):
        super().__init__()
        self.setWindowTitle(f"Rehab & Move - Dashboard Paciente - Panel de {user_name}")
        self.setWindowIcon(QIcon(resource_path("assets/logo_Rehab_Move.png")))
        self.setMinimumSize(800, 600)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Dashboard del Paciente")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        self.setLayout(layout)