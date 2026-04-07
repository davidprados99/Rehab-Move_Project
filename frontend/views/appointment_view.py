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
        
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.setObjectName("Calendar")

        main_layout.addWidget(self.title)
        main_layout.addWidget(self.calendar)

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
        
        # Define style for appointment days
        fmt_done = QTextCharFormat()
        fmt_done.setBackground(QColor("#5DA7A3")) 
        fmt_done.setForeground(QColor("white"))
        fmt_done.setFontWeight(QFont.Bold)

        #Define style for pending appointment 
        fmt_pending = QTextCharFormat()
        fmt_pending.setBackground(QColor("#F0E68C")) 
        fmt_pending.setForeground(QColor("black"))
        fmt_pending.setFontWeight(QFont.Bold)

        # Define style for cancelled appointment
        fmt_cancelled = QTextCharFormat()
        fmt_cancelled.setBackground(QColor("#F08080"))
        fmt_cancelled.setForeground(QColor("white"))
        fmt_cancelled.setFontWeight(QFont.Bold)

        # Clean the calendar first
        self.calendar.setDateTextFormat(QDate(), QTextCharFormat())

        # Mark the days with appointments
        for appt in appointments:
            # gET the date part from the datetime string
            date_str = appt["date"].split("T")[0]
            qdate = QDate.fromString(date_str, "yyyy-MM-dd")
            
            # Check if the date is valid before applying the format
            if qdate.isValid():
                if appt["state"] == "completado":
                    self.calendar.setDateTextFormat(qdate, fmt_done)
                elif appt["state"] == "pendiente":
                    self.calendar.setDateTextFormat(qdate, fmt_pending)
                elif appt["state"] == "cancelado":
                    self.calendar.setDateTextFormat(qdate, fmt_cancelled)

    



