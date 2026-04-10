from PySide6.QtWidgets import QCalendarWidget, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QAbstractItemView, QMessageBox, QDialog
from PySide6.QtCore import QDate, Qt
from PySide6.QtGui import QColor, QFont, QIcon, QTextCharFormat

class AppointmentView(QWidget):

    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api = api_client
        self.setWindowTitle("Rehab & Move - Citas")
        self.setMinimumSize(600, 400)
        self.setWindowIcon(QIcon("assets/logo_Rehab&Move.png"))
        self.init_ui()
    
    def init_ui(self):
        main_layout = QVBoxLayout(self)

        self.title = QLabel("Calendario de sesiones")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setObjectName("SectionTitle")
        
        self.calendar_layout = QVBoxLayout()
        self.calendar_layout.setContentsMargins(20, 20, 20, 60)

        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)

        self.calendar_layout.addWidget(self.calendar)

        main_layout.addWidget(self.title)
        main_layout.addLayout(self.calendar_layout)
        

        bottom_layout = QHBoxLayout()
        #Add button only for physios to create appointments
        self.btn_add_appointment = QPushButton("Añadir Cita")
        self.btn_add_appointment.setObjectName("LoginBtn")

        self.btn_mod_appointment = QPushButton("Modificar Cita")
        self.btn_mod_appointment.setObjectName("LoginBtn")

        self.btn_del_appointment = QPushButton("Eliminar Cita")
        self.btn_del_appointment.setObjectName("LoginBtn")

        self.btn_back = QPushButton("Volver")
        self.btn_back.setObjectName("CancelBtn")
        
        bottom_layout.addWidget(self.btn_add_appointment)
        bottom_layout.addWidget(self.btn_mod_appointment)
        bottom_layout.addWidget(self.btn_del_appointment)
        bottom_layout.addWidget(self.btn_back)

        main_layout.addLayout(bottom_layout)
    
    def update_calendar_markers(self, appointments):
        pass
        #TODO - Add markers to the calendar for the dates with appointments



