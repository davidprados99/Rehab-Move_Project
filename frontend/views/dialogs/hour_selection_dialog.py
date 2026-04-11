from PySide6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel, QScrollArea, QWidget
from PySide6.QtCore import Qt

class HourSelectionDialog(QDialog):
    def __init__(self, date_str, appointments_of_day, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Horas disponibles - {date_str}")
        self.setMinimumSize(350, 500)
        
        self.selected_hour = None
        self.action_type = None # "ADD" o "DELETE"
        self.appointment_id = None 

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(f"Gestión de citas para el día: {date_str}"))

        # Scroll area if there are many hours
        scroll = QScrollArea()
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # Make buttons for hours 9:00 to 21:00
        for h in range(9, 22):
            hour_str = f"{h:02d}:00"
            btn = QPushButton(hour_str)
            btn.setMinimumHeight(40)

            # Hour 14:00 is reserved for lunch break, so we mark it as unavailable
            if h == 14:
                btn.setText(f"{hour_str} - COMIDA")
                btn.setEnabled(False)
                btn.setStyleSheet("background-color: #D3D3D3; color: #7f8c8d; border: none;") # GRAY
            
            else:
                # Check if this hour is occupied by any appointment of the day
                appt = None
                for a in appointments_of_day:
                    if hour_str in a["date"]:
                        appt = a
                        break
                if appt:
                    # 2. Occupied
                    btn.setText(f"{hour_str} - OCUPADO" + f" ({appt['patient']['name']} {appt['patient']['surnames']})")
                    btn.setStyleSheet("background-color: #F08080; color: white; font-weight: bold;") # Red
                    btn.clicked.connect(lambda ch, h=hour_str, id=appt["id_appointment"]: self.handle_click(h, "DELETE", id))
                else:
                    # 3. Free
                    btn.setText(f"{hour_str} - LIBRE")
                    btn.setStyleSheet("background-color: white; color: #2c3e50; border: 1px solid #5DA7A3;") # White with border 
                    btn.clicked.connect(lambda ch, h=hour_str: self.handle_click(h, "ADD"))

            scroll_layout.addWidget(btn)

        scroll.setWidget(scroll_content)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)

    def handle_click(self, hour, action, appt_id=None):
        self.selected_hour = hour
        self.action_type = action
        self.appointment_id = appt_id
        self.accept()