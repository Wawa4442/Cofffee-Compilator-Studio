import os
import sys
import ctypes
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from ventana_principal import VentanaPrincipal

# Registrar un App ID de Windows para que el icono de la barra de tareas no herede el de Python
myappid = 'mycompany.myproduct.subproduct.1'
try:
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except Exception:
    pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion") # Estilo limpio

    base_path = Path(__file__).resolve().parent
    logo_path = os.path.join(base_path, "assets", "Coffee Logo.jpg")
    if not os.path.exists(logo_path):
        logo_path = os.path.join(base_path, "assets", "Coffee Logo.png")
    if not os.path.exists(logo_path):
        logo_path = os.path.join(base_path, "assets", "Coffee Logo.jpeg")

    if os.path.exists(logo_path):
        app.setWindowIcon(QIcon(logo_path))

    window = VentanaPrincipal()
    window.show()
    sys.exit(app.exec())
