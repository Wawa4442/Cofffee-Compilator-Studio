import os
import sys
import subprocess
from PySide6.QtWidgets import (
    QMainWindow, QTextEdit, QTabWidget, QToolBar, QSplitter,
    QStatusBar, QFileDialog, QMessageBox, QApplication
)
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import Qt
# Asegúrate de que editor.py exista y tenga la clase EditorCodigo
from editor import EditorCodigo

class VentanaPrincipal(QMainWindow):
    def __init__(self, archivo_inicial=None):
        super().__init__()

        self.setWindowTitle("Coffee Compiler Studio - UAA 2026")
        self.resize(1200, 900)

        # --- Widget Central: Pestañas ---
        self.tabs_editor = QTabWidget()
        self.tabs_editor.setTabsClosable(True)
        self.tabs_editor.tabCloseRequested.connect(self.cerrar_pestana)

        # --- Paneles de Análisis ---
        self.tabs_analisis = QTabWidget()
        self.res_lexico = QTextEdit()
        self.res_sintactico = QTextEdit()
        self.res_semantico = QTextEdit()
        self.res_intermedio = QTextEdit()
        self.tabla_simbolos = QTextEdit()

        for panel, nombre in [(self.res_lexico, "Léxico"), (self.res_sintactico, "Sintáctico"),
                             (self.res_semantico, "Semántico"), (self.res_intermedio, "Intermedio"),
                             (self.tabla_simbolos, "Tabla Símbolos")]:
            panel.setReadOnly(True)
            self.tabs_analisis.addTab(panel, nombre)

        # --- Paneles Inferiores ---
        self.tabs_inferiores = QTabWidget()
        self.consola_errores = QTextEdit()
        self.salida_ejecucion = QTextEdit()
        self.tabs_inferiores.addTab(self.consola_errores, "Lista de Errores")
        self.tabs_inferiores.addTab(self.salida_ejecucion, "Resultado de Ejecución")

        # --- Layout ---
        self.splitter_vertical = QSplitter(Qt.Vertical)
        self.splitter_vertical.addWidget(self.tabs_analisis)
        self.splitter_vertical.addWidget(self.tabs_inferiores)

        self.splitter_horizontal = QSplitter(Qt.Horizontal)
        self.splitter_horizontal.addWidget(self.tabs_editor)
        self.splitter_horizontal.addWidget(self.splitter_vertical)
        self.splitter_horizontal.setStretchFactor(0, 3)

        self.setCentralWidget(self.splitter_horizontal)

        self.crear_menus()
        self.crear_toolbar()
        self.setStatusBar(QStatusBar())

        # LÓGICA DE APERTURA INICIAL
        if archivo_inicial:
            self.cargar_archivo_en_pestana(archivo_inicial)
        else:
            self.nuevo_archivo()

    # ======================
    # LÓGICA DE VENTANAS (PROYECTOS)
    # ======================

    def lanzar_nueva_instancia(self, ruta_archivo):
        """Lanza una nueva ventana del IDE con un archivo específico"""
        script_actual = sys.argv[0]
        # Usamos sys.executable para asegurar que use el mismo Python
        subprocess.Popen([sys.executable, script_actual, ruta_archivo])

    def nuevo_proyecto(self):
        """Crea un archivo físico y lo abre en una ventana nueva"""
        nombre, _ = QFileDialog.getSaveFileName(
            self, "Crear Nuevo Proyecto Coffee", "", "Coffee Files (*.ccs)"
        )
        if nombre:
            if not nombre.lower().endswith('.ccs'):
                nombre += '.ccs'
            try:
                with open(nombre, "w", encoding="utf-8") as f:
                    f.write("// Nuevo Proyecto Coffee\n\nmain() {\n\t\n}")
                self.lanzar_nueva_instancia(nombre)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo crear: {e}")

    def abrir_archivo(self):
        """Abre un archivo existente en una ventana nueva"""
        nombre, _ = QFileDialog.getOpenFileName(
            self, "Abrir Proyecto Coffee", "", "Coffee Files (*.ccs);;Todos (*.*)"
        )
        if nombre:
            self.lanzar_nueva_instancia(nombre)

    # ======================
    # LÓGICA DE PESTAÑAS (DENTRO DE LA VENTANA)
    # ======================

    def nuevo_archivo(self):
        """Crea una pestaña de archivo temporal (Sin título)"""
        nuevo_editor = EditorCodigo()
        nuevo_editor.ruta_archivo = None
        nuevo_editor.textChanged.connect(self.marcar_como_modificado)
        idx = self.tabs_editor.addTab(nuevo_editor, "Sin título.ccs")
        self.tabs_editor.setCurrentIndex(idx)

    def cargar_archivo_en_pestana(self, nombre):
        try:
            with open(nombre, "r", encoding="utf-8") as f:
                contenido = f.read()

            nuevo_editor = EditorCodigo()
            nuevo_editor.setPlainText(contenido)
            nuevo_editor.ruta_archivo = nombre
            nuevo_editor.textChanged.connect(self.marcar_como_modificado)

            idx = self.tabs_editor.addTab(nuevo_editor, os.path.basename(nombre))
            self.tabs_editor.setCurrentIndex(idx)
            self.setWindowTitle(f"Coffee Compiler Studio - {nombre}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar: {e}")

    def obtener_editor_actual(self) -> EditorCodigo:
        return self.tabs_editor.currentWidget()

    def guardar_archivo(self):
        editor = self.obtener_editor_actual()
        if not editor: return
        if editor.ruta_archivo is None:
            self.guardar_como()
        else:
            self._escribir_a_disco(editor, editor.ruta_archivo)

    def guardar_como(self):
        editor = self.obtener_editor_actual()
        if not editor: return
        nombre, _ = QFileDialog.getSaveFileName(
            self, "Guardar como", "", "Coffee Files (*.ccs);;Todos (*.*)"
        )
        if nombre:
            if not nombre.lower().endswith('.ccs'): nombre += '.ccs'
            self._escribir_a_disco(editor, nombre)
            self.tabs_editor.setTabText(self.tabs_editor.currentIndex(), os.path.basename(nombre))
            self.setWindowTitle(f"Coffee Compiler Studio - {nombre}")

    def _escribir_a_disco(self, editor, ruta):
        try:
            with open(ruta, "w", encoding="utf-8") as f:
                f.write(editor.toPlainText())
            editor.ruta_archivo = ruta
            idx = self.tabs_editor.indexOf(editor)
            texto_tab = self.tabs_editor.tabText(idx)
            if texto_tab.endswith("*"):
                self.tabs_editor.setTabText(idx, texto_tab[:-1])
            self.statusBar().showMessage("Guardado", 2000)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al guardar: {e}")

    def marcar_como_modificado(self):
        idx = self.tabs_editor.currentIndex()
        if idx == -1: return
        texto = self.tabs_editor.tabText(idx)
        if not texto.endswith("*"):
            self.tabs_editor.setTabText(idx, texto + "*")

    def cerrar_pestana(self, indice):
        editor = self.tabs_editor.widget(indice)
        texto_tab = self.tabs_editor.tabText(indice)

        if texto_tab.endswith("*"):
            self.tabs_editor.setCurrentIndex(indice)
            resp = QMessageBox.question(
                self, "Guardar cambios",
                f"¿Guardar cambios en '{texto_tab[:-1]} antes de cerrar?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
            )
            if resp == QMessageBox.Save:
                self.guardar_archivo()
            elif resp == QMessageBox.Cancel:
                return False

        self.tabs_editor.removeWidget(editor)
        # Si cerramos la última pestaña, creamos una nueva vacía
        if self.tabs_editor.count() == 0:
            self.nuevo_archivo()
        return True

    def closeEvent(self, event):
        while self.tabs_editor.count() > 0:
            self.tabs_editor.setCurrentIndex(0)
            if not self.cerrar_pestana(0):
                event.ignore()
                return
        event.accept()

    # ======================
    # MENÚS Y INTERFAZ
    # ======================

    def crear_menus(self):
        archivo = self.menuBar().addMenu("&Archivo")

        # Nuevo Proyecto
        acc_proy = QAction("Nuevo Proyecto (Ventana Nueva)", self)
        acc_proy.setShortcut("Ctrl+Shift+N")
        acc_proy.triggered.connect(self.nuevo_proyecto)
        archivo.addAction(acc_proy)

        # Abrir (Ahora en ventana nueva)
        acc_abrir = QAction("Abrir Proyecto...", self)
        acc_abrir.setShortcut("Ctrl+O")
        acc_abrir.triggered.connect(self.abrir_archivo)
        archivo.addAction(acc_abrir)

        archivo.addSeparator()

        # Nuevo Archivo (Pestaña)
        acc_nuevo = QAction("Nuevo Archivo (Pestaña)", self)
        acc_nuevo.setShortcut("Ctrl+N")
        acc_nuevo.triggered.connect(self.nuevo_archivo)
        archivo.addAction(acc_nuevo)

        archivo.addAction(QAction("Guardar", self, shortcut="Ctrl+S", triggered=self.guardar_archivo))
        archivo.addAction(QAction("Guardar como...", self, shortcut="Ctrl+Shift+S", triggered=self.guardar_como))

        archivo.addSeparator()
        archivo.addAction(QAction("Cerrar Pestaña", self, shortcut="Ctrl+W", triggered=lambda: self.cerrar_pestana(self.tabs_editor.currentIndex())))
        archivo.addAction(QAction("Salir", self, shortcut="Ctrl+Q", triggered=self.close))

        ver = self.menuBar().addMenu("&Ver")
        ver.addAction(QAction("Aumentar Zoom", self, shortcut="Ctrl++", triggered=lambda: self.obtener_editor_actual().zoomIn(2)))
        ver.addAction(QAction("Disminuir Zoom", self, shortcut="Ctrl+-", triggered=lambda: self.obtener_editor_actual().zoomOut(2)))

    def wheelEvent(self, event):
        if event.modifiers() == Qt.ControlModifier:
            ed = self.obtener_editor_actual()
            if ed:
                if event.angleDelta().y() > 0: ed.zoomIn(2)
                else: ed.zoomOut(2)
        else:
            super().wheelEvent(event)

    def crear_toolbar(self):
        toolbar = QToolBar("Main")
        self.addToolBar(toolbar)
        for f in ["Léxico", "Sintáctico", "Semántico", "Intermedio", "Ejecutar"]:
            toolbar.addAction(QAction(f, self))

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Si hay un argumento, es la ruta de un archivo a abrir
    archivo_a_cargar = sys.argv[1] if len(sys.argv) > 1 and os.path.exists(sys.argv[1]) else None

    window = VentanaPrincipal(archivo_inicial=archivo_a_cargar)
    window.show()
    sys.exit(app.exec())
