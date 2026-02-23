import sys
from PySide6.QtWidgets import QApplication
from ventana_principal import VentanaPrincipal

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion") # Estilo limpio para Linux

    window = VentanaPrincipal()
    window.show()
    sys.exit(app.exec())
