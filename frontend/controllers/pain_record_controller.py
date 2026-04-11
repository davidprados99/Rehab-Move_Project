from PySide6.QtWidgets import QMessageBox
from views.pain_record_view import PainRecordView
from matplotlib import pyplot as plt
import pandas as pd

class PainRecordController:
    def __init__(self, api_client, id_patient):
        self.api = api_client
        self.id_patient = id_patient
        self.view = PainRecordView(api_client, id_patient)
        self.view.btn_back.clicked.connect(self.go_back)
        success, pain_records = self.api.get_pain_records(self.id_patient)
        if success:
            self.generate_pain_graphic(pain_records)
        else:
            QMessageBox.warning(self.view, "Error", "No se pudieron cargar los registros de dolor.")
    
    def go_back(self):
        self.view.close()
        # Logic to return to the previous dashboard (physio or patient) based on user role
        if self.api.user_role == "physio":
            from controllers.physio_controller import PhysioController
            self.physio_controller = PhysioController(self.api)
            self.physio_controller.view.show()
        else:
            from controllers.patient_controller import PatientController
            self.patient_controller = PatientController(self.api)
            self.patient_controller.view.show()

    def generate_pain_graphic(self, pain_records):
        if not pain_records:
            QMessageBox.information(self.view, "Sin datos", "No hay registros de dolor para mostrar.")
            return
        
        self.df = pd.DataFrame(pain_records)
        self.df['record_date'] = pd.to_datetime(self.df['record_date'])
        self.df.sort_values('record_date', inplace=True)

        self.view.figure.clear()
        ax = self.view.figure.add_subplot(111)

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

        self.view.canvas.mpl_connect('pick_event', self.on_pick)

        self.view.figure.autofmt_xdate()
        self.view.canvas.draw()
    
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
        msg = QMessageBox(self.view)
        msg.setWindowTitle(f"Detalle del Registro - {date}")
        msg.setIcon(QMessageBox.Information)
        
        # Use HTML to format the message content with colors and styles
        text_html = f"""
        <h3 style='color: #5DA7A3;'>Resumen de la Sesión</h3>
        <p><b>Fecha:</b> {date}</p>
        <p><b>Nivel de Dolor:</b> <span style='color: #F08080; font-size: 16px;'>{level}/10</span></p>
        <hr>
        <p><b>Notas del paciente:</b><br><i>{comment}</i></p>
        """
        msg.setText(text_html)
        msg.exec()
        