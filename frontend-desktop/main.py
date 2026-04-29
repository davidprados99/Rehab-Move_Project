import sys
from PySide6.QtWidgets import QApplication
from controllers.login_controller import LoginController
from PySide6.QtCore import Qt
from utils import resource_path

def load_stylesheet(path):
    """Function to load a stylesheet from a file."""
    with open(path, "r") as f:
        return f.read()

    
def main():
    # Enable high DPI scaling for better appearance on high-resolution displays
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    # 1. Create the application with the system arguments (allows for command line options)
    app = QApplication(sys.argv)
    
    # Load external stylesheet (optional, but recommended for better UI)
    try:
        style = load_stylesheet(resource_path("assets/main_styles.qss"))
        app.setStyleSheet(style)
    except FileNotFoundError:
        print("Stylesheet not found. Continuing with default style.")

    # 2. Instantiate the controller, which will create the view and handle the logic
    controller = LoginController()
    
    # 3. Show the view (the controller has a reference to it)
    controller.view.show()
    
    # 4. Start the event loop (this keeps the application running and responsive)
    sys.exit(app.exec())

if __name__ == "__main__":
    main()