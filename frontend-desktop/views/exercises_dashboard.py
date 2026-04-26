from PySide6.QtWidgets import QAbstractItemView, QFrame, QHBoxLayout, QHeaderView, QTableWidget, QTableWidgetItem, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

class ExercisesDashboard(QWidget):
    def __init__(self, api_client):
        super().__init__()
        self.api = api_client
        self.setWindowTitle("Gestión de Ejercicios")
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

        #Sidebar buttons
        self.btn_add_exercise = QPushButton("Añadir Ejercicio")
        sidebar_layout.addWidget(self.btn_add_exercise)
        self.btn_add_exercise.setObjectName("MenuBtn")

        self.btn_mod_exercise = QPushButton("Modificar Ejercicio")
        sidebar_layout.addWidget(self.btn_mod_exercise)
        self.btn_mod_exercise.setObjectName("MenuBtn")

        self.btn_delete_exercise = QPushButton("Eliminar Ejercicio")
        sidebar_layout.addWidget(self.btn_delete_exercise)
        self.btn_delete_exercise.setObjectName("MenuBtn")

        self.btn_assign_exercise = QPushButton("Asignar Ejercicio")
        sidebar_layout.addWidget(self.btn_assign_exercise)
        self.btn_assign_exercise.setObjectName("MenuBtn")

        self.btn_back = QPushButton("Volver al Dashboard")
        sidebar_layout.addWidget(self.btn_back)
        self.btn_back.setObjectName("CancelBtn")

        self.content_container = QFrame()
        self.content_container.setObjectName("ContentArea")
        content_layout = QVBoxLayout(self.content_container)

        self.title = QLabel("Gestión de Ejercicios")
        self.title.setObjectName("SectionTitle")
        self.title.setAlignment(Qt.AlignCenter)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Nombre", "Descripción", "URL", "Activo"])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)  # Select entire rows

        #Customize table appearance and behavior
        self.table.horizontalHeader().setStretchLastSection(True) # Stretch the last column to fill remaining space
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # Make the table read-only
        self.table.verticalHeader().setVisible(False)  # Hide row numbers
        self.table.setShowGrid(False)  # Hide grid lines for a cleaner look
        self.table.setAlternatingRowColors(True)  # Alternate row colors for better readability
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)  # Allow only single row selection
        self.table.verticalHeader().setDefaultSectionSize(40)  # Set default row height
        

        # Customize column widths
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents) # Adjust width to content for ID column
        header.setSectionResizeMode(1, QHeaderView.Stretch) # Stretch name column to fill available space
        header.setSectionResizeMode(2, QHeaderView.Stretch) # Stretch description column to fill available space
        header.setSectionResizeMode(3, QHeaderView.Stretch) # Stretch URL column to fill available space
        header.setSectionResizeMode(4, QHeaderView.Fixed) # Set fixed width for active column
        self.table.setColumnWidth(4, 100) # Set fixed width for active column

        content_layout.addWidget(self.title)
        content_layout.addWidget(self.table)
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.content_container)
