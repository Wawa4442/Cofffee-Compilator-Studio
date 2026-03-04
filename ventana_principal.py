import os
import sys

from PySide6.QtWidgets import (
    QMainWindow, QTextEdit, QTabWidget, QToolBar,
    QSplitter, QStatusBar, QFileDialog,
    QMessageBox, QApplication
)

from PySide6.QtGui import QAction, QFont, QIcon
from PySide6.QtCore import Qt, QSize

from editor import EditorCodigo


class VentanaPrincipal(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Coffee Compiler Studio")
        self.resize(1200,900)


# EDITOR

        self.tabs_editor = QTabWidget()
        self.tabs_editor.setTabsClosable(True)
        self.tabs_editor.tabCloseRequested.connect(self.cerrar_pestana)


# ANALISIS

        self.tabs_analisis = QTabWidget()

        self.res_lexico = QTextEdit()
        self.res_sintactico = QTextEdit()
        self.res_semantico = QTextEdit()
        self.res_intermedio = QTextEdit()
        self.tabla_simbolos = QTextEdit()


# INFERIOR

        self.tabs_inferiores = QTabWidget()

        self.consola_errores = QTextEdit()
        self.salida_ejecucion = QTextEdit()


# CONFIG TEXTO

        fuente = QFont("Consolas",10)

        for panel in [

            self.res_lexico,
            self.res_sintactico,
            self.res_semantico,
            self.res_intermedio,
            self.tabla_simbolos,
            self.consola_errores,
            self.salida_ejecucion

        ]:

            panel.setReadOnly(True)
            panel.setFont(fuente)
            panel.setLineWrapMode(QTextEdit.NoWrap)


# TABS

        self.tabs_analisis.addTab(self.res_lexico,"Léxico")
        self.tabs_analisis.addTab(self.res_sintactico,"Sintáctico")
        self.tabs_analisis.addTab(self.res_semantico,"Semántico")
        self.tabs_analisis.addTab(self.res_intermedio,"Código Intermedio")
        self.tabs_analisis.addTab(self.tabla_simbolos,"Tabla Símbolos")

        self.tabs_inferiores.addTab(self.consola_errores,"Errores")
        self.tabs_inferiores.addTab(self.salida_ejecucion,"Ejecución")


# LAYOUT

        splitterV = QSplitter(Qt.Vertical)
        splitterV.addWidget(self.tabs_analisis)
        splitterV.addWidget(self.tabs_inferiores)

        splitterH = QSplitter(Qt.Horizontal)
        splitterH.addWidget(self.tabs_editor)
        splitterH.addWidget(splitterV)

        splitterH.setStretchFactor(0,3)

        self.setCentralWidget(splitterH)


        self.crear_menus()
        self.crear_toolbar_archivo()
        self.crear_toolbar()

        self.setStatusBar(QStatusBar())

        self.nuevo_archivo()



# NUEVO

    def nuevo_archivo(self):

        editor = EditorCodigo()

        editor.ruta_archivo = None

        editor.textChanged.connect(self.marcar_modificado)
        editor.cursorPositionChanged.connect(self.actualizar_estado)

        i=self.tabs_editor.addTab(editor,"Sin titulo.ccs")

        self.tabs_editor.setCurrentIndex(i)



# ABRIR

    def abrir_archivo(self):

        nombre,_ = QFileDialog.getOpenFileName(

            self,
            "Abrir",
            "",
            "Archivos (*.ccs *.txt);;Todos (*)"

        )

        if nombre:
            self.cargar_archivo(nombre)



# EVITAR DUPLICADOS

    def cargar_archivo(self,nombre):

        for i in range(self.tabs_editor.count()):

            ed=self.tabs_editor.widget(i)

            if hasattr(ed,"ruta_archivo"):

                if ed.ruta_archivo==nombre:

                    self.tabs_editor.setCurrentIndex(i)
                    return


        with open(nombre,"r",encoding="utf8") as f:
            texto=f.read()


        editor=EditorCodigo()

        editor.setPlainText(texto)

        editor.ruta_archivo=nombre

        editor.textChanged.connect(self.marcar_modificado)
        editor.cursorPositionChanged.connect(self.actualizar_estado)


        i=self.tabs_editor.addTab(
            editor,
            os.path.basename(nombre)
        )

        self.tabs_editor.setCurrentIndex(i)



# EDITOR ACTUAL

    def obtener_editor_actual(self):
        return self.tabs_editor.currentWidget()



# GUARDAR

    def guardar_archivo(self):

        ed=self.obtener_editor_actual()

        if not ed:return

        if ed.ruta_archivo==None:
            self.guardar_como()
            return

        self._guardar(ed,ed.ruta_archivo)



    def guardar_como(self):

        ed=self.obtener_editor_actual()

        if not ed:return

        nombre,_=QFileDialog.getSaveFileName(

            self,
            "Guardar",
            "",
            "Archivos (*.ccs)"
        )

        if nombre:
            self._guardar(ed,nombre)



    def _guardar(self,ed,ruta):

        with open(ruta,"w",encoding="utf8") as f:
            f.write(ed.toPlainText())

        ed.ruta_archivo=ruta

        i=self.tabs_editor.indexOf(ed)

        self.tabs_editor.setTabText(
            i,
            os.path.basename(ruta)
        )



# MODIFICADO

    def marcar_modificado(self):

        i=self.tabs_editor.currentIndex()

        if i==-1:return

        texto=self.tabs_editor.tabText(i)

        if not texto.endswith("*"):
            self.tabs_editor.setTabText(i,texto+"*")



# CERRAR PESTAÑA

    def cerrar_pestana(self,i):

        if i<0:return

        self.tabs_editor.setCurrentIndex(i)

        texto=self.tabs_editor.tabText(i)

        if texto.endswith("*"):

            r=QMessageBox.question(

                self,
                "Guardar cambios",
                f"¿Guardar cambios en '{texto[:-1]}'?",

                QMessageBox.Save|
                QMessageBox.Discard|
                QMessageBox.Cancel
            )

            if r==QMessageBox.Save:
                self.guardar_archivo()

            elif r==QMessageBox.Cancel:
                return


        self.tabs_editor.removeTab(i)



# CERRAR PROGRAMA

    def closeEvent(self,event):

        for i in range(self.tabs_editor.count()):

            texto=self.tabs_editor.tabText(i)

            if texto.endswith("*"):

                self.tabs_editor.setCurrentIndex(i)

                r=QMessageBox.question(

                    self,
                    "Guardar cambios",
                    f"¿Guardar cambios en '{texto[:-1]}'?",

                    QMessageBox.Save|
                    QMessageBox.Discard|
                    QMessageBox.Cancel
                )

                if r==QMessageBox.Save:
                    self.guardar_archivo()

                elif r==QMessageBox.Cancel:
                    event.ignore()
                    return

        event.accept()



# LINEA COLUMNA

    def actualizar_estado(self):

        ed=self.obtener_editor_actual()

        if not ed:return

        c=ed.textCursor()

        self.statusBar().showMessage(
            f"Línea {c.blockNumber()+1} | Columna {c.columnNumber()+1}"
        )



# MENUS

    def crear_menus(self):

        archivo=self.menuBar().addMenu("&Archivo")

        archivo.addAction(
            QAction("Nuevo Archivo",self,
            shortcut="Ctrl+N",
            triggered=self.nuevo_archivo)
        )

        archivo.addAction(
            QAction("Abrir",self,
            shortcut="Ctrl+O",
            triggered=self.abrir_archivo)
        )

        archivo.addSeparator()

        archivo.addAction(
            QAction("Guardar",self,
            shortcut="Ctrl+S",
            triggered=self.guardar_archivo)
        )

        archivo.addAction(
            QAction("Guardar como",self,
            shortcut="Ctrl+Shift+S",
            triggered=self.guardar_como)
        )

        archivo.addSeparator()

        archivo.addAction(
            QAction("Cerrar pestaña",self,
            shortcut="Ctrl+W",
            triggered=lambda:self.cerrar_pestana(
                self.tabs_editor.currentIndex()))
        )

        archivo.addAction(
            QAction("Salir",self,
            shortcut="Ctrl+Q",
            triggered=self.close)
        )


# COMPILAR MENU

        compilar=self.menuBar().addMenu("&Compilar")
        self.agregar_fases(compilar)


# VER MENU

        ver=self.menuBar().addMenu("&Ver")

        ver.addAction(QAction(
            "Zoom +",
            self,
            shortcut="Ctrl++",
            triggered=lambda:self.obtener_editor_actual().zoomIn(2)
        ))

        ver.addAction(QAction(
            "Zoom -",
            self,
            shortcut="Ctrl+-",
            triggered=lambda:self.obtener_editor_actual().zoomOut(2)
        ))

# TOOLBAR ARCHIVOS

    def crear_toolbar_archivo(self):
        """Crea la barra de herramientas para la gestión de archivos con iconos."""
        toolbar_archivo = QToolBar("Archivo")
        toolbar_archivo.setIconSize(QSize(36, 36))

        toolbar_archivo.setToolButtonStyle(Qt.ToolButtonIconOnly)

        self.addToolBar(Qt.TopToolBarArea, toolbar_archivo)

        # 1. Acción Nuevo
        icono_nuevo = QIcon("assets/file_new.png")
        accion_nuevo = QAction(icono_nuevo, "Nuevo Archivo", self)
        accion_nuevo.setShortcut("Ctrl+N")
        accion_nuevo.setToolTip("Crear un nuevo archivo de Coffee (Ctrl+N)")
        accion_nuevo.triggered.connect(self.nuevo_archivo)
        toolbar_archivo.addAction(accion_nuevo)

        # 2. Acción Abrir
        icono_abrir = QIcon("assets/file_open.png")
        accion_abrir = QAction(icono_abrir, "Abrir", self)
        accion_abrir.setShortcut("Ctrl+O")
        accion_abrir.setToolTip("Abrir archivo existente (Ctrl+O)")
        accion_abrir.triggered.connect(self.abrir_archivo)
        toolbar_archivo.addAction(accion_abrir)

        # 3. Acción Guardar
        icono_guardar = QIcon("assets/file_save.png")
        accion_guardar = QAction(icono_guardar, "Guardar", self)
        accion_guardar.setShortcut("Ctrl+S")
        accion_guardar.setToolTip("Guardar archivo actual (Ctrl+S)")
        accion_guardar.triggered.connect(self.guardar_archivo)
        toolbar_archivo.addAction(accion_guardar)

        # 4. Acción Guardar como
        icono_guardar_como = QIcon("assets/file_save_as.png")
        accion_guardar_como = QAction(icono_guardar_como, "Guardar como", self)
        accion_guardar_como.setShortcut("Ctrl+Shift+S")
        accion_guardar_como.setToolTip("Guardar archivo actual con otro nombre (Ctrl+Shift+S)")
        accion_guardar_como.triggered.connect(self.guardar_como)
        toolbar_archivo.addAction(accion_guardar_como)

# TOOLBAR

    def crear_toolbar(self):

        toolbar=QToolBar("Compilación")

        toolbar.setIconSize(QSize(36, 36))
        toolbar.setToolButtonStyle(Qt.ToolButtonIconOnly)

        self.addToolBar(toolbar)

        self.agregar_fases(toolbar)


    def agregar_fases(self,objeto):

        fases = [
                {"nombre": "Léxico", "icono": "assets/lexico.png"},
                {"nombre": "Sintáctico", "icono": "assets/sintactico.png"},
                {"nombre": "Semántico", "icono": "assets/semantico.png"},
                {"nombre": "Intermedio", "icono": "assets/intermedio.png"},
                {"nombre": "Ejecutar", "icono": "assets/ejecutar.png"}
        ]

        for f in fases:
                icono = QIcon(f["icono"])

                accion = QAction(icono, f["nombre"], self)

                accion.setToolTip(f["nombre"])

                objeto.addAction(accion)


if __name__=="__main__":

    app=QApplication(sys.argv)

    w=VentanaPrincipal()

    w.show()

    sys.exit(app.exec())
