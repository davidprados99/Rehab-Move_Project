from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from PySide6.QtCore import Qt
from services.api_client import ApiClient

class PhysioDashboard(QWidget):
    def __init__(self, api_client):
        super().__init__()
        self.api = api_client
        self.setWindowTitle(f"Rehab & Move - Dashboard Fisioterapeuta- Panel de {self.api.name}")
        self.setMinimumSize(800, 600)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Dashboard del Fisioterapeuta")
        title.setAlignment(Qt.AlignCenter)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Nombre", "Apellidos", "Email", "Fecha Inicio"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.load_patients()  # Load patients into the table when the dashboard is initialized

        layout.addWidget(title)
        layout.addWidget(self.table)
        self.setLayout(layout)
    
    def load_patients(self):
        id_physio = self.api.user_id  # Assuming the user role contains the physio ID, adjust as needed
        success, patients = self.api.get_patients(id_physio=id_physio)
        if success:
            self.table.setRowCount(0)  # Clear existing rows

            for row_number, patient in enumerate(patients):
                self.table.insertRow(row_number)
                self.table.setItem(row_number, 0, QTableWidgetItem(str(patient.get("id_patient"))))
                self.table.setItem(row_number, 1, QTableWidgetItem(patient.get("name", "N/A")))
                self.table.setItem(row_number, 2, QTableWidgetItem(patient.get("surnames", "N/A")))
                self.table.setItem(row_number, 3, QTableWidgetItem(patient.get("email", "N/A")))
                self.table.setItem(row_number, 4, QTableWidgetItem(patient.get("start_date", "N/A")))

                self.table.item(row_number, 0).setTextAlignment(Qt.AlignCenter)
        else:
            print(f"Error al cargar pacientes: {patients}")
            QMessageBox.critical(self, "Error", f"No se pudieron cargar los pacientes: {patients}")
            