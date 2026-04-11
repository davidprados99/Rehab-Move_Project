from typing import Counter

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
        # Red. Complete day
        fmt_full = QTextCharFormat()
        fmt_full.setBackground(QColor("#F08080"))
        fmt_full.setForeground(QColor("white"))
        fmt_full.setFontWeight(QFont.Bold)

        # Green.. Some appointments but not full day
        fmt_partial = QTextCharFormat()
        fmt_partial.setBackground(QColor("#5DA7A3"))
        fmt_partial.setForeground(QColor("white"))

        # Clean all calendar markers first
        self.calendar.setDateTextFormat(QDate(), QTextCharFormat())  # Reset all

        # Count appointments per day
        date_list = [appt["date"].split("T")[0] for appt in appointments if appt["state"] != "CANCELADO"]
        appt_count = Counter(date_list)

        TOTAL_SLOTS = 11  # From 9:00 to 21:00, excluding 14:00

        for date_str, count in appt_count.items():
            qdate = QDate.fromString(date_str, "yyyy-MM-dd")
            if count >= TOTAL_SLOTS:
                self.calendar.setDateTextFormat(qdate, fmt_full)
            else:
                self.calendar.setDateTextFormat(qdate, fmt_partial)



