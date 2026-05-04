import sys
from PyQt6.QtWidgets import QApplication
from gui import MainApp

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainApp()
    window.resize(900, 600)
    window.show()

    sys.exit(app.exec())