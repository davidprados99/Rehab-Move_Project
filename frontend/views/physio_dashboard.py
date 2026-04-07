from PySide6.QtWidgets import QAbstractItemView, QDialog, QFrame, QHBoxLayout, QHeaderView, QTableWidget, QTableWidgetItem, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from services.api_client import ApiClient
from views.add_patient_dialog import AddPatientDialog

class PhysioDashboard(QWidget):
    def __init__(self, api_client):
        super().__init__()
        self.api = api_client
        self.setWindowTitle(f"Rehab & Move - Dashboard Fisioterapeuta- Panel de {self.api.name}")
        self.setMinimumSize(800, 600)
        self.setWindowIcon(QIcon("assets/logo_Rehab&Move.png"))
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.sidebar = QFrame()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(200)
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(20, 20, 20, 20)

        # Sidebar buttons
        self.btn_exercises = QPushButton("Menu Ejercicios")
        sidebar_layout.addWidget(self.btn_exercises)
        self.btn_exercises.setObjectName("MenuBtn")

        self.btn_add = QPushButton("Añadir Paciente")
        sidebar_layout.addWidget(self.btn_add)
        self.btn_add.setObjectName("MenuBtn")

        self.btn_delete = QPushButton("Eliminar Paciente")
        sidebar_layout.addWidget(self.btn_delete)
        self.btn_delete.setObjectName("MenuBtn")

        self.btn_appointments = QPushButton("Citas")
        sidebar_layout.addWidget(self.btn_appointments)
        self.btn_appointments.setObjectName("MenuBtn")

        self.btn_pain_record = QPushButton("Registros de Dolor")
        sidebar_layout.addWidget(self.btn_pain_record)
        self.btn_pain_record.setObjectName("MenuBtn")

        self.btn_exercise_plan = QPushButton("Plan de Ejercicio")
        sidebar_layout.addWidget(self.btn_exercise_plan)
        self.btn_exercise_plan.setObjectName("MenuBtn")

        self.btn_logout = QPushButton("Cerrar Sesión")
        sidebar_layout.addWidget(self.btn_logout)
        self.btn_logout.setObjectName("MenuBtn")

        self.content_container = QFrame()
        self.content_container.setObjectName("ContentArea")
        content_layout = QVBoxLayout(self.content_container)

        self.title = QLabel("Lista de Pacientes")
        self.title.setObjectName("SectionTitle")
        self.title.setAlignment(Qt.AlignCenter)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Nombre", "Apellidos", "mail", "Fecha Inicio"])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)  # Select entire rows

        #Customize table appearance
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # Make the table read-only
        self.table.verticalHeader().setVisible(False)  # Hide row numbers
        self.table.setShowGrid(False)  # Hide grid lines for a cleaner look
        self.table.setAlternatingRowColors(True)  # Alternate row colors for better readability
        

        # Customize column widths
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents) 
        header.setSectionResizeMode(1, QHeaderView.Stretch)          
        header.setSectionResizeMode(2, QHeaderView.Stretch)          
        header.setSectionResizeMode(3, QHeaderView.Stretch)          
        header.setSectionResizeMode(4, QHeaderView.Fixed)            
        self.table.setColumnWidth(4, 120)

        content_layout.addWidget(self.title)
        content_layout.addWidget(self.table)

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.content_container)
        self.setLayout(main_layout)

        
