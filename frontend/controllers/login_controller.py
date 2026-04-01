from views.login_view import LoginView
from services.api_client import ApiClient
from views.physio_dashboard import PhysioDashboard
from views.patient_dashboard import PatientDashboard
from PySide6.QtWidgets import QMessageBox

class LoginController:
    def __init__(self):
        self.view = LoginView()
        self.api = ApiClient()
        
        # Connect the login button to the handler
        self.view.login_btn.clicked.connect(self.handle_login)

    def handle_login(self):
        self.view.show()  # Ensure the login view is visible
        email = self.view.email_input.text()
        password = self.view.password_input.text()

        success, message = self.api.login(email, password)

        self.view.email_input.clear()
        self.view.password_input.clear()   

        if success:
            self.view.hide()  # Hide the login view
            print(f"Login exitoso. Rol: {self.api.user_role}")
            # There is where you would navigate to the next screen based on the user role

            if self.api.user_role == "physio":
                print("Navegando al dashboard del fisioterapeuta...")
                self.dashboard = PhysioDashboard(email)
                self.dashboard.show()
            else:
                print("Navegando al dashboard del paciente...")
                self.dashboard = PatientDashboard(email)
                self.dashboard.show()
        else:
            print(f"Error: {message}")
            QMessageBox.critical(self.view, "Error", f"Login fallido: {message}")