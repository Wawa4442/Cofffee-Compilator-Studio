import os
from PySide6.QtWidgets import (QMainWindow, QTextEdit, QTabWidget, QVBoxLayout,
                             QWidget, QToolBar, QSplitter, QStatusBar, QFileDialog)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt
from editor import EditorCodigo

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IDE de Compiladores - UAA 2026")
        self.resize(1100, 800)

        # Splitters para organizar la pantalla
        self.splitter_horizontal = QSplitter(Qt.Horizontal)
        self.splitter_vertical = QSplitter(Qt.Vertical)

        # Panel Izquierdo: Editor (Requerimientos 3.4, 3.7, 3.8)
        self.editor = EditorCodigo()
        self.editor.cursorPositionChanged.connect(self.actualizar_estado)

        # Panel Derecho: Resultados de Análisis (Requerimientos 3.2 a 5)
        self.tabs_analisis = QTabWidget()
        self.res_lexico = QTextEdit()
        self.res_sintactico = QTextEdit()
        self.res_semantico = QTextEdit()
        self.res_intermedio = QTextEdit()
        self.tabla_simbolos = QTextEdit()

        self.tabs_analisis.addTab(self.res_lexico, "Léxico")
        self.tabs_analisis.addTab(self.res_sintactico, "Sintáctico")
        self.tabs_analisis.addTab(self.res_semantico, "Semántico")
        self.tabs_analisis.addTab(self.res_intermedio, "Código Intermedio")
        self.tabs_analisis.addTab(self.tabla_simbolos, "Tabla Símbolos")

        # Panel Inferior: Errores y Ejecución (Requerimientos 7 y 8)
        self.tabs_inferiores = QTabWidget()
        self.consola_errores = QTextEdit()
        self.salida_ejecucion = QTextEdit()

        self.tabs_inferiores.addTab(self.consola_errores, "Lista de Errores")
        self.tabs_inferiores.addTab(self.salida_ejecucion, "Resultado de Ejecución")

        # Ensamblaje de la Interfaz
        self.splitter_vertical.addWidget(self.tabs_analisis)
        self.splitter_vertical.addWidget(self.tabs_inferiores)

        self.splitter_horizontal.addWidget(self.editor)
        self.splitter_horizontal.addWidget(self.splitter_vertical)
        self.splitter_horizontal.setStretchFactor(0, 3)

        self.setCentralWidget(self.splitter_horizontal)

        self.crear_menus()
        self.crear_toolbar()
        self.setStatusBar(QStatusBar())

    def crear_menus(self):
        # Menú Archivo (Requerimiento 2.1)
        archivo = self.menuBar().addMenu("&Archivo")
        for txt in ["Nuevo", "Abrir", "Cerrar", "Guardar", "Guardar como"]:
            archivo.addAction(QAction(txt, self))
        archivo.addSeparator()
        archivo.addAction(QAction("Salir", self, triggered=self.close))

        # Menú Compilar (Requerimiento 2.2)
        compilar = self.menuBar().addMenu("&Compilar")
        self.agregar_fases(compilar)

    def crear_toolbar(self):
        # Barra de botones (Requerimiento 2.8)
        toolbar = QToolBar("Compilación")
        self.addToolBar(toolbar)
        self.agregar_fases(toolbar)

    def agregar_fases(self, objeto):
        fases = ["Léxico", "Sintáctico", "Semántico", "Intermedio", "Ejecutar"]
        for f in fases:
            accion = QAction(f, self)
            # Aquí conectarás luego con os.system() para llamar al compilador
            objeto.addAction(accion)

    def actualizar_estado(self):
        # Actualizar Columna (Requerimiento 3.8)
        cursor = self.editor.textCursor()
        linea = cursor.blockNumber() + 1
        columna = cursor.columnNumber() + 1
        self.statusBar().showMessage(f"Línea: {linea} | Columna: {columna}")
