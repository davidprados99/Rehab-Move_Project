from typing import Counter

from PySide6.QtWidgets import QCalendarWidget, QStyledItemDelegate, QTableView, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QAbstractItemView, QMessageBox, QDialog
from PySide6.QtCore import QDate, Qt
from PySide6.QtGui import QColor, QFont, QIcon, QPen, QTextCharFormat

class AppointmentView(QWidget):

    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api = api_client
        self.painted_dates = []  # To keep track of which dates we've marked in the calendar
        self.setWindowTitle("Rehab & Move - Citas")
        self.setMinimumSize(600, 400)
        self.setWindowIcon(QIcon("assets/logo_Rehab_Move.png"))
        self.init_ui()
    
    def init_ui(self):
        main_layout = QVBoxLayout(self)

        self.title = QLabel("Calendario de sesiones")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setObjectName("SectionTitle")
        
        self.calendar_layout = QVBoxLayout()
        self.calendar_layout.setContentsMargins(20, 20, 20, 60)

        self.calendar = QCalendarWidget()
        self.calendar.setObjectName("CitasCalendar")
        self.calendar.setGridVisible(True)

        self.calendar_layout.addWidget(self.calendar)

        main_layout.addWidget(self.title)
        main_layout.addLayout(self.calendar_layout)
        
        self.btn_back = QPushButton("Volver")
        self.btn_back.setObjectName("CancelBtn")
        main_layout.addWidget(self.btn_back)
    
    def update_calendar_markers(self, appointments):
        clean_fmt = QTextCharFormat() 
        for qdate in self.painted_dates:
            self.calendar.setDateTextFormat(qdate, clean_fmt)
        self.painted_dates.clear() 

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
        date_list = [appt["date"].split("T")[0] for appt in appointments if appt["state"] != "cancelado"]
        appt_count = Counter(date_list)

        TOTAL_SLOTS = 13  # From 9:00 to 22:00

        for date_str, count in appt_count.items():
            qdate = QDate.fromString(date_str, "yyyy-MM-dd")
            self.painted_dates.append(qdate)  # Keep track of painted dates to reset later
            if count >= TOTAL_SLOTS:
                self.calendar.setDateTextFormat(qdate, fmt_full)
            else:
                self.calendar.setDateTextFormat(qdate, fmt_partial)

        # Additionally, underline today's date      
        today = QDate.currentDate()
        fmt = self.calendar.dateTextFormat(today)
        fmt.setFontUnderline(True)     
        fmt.setFontWeight(QFont.ExtraBold)
        self.calendar.setDateTextFormat(today, fmt)
        self.painted_dates.append(today)
        



