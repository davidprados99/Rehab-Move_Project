from PySide6.QtWidgets import QFrame, QGraphicsDropShadowEffect, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel,  QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap, QColor

class LoginView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rehab & Move - Login")
        self.setMinimumWidth(300)
        self.setMinimumHeight(200)
        self.setWindowIcon(QIcon("assets/logo_Rehab_Move.png"))
        self.init_ui()

    def init_ui(self):
        self.setObjectName("MainWin")
        main_layout = QVBoxLayout(self)

        # Tarjeta blanca
        self.card = QFrame()
        self.card.setObjectName("LoginCard") 
        self.card.setFixedWidth(320)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 30))
        self.card.setGraphicsEffect(shadow)

        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(30, 40, 30, 40)
        card_layout.setSpacing(15)

        # Logo
        self.logo_label = QLabel()
        pixmap = QPixmap("assets/logo_Rehab_Move.png")
        self.logo_label.setPixmap(pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.logo_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.logo_label)

        # Title
        self.title = QLabel("¡Bienvenido!")
        self.title.setObjectName("WelcomeText")
        self.title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.title)

        # Inptuts
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Correo electrónico")
        card_layout.addWidget(self.email_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.Password)
        card_layout.addWidget(self.password_input)

        # Button
        self.login_btn = QPushButton("Entrar")
        self.login_btn.setObjectName("LoginBtn")
        card_layout.addWidget(self.login_btn)

        #Canel button
        self.cancel_btn = QPushButton("Cancelar")
        self.cancel_btn.setObjectName("CancelBtn")
        card_layout.addWidget(self.cancel_btn)

        main_layout.addWidget(self.card)
        