from PySide6.QtWidgets import QDialog,QVBoxLayout,QLabel, QPushButton
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl
from PySide6.QtGui import QIcon
from utils import resource_path

class VideoDialog(QDialog):
    def __init__(self,name, description, video_url, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Video del ejercicio")
        self.setWindowIcon(QIcon(resource_path("assets/logo_Rehab_Move.png")))
        self.setMinimumSize(800, 600)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        # Name
        self.name_label = QLabel(name.upper())
        self.name_label.setObjectName("ExerciseTitle") 
        self.name_label.setWordWrap(True)
        layout.addWidget(self.name_label)

        # Description
        self.desc_label = QLabel(description)
        self.desc_label.setObjectName("ExerciseDescription") 
        self.desc_label.setWordWrap(True)
        layout.addWidget(self.desc_label)

        # Video
        self.video_web = QWebEngineView()
        self.video_web.setObjectName("VideoPlayer") 
        self.video_web.load(QUrl(video_url))
        layout.addWidget(self.video_web, stretch=1)

        # Button
        self.close_btn = QPushButton("Cerrar")
        self.close_btn.setObjectName("CancelBtn")
        self.close_btn.clicked.connect(self.accept)
        layout.addWidget(self.close_btn)
