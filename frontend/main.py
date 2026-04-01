import sys
from PySide6.QtWidgets import QApplication
from controllers.login_controller import LoginController

def load_stylesheet(path):
    """Function to load a stylesheet from a file."""
    with open(path, "r") as f:
        return f.read()

    
def main():
    # 1. Create the application with the system arguments (allows for command line options)
    app = QApplication(sys.argv)
    
    # Load external stylesheet (optional, but recommended for better UI)
    try:
        style = load_stylesheet("assets/main_styles.qss")
        app.setStyleSheet(style)
    except FileNotFoundError:
        print("Aviso: No se encontró el archivo de estilos.")

    # 2. Instantiate the controller, which will create the view and handle the logic
    controller = LoginController()
    
    # 3. Show the view (the controller has a reference to it)
    controller.view.show()
    
    # 4. Start the event loop (this keeps the application running and responsive)
    sys.exit(app.exec())

if __name__ == "__main__":
    main()