from PySide6.QtWidgets import QAbstractItemView, QFrame, QHBoxLayout, QHeaderView, QTableWidget, QTableWidgetItem, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

class PhysioDashboard(QWidget):
    def __init__(self, api_client):
        super().__init__()
        self.api = api_client
        self.setWindowTitle(f"Rehab & Move - Dashboard Fisioterapeuta- Panel de {self.api.name}")
        self.setMinimumSize(800, 600)
        self.setWindowIcon(QIcon("assets/logo_Rehab_Move.png"))
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        self.sidebar = QFrame()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(200)
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(20, 20, 20, 20)
        sidebar_layout.setSpacing(20)

        # Sidebar buttons
        self.btn_add = QPushButton("Añadir Paciente")
        sidebar_layout.addWidget(self.btn_add)
        self.btn_add.setObjectName("MenuBtn")

        self.btn_mod = QPushButton("Modificar Paciente")
        sidebar_layout.addWidget(self.btn_mod)
        self.btn_mod.setObjectName("MenuBtn")

        self.btn_delete = QPushButton("Eliminar Paciente")
        sidebar_layout.addWidget(self.btn_delete)
        self.btn_delete.setObjectName("MenuBtn")

        self.btn_appointments = QPushButton("Citas")
        sidebar_layout.addWidget(self.btn_appointments)
        self.btn_appointments.setObjectName("MenuBtn2")

        self.btn_pain_records = QPushButton("Registros de Dolor")
        sidebar_layout.addWidget(self.btn_pain_records)
        self.btn_pain_records.setObjectName("MenuBtn2")

        self.btn_exercises = QPushButton("Menu Ejercicios")
        sidebar_layout.addWidget(self.btn_exercises)
        self.btn_exercises.setObjectName("MenuBtn")

        self.btn_assign_exercises = QPushButton("Ejercicios Asignados")
        sidebar_layout.addWidget(self.btn_assign_exercises)
        self.btn_assign_exercises.setObjectName("MenuBtn")

        self.btn_logout = QPushButton("Cerrar Sesión")
        sidebar_layout.addWidget(self.btn_logout)
        self.btn_logout.setObjectName("CancelBtn")

        self.content_container = QFrame()
        self.content_container.setObjectName("ContentArea")
        content_layout = QVBoxLayout(self.content_container)

        self.title = QLabel("Lista de Pacientes")
        self.title.setObjectName("SectionTitle")
        self.title.setAlignment(Qt.AlignCenter)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Nombre", "Apellidos", "Email", "Teléfono", "Fecha Inicio"])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)  # Select entire rows

        #Customize table appearance and behavior
        self.table.horizontalHeader().setStretchLastSection(True) # Stretch the last column to fill remaining space
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # Make the table read-only
        self.table.verticalHeader().setVisible(False)  # Hide row numbers
        self.table.setShowGrid(False)  # Hide grid lines for a cleaner look
        self.table.setAlternatingRowColors(True)  # Alternate row colors for better readability
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)  # Allow only single row selection
        

        # Customize column widths
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents) # Adjust width to content for ID column
        header.setSectionResizeMode(1, QHeaderView.Stretch) # Stretch name column to fill available space
        header.setSectionResizeMode(2, QHeaderView.Stretch) # Stretch surnames column to fill available space
        header.setSectionResizeMode(3, QHeaderView.Stretch) # Stretch email column to fill available space
        header.setSectionResizeMode(4, QHeaderView.Fixed) # Set fixed width for phone column
        header.setSectionResizeMode(5, QHeaderView.Fixed) # Set fixed width for start date column
        self.table.setColumnWidth(4, 140) # Set fixed width for phone column
        self.table.setColumnWidth(5, 140) # Set fixed width for start date column

        content_layout.addWidget(self.title)
        content_layout.addWidget(self.table)

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.content_container)
        self.setLayout(main_layout)
