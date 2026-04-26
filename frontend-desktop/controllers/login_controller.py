from views.login_view import LoginView
from services.api_client import ApiClient
from views.physio_dashboard import PhysioDashboard
from views.patient_dashboard import PatientDashboard
from PySide6.QtWidgets import QMessageBox
from controllers.physio_controller import PhysioController

class LoginController:
    def __init__(self):
        self.view = LoginView()
        self.api = ApiClient()
        
        # Connect the login button to the handler
        self.view.login_btn.clicked.connect(self.handle_login)
        self.view.cancel_btn.clicked.connect(self.handle_cancel)

    def handle_login(self):
        self.view.show()  # Ensure the login view is visible
        email = self.view.email_input.text()
        password = self.view.password_input.text()

        success, message = self.api.login(email, password)

        self.view.email_input.clear()
        self.view.password_input.clear()   

        if success:
            self.view.hide()  # Hide the login view
            if self.api.user_role == "physio":
                self.controller = PhysioController(self.api)
                self.controller.view.show()
            else:
                self.dashboard = PatientDashboard(self.api)
                self.dashboard.show()
        else:
            QMessageBox.critical(self.view, "Error", f"Login fallido: {message}")
        
    def handle_cancel(self):
        self.view.password_input.clear()
        self.view.close()