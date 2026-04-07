from PySide6.QtWidgets import QCalendarWidget, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QAbstractItemView, QMessageBox, QDialog
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

class AppointmentView(QWidget):

    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api = api_client
        self.setWindowTitle("Rehab & Move - Citas")
        self.setMinimumSize(600, 400)
        self.setWindowIcon(QIcon("assets/logo_Rehab&Move.png"))
        self.init_ui()
    
    def init_ui(self):
        main_layout = QHBoxLayout(self)

        # --- Left Column ---

        left_panel = QVBoxLayout()

        self.title = QLabel("Calendario de sesiones")
        
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.setObjectName("Calendar")

        # Role handle
        if self.api.user_role != "physio":
            self.calendar.setSelectionMode(QCalendarWidget.NoSelection)  
        else:
            self.calendar.setSelectionMode(QCalendarWidget.SingleSelection)  

        left_panel.addWidget(self.title)
        left_panel.addWidget(self.calendar)

        #Add button only for physios to create appointments
        self.btn_add_appointment = QPushButton("Añadir Cita")
        self.btn_add_appointment.setObjectName("LoginBtn")

        # Role handle
        if self.api.user_role != "physio":
            self.btn_add_appointment.hide()

        left_panel.addWidget(self.btn_add_appointment)
        left_panel.addStretch()

        # --- Right Column ---
        right_panel = QVBoxLayout()

        # Future appointments
        self.future_label = QLabel("Próximas Citas")
        self.future_table = QTableWidget(0, 3)
        self.future_table.setHorizontalHeaderLabels(["Fecha", "Paciente", "Acción"])
        right_panel.addWidget(self.future_label)

        # Role handle
        if self.api.user_role != "physio":
            self.future_table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # Disable editing for patients
        right_panel.addWidget(self.future_table)
        
        # Past appointments
        self.past_label = QLabel("Citas Pasadas")
        self.past_table = QTableWidget(0, 3)
        self.past_table.setHorizontalHeaderLabels(["Fecha", "Paciente", "Resumen"])
        right_panel.addWidget(self.past_label)

        # Btn Back
        self.btn_back = QPushButton("Volver")
        self.btn_back.setObjectName("LoginBtn")
        right_panel.addWidget(self.btn_back)

        main_layout.addLayout(left_panel, 1)
        main_layout.addLayout(right_panel, 2)

    



