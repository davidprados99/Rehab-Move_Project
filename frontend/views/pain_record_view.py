from PySide6.QtWidgets import QAbstractItemView, QDialog, QFrame, QHBoxLayout, QHeaderView, QTableWidget, QTableWidgetItem, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from matplotlib.figure import Figure
from services.api_client import ApiClient
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd

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
        self.title = QLabel("Registro de Dolor")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setObjectName("SectionTitle")
        main_layout.addWidget(self.title)

        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        main_layout.addWidget(self.canvas)

        success, pain_records = self.api_client.get_pain_records(self.id_patient)
        if success:
            self.generate_pain_graphic(pain_records)
        else:
            QMessageBox.warning(self, "Error", "No se pudieron cargar los registros de dolor.")

        self.btn_back = QPushButton("Volver")
        self.btn_back.setObjectName("CancelBtn")
        main_layout.addWidget(self.btn_back)


    def generate_pain_graphic(self, pain_records):
        if not pain_records:
            QMessageBox.information(self, "Sin datos", "No hay registros de dolor para mostrar.")
            return
        
        self.df = pd.DataFrame(pain_records)
        self.df['record_date'] = pd.to_datetime(self.df['record_date'])
        self.df.sort_values('record_date', inplace=True)

        self.figure.clear()
        ax = self.figure.add_subplot(111)

        ax.plot(self.df['record_date'], self.df['level_pain'], 
                marker='o', 
                linestyle='-', 
                color='#F08080', 
                linewidth=2, 
                markersize=8,
                picker= 10)
        
        ax.set_title('Evolución del Dolor en el Tiempo')
        ax.set_xlabel('Fecha')
        ax.set_ylabel('Nivel de Dolor')
        ax.set_ylim(-0.5, 10.5)
        ax.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)

        self.canvas.mpl_connect('pick_event', self.on_pick)

        self.figure.autofmt_xdate()
        self.canvas.draw()
    
    def on_pick(self, event):
        # Take the index of the point that was clicked
        ind = event.ind[0] 
        
        # Get the corresponding data from the DataFrame
        date = self.df.iloc[ind]['record_date'].strftime('%d/%m/%Y')
        level = self.df.iloc[ind]['level_pain']
        comment = self.df.iloc[ind]['comment'] or "Sin comentarios adicionales."

        # Launch a pop-up with the details of the pain record
        self.show_record_details(date, level, comment)

    def show_record_details(self, date, level, comment):
        msg = QMessageBox(self)
        msg.setWindowTitle(f"Detalle del Registro - {date}")
        msg.setIcon(QMessageBox.Information)
        
        # Use HTML to format the message content with colors and styles
        text_html = f"""
        <h3 style='color: #5DA7A3;'>Resumen de la Sesión</h3>
        <p><b>Fecha:</b> {date}</p>
        <p><b>Nivel de Dolor:</b> <span style='color: #F08080; font-size: 16px;'>{level}/10</span></p>
        <hr>
        <p><b>Notas del fisio:</b><br><i>{comment}</i></p>
        """
        msg.setText(text_html)
        msg.exec()