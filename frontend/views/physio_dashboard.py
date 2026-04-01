from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from PySide6.QtCore import Qt

class PhysioDashboard(QWidget):
    def __init__(self, user_name):
        super().__init__()
        self.setWindowTitle(f"Rehab & Move - Dashboard Fisioterapeuta- Panel de {user_name}")
        self.setMinimumSize(800, 600)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Dashboard del Fisioterapeuta")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.setLayout(layout)
    
    def load_patients(self):
        pass