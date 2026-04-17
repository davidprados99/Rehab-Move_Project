from PySide6.QtWidgets import QAbstractItemView, QDialog, QFrame, QHBoxLayout, QHeaderView, QTableWidget, QTableWidgetItem, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from matplotlib.figure import Figure
from services.api_client import ApiClient
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class PainRecordView(QWidget):
    def __init__(self, api_client, id_patient, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.id_patient = id_patient
        self.setWindowTitle("Registro de Dolor")
        self.setMinimumSize(600, 400)
        self.setWindowIcon(QIcon("assets/logo_Rehab&Move.png"))
        self.init_ui()
    
    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 10, 20, 10)
        main_layout.setSpacing(15)

        self.title = QLabel("Historial de Dolor")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setObjectName("SectionTitle")
        main_layout.addWidget(self.title, stretch=0)

        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        main_layout.addWidget(self.canvas, stretch=1)

        self.btn_back = QPushButton("Volver")
        self.btn_back.setObjectName("CancelBtn")
        self.btn_back.setFixedWidth(150)
        main_layout.addWidget(self.btn_back, stretch=0, alignment=Qt.AlignCenter)
