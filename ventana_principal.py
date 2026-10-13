import os
import sys

from PySide6.QtWidgets import (
    QMainWindow, QTextEdit, QTabWidget, QToolBar,
    QSplitter, QStatusBar, QFileDialog,
    QMessageBox, QApplication,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QTreeWidget, QTreeWidgetItem  # Agregados para el AST visual
)

from PySide6.QtGui import QAction, QFont, QIcon
from PySide6.QtCore import Qt, QSize

from editor import EditorCodigo
from lexer import Lexer
from parser import Parser  # Importamos nuestro nuevo analizador sintáctico
from semantic_analyzer import SemanticAnalyzer


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

        self.res_lexico = QTableWidget()
        self.res_lexico.setColumnCount(3)
        self.res_lexico.setHorizontalHeaderLabels(["Tipo", "Lexema", "Posición [F:C]"])
        self.res_lexico.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.res_lexico.setEditTriggers(QTableWidget.NoEditTriggers)
        self.res_lexico.verticalHeader().setVisible(False)

        # CT-11: Reemplazamos QTextEdit por QTreeWidget para el árbol colapsable
        self.res_sintactico = QTreeWidget()
        self.res_sintactico.setHeaderLabel("Árbol Sintáctico Abstracto (AST)")

        # Pestaña Semántico -> QTreeWidget para el Árbol Sintáctico Anotado
        self.res_semantico = QTreeWidget()
        self.res_semantico.setHeaderLabel("Árbol Sintáctico Anotado (AST + Semántica)")

        self.res_intermedio = QTextEdit()

        # Pestaña Tabla de Símbolos -> QTableWidget estructurado
        self.tabla_simbolos = QTableWidget()
        self.tabla_simbolos.setColumnCount(4)
        self.tabla_simbolos.setHorizontalHeaderLabels([
            "Identificador", "Tipo", "Líneas", "Offset (bytes)"
        ])
        self.tabla_simbolos.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tabla_simbolos.horizontalHeader().setStretchLastSection(True)
        self.tabla_simbolos.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla_simbolos.verticalHeader().setVisible(False)

# INFERIOR

        self.tabs_inferiores = QTabWidget()

        self.consola_errores = QTextEdit()
        self.salida_ejecucion = QTextEdit()

# CONFIG TEXTO

        fuente = QFont("Consolas", 10)
        self.res_lexico.setFont(fuente)
        self.res_sintactico.setFont(fuente)
        self.res_semantico.setFont(fuente)
        self.tabla_simbolos.setFont(fuente)

        for panel in [
            self.res_intermedio,
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

        splitterH.setStretchFactor(0,1)
        splitterH.setStretchFactor(1,1)
        splitterH.setSizes([600, 600])

        self.setCentralWidget(splitterH)

        self.crear_menus()
        self.crear_toolbar_archivo()
        self.crear_toolbar()

        self.setStatusBar(QStatusBar())

        self.tabs_editor.currentChanged.connect(self.invalidar_resultados)
        self.invalidar_resultados()
        self.nuevo_archivo()

# NUEVO

    def nuevo_archivo(self):

        editor = EditorCodigo()
        editor.ruta_archivo = None
        editor.textChanged.connect(self.marcar_modificado)
        editor.textChanged.connect(self.invalidar_resultados)
        editor.cursorPositionChanged.connect(self.actualizar_estado)
        i = self.tabs_editor.addTab(editor,"Sin titulo.ccs")
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
            ed = self.tabs_editor.widget(i)
            if hasattr(ed,"ruta_archivo"):
                if ed.ruta_archivo == nombre:
                    self.tabs_editor.setCurrentIndex(i)
                    return

        with open(nombre,"r",encoding="utf8") as f:
            texto = f.read()

        editor = EditorCodigo()
        editor.setPlainText(texto)
        editor.ruta_archivo = nombre
        editor.textChanged.connect(self.marcar_modificado)
        editor.textChanged.connect(self.invalidar_resultados)
        editor.cursorPositionChanged.connect(self.actualizar_estado)

        i = self.tabs_editor.addTab(
            editor,
            os.path.basename(nombre)
        )

        self.tabs_editor.setCurrentIndex(i)

# EDITOR ACTUAL

    def obtener_editor_actual(self):
        return self.tabs_editor.currentWidget()

# GUARDAR

    def guardar_archivo(self):

        ed = self.obtener_editor_actual()
        if not ed:return

        if ed.ruta_archivo == None:
            self.guardar_como()
            return

        self._guardar(ed,ed.ruta_archivo)

    def guardar_como(self):

        ed = self.obtener_editor_actual()
        if not ed:return

        nombre,_ = QFileDialog.getSaveFileName(
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

        ed.ruta_archivo = ruta
        i = self.tabs_editor.indexOf(ed)
        self.tabs_editor.setTabText(
            i,
            os.path.basename(ruta)
        )

# MODIFICADO

    def marcar_modificado(self):

        i = self.tabs_editor.currentIndex()
        if i == -1:return
        texto = self.tabs_editor.tabText(i)
        if not texto.endswith("*"):
            self.tabs_editor.setTabText(i,texto+"*")

# CERRAR PESTAÑA

    def cerrar_pestana(self,i):

        if i<0:return
        self.tabs_editor.setCurrentIndex(i)
        texto = self.tabs_editor.tabText(i)

        if texto.endswith("*"):
            r = QMessageBox.question(
                self,
                "Guardar cambios",
                f"¿Guardar cambios en '{texto[:-1]}'?",
                QMessageBox.Save|
                QMessageBox.Discard|
                QMessageBox.Cancel
            )

            if r == QMessageBox.Save:
                self.guardar_archivo()
            elif r == QMessageBox.Cancel:
                return

        self.tabs_editor.removeTab(i)

# CERRAR PROGRAMA

    def closeEvent(self,event):

        for i in range(self.tabs_editor.count()):
            texto = self.tabs_editor.tabText(i)
            if texto.endswith("*"):
                self.tabs_editor.setCurrentIndex(i)
                r = QMessageBox.question(
                    self,
                    "Guardar cambios",
                    f"¿Guardar cambios en '{texto[:-1]}'?",
                    QMessageBox.Save|
                    QMessageBox.Discard|
                    QMessageBox.Cancel
                )

                if r == QMessageBox.Save:
                    self.guardar_archivo()
                elif r == QMessageBox.Cancel:
                    event.ignore()
                    return

        event.accept()

# LINEA COLUMNA

    def actualizar_estado(self):

        ed = self.obtener_editor_actual()
        if not ed:return
        c = ed.textCursor()
        self.statusBar().showMessage(
            f"Línea {c.blockNumber()+1} | Columna {c.columnNumber()+1}"
        )

# 🔥 ANALISIS LEXICO

    def invalidar_resultados(self, *_):
        self.res_lexico.setRowCount(0)
        self.res_sintactico.clear()
        self.res_semantico.clear()
        self.tabla_simbolos.setRowCount(0)
        self.consola_errores.clear()
        self.ast_original = None
        self.ast_anotado = None
        self.tabla_resultado = None
        self.errores_lexicos = []
        self.errores_sintacticos = []
        self.errores_semanticos = []

    def analisis_lexico(self):

        self.invalidar_resultados()
        editor = self.obtener_editor_actual()
        if not editor:
            return

        codigo = editor.toPlainText()
        lexer = Lexer(codigo)
        tokens, errores = lexer.analizar()
        self.errores_lexicos = list(errores)

        tokens_validos = [t for t in tokens if t.tipo != "COMENTARIO"]

        self.res_lexico.setRowCount(0)
        self.res_lexico.setRowCount(len(tokens_validos))

        texto_tokens = ""

        for row, t in enumerate(tokens_validos):
            self.res_lexico.setItem(row, 0, QTableWidgetItem(t.tipo))
            self.res_lexico.setItem(row, 1, QTableWidgetItem(t.valor))
            self.res_lexico.setItem(row, 2, QTableWidgetItem(f"[{t.linea}:{t.columna}]"))

            texto_tokens += f"{t.tipo}('{t.valor}') [{t.linea}:{t.columna}]\n"

        # Limpiar la consola antes de mostrar errores
        self.consola_errores.clear()
        lista_errores = []

        for val, linea, col in errores:
            lista_errores.append(f"Error Léxico: '{val}' no reconocido en línea {linea}, columna {col}")

        if lista_errores:
            self.consola_errores.setPlainText("\n".join(lista_errores))
            self.statusBar().showMessage("Análisis Léxico finalizado con errores.", 5000)
        else:
            self.statusBar().showMessage("Análisis Léxico completado sin errores.", 5000)

        # Retornamos tokens y errores para que el sintáctico los pueda usar en cadena
        return tokens_validos, errores

# 🔥 ANALISIS SINTACTICO

    def analisis_sintactico(self):
        # Primero ejecutamos el léxico para obtener los tokens más recientes
        resultado_lexico = self.analisis_lexico()
        if not resultado_lexico:
            return

        tokens, errores_lexicos = resultado_lexico

        # Iniciamos el parser
        parser = Parser(tokens)
        arbol, errores_sintacticos = parser.analizar()
        self.ast_original = arbol
        self.errores_sintacticos = list(errores_sintacticos)

        # Limpiamos el árbol visual anterior
        self.res_sintactico.clear()

        # Función recursiva para dibujar los nodos en el QTreeWidget
        def construir_arbol_visual(nodo_ast, item_padre):
            for hijo in nodo_ast.hijos:
                hijo_item = QTreeWidgetItem([hijo.nombre])
                item_padre.addChild(hijo_item)
                # Llamada recursiva para los hijos del hijo
                construir_arbol_visual(hijo, hijo_item)

        # Si se generó el árbol raíz, lo dibujamos
        if arbol:
            raiz_item = QTreeWidgetItem([arbol.nombre])
            self.res_sintactico.addTopLevelItem(raiz_item)
            construir_arbol_visual(arbol, raiz_item)
            # Expandir todo para que el usuario lo vea inmediatamente
            self.res_sintactico.expandAll()

        # Consolidar errores en la consola
        texto_errores = self.consola_errores.toPlainText()

        if errores_sintacticos:
            if texto_errores:
                texto_errores += "\n\n"
            texto_errores += "--- ERRORES SINTÁCTICOS ---\n"
            for msg, linea, col in errores_sintacticos:
                texto_errores += f"{msg} en línea {linea}, columna {col}\n"

            self.consola_errores.setPlainText(texto_errores)
            self.statusBar().showMessage("Análisis Sintáctico finalizado con errores (Modo Pánico activado).", 5000)
        elif not errores_lexicos:
            self.statusBar().showMessage("Análisis Sintáctico completado. ¡Estructura validada al 100%!", 5000)

        # Cambiamos automáticamente a la pestaña del Sintáctico
        self.tabs_analisis.setCurrentIndex(1)
        return arbol, errores_sintacticos, errores_lexicos

# 🔥 ANALISIS SEMANTICO

    def analisis_semantico(self):
        # 1. Ejecutar análisis sintáctico previo para validar y obtener AST
        resultado_sintactico = self.analisis_sintactico()
        if not resultado_sintactico:
            return

        arbol, errores_sintacticos, errores_lexicos = resultado_sintactico
        if not arbol:
            return
        if errores_lexicos or errores_sintacticos:
            self.statusBar().showMessage(
                "Análisis semántico pendiente: corrija los errores léxicos y sintácticos.", 5000
            )
            return

        # 2. Ejecutar analizador semántico sobre el AST
        analyzer = SemanticAnalyzer()
        ast_anotado, tabla, errores_semanticos = analyzer.analizar(arbol)
        self.ast_anotado = ast_anotado
        self.tabla_resultado = tabla
        self.errores_semanticos = list(errores_semanticos)

        # 3. Limpiar y dibujar Árbol Sintáctico Anotado en QTreeWidget
        self.res_semantico.clear()

        def construir_arbol_anotado(nodo, item_padre):
            for hijo in nodo.hijos:
                texto = hijo.nombre
                etiquetas = []
                if hijo.tipo_dato:
                    if hijo.tipo_dato == "ERROR_TYPE":
                        etiquetas.append("Tipo: [ERROR]")
                    else:
                        etiquetas.append(f"Tipo: {hijo.tipo_dato}")
                if hijo.valor_constante is not None:
                    etiquetas.append(f"Valor: {hijo.valor_constante}")
                if hijo.dtype:
                    etiquetas.append(f"dtype: {hijo.dtype}")
                if hijo.conversion:
                    etiquetas.append(f"Conversión: {hijo.conversion}")

                if etiquetas:
                    texto += f"  -->  [{', '.join(etiquetas)}]"

                hijo_item = QTreeWidgetItem([texto])
                item_padre.addChild(hijo_item)
                construir_arbol_anotado(hijo, hijo_item)

        if ast_anotado:
            texto_raiz = ast_anotado.nombre
            if ast_anotado.tipo_dato:
                texto_raiz += f"  -->  [Tipo: {ast_anotado.tipo_dato}]"
            raiz_item = QTreeWidgetItem([texto_raiz])
            self.res_semantico.addTopLevelItem(raiz_item)
            construir_arbol_anotado(ast_anotado, raiz_item)
            self.res_semantico.expandAll()

        # 4. Actualizar Tabla de Símbolos en QTableWidget
        simbolos = tabla.obtener_simbolos()
        self.tabla_simbolos.setRowCount(0)
        self.tabla_simbolos.setRowCount(len(simbolos))
        for row, s in enumerate(simbolos):
            self.tabla_simbolos.setItem(row, 0, QTableWidgetItem(s.nombre))
            self.tabla_simbolos.setItem(row, 1, QTableWidgetItem(s.tipo))
            self.tabla_simbolos.setItem(row, 2, QTableWidgetItem(s.lineas_str()))
            self.tabla_simbolos.setItem(row, 3, QTableWidgetItem(f"{s.offset} B"))

        # 5. Consolidar y categorizar errores en la consola
        secciones_errores = []
        if errores_lexicos:
            secciones_errores.append("=== ERRORES LÉXICOS ===")
            for val, lin, col in errores_lexicos:
                secciones_errores.append(f"Error Léxico: '{val}' no reconocido en línea {lin}, columna {col}")

        if errores_sintacticos:
            if secciones_errores:
                secciones_errores.append("")
            secciones_errores.append("=== ERRORES SINTÁCTICOS ===")
            for msg, lin, col in errores_sintacticos:
                secciones_errores.append(f"{msg} en línea {lin}, columna {col}")

        if errores_semanticos:
            if secciones_errores:
                secciones_errores.append("")
            secciones_errores.append("=== ERRORES SEMÁNTICOS ===")
            for msg, lin, col in errores_semanticos:
                secciones_errores.append(f"Error Semántico: {msg} en línea {lin}, columna {col}")

        if secciones_errores:
            self.consola_errores.setPlainText("\n".join(secciones_errores))
            self.statusBar().showMessage(f"Análisis Semántico finalizado con {len(errores_semanticos)} error(es) semántico(s).", 5000)
        else:
            self.consola_errores.setPlainText("¡Compilación exitosa! Estructura y semántica validadas al 100% (0 errores).")
            self.statusBar().showMessage("Análisis Semántico completado con éxito. ¡0 errores!", 5000)

        # Cambiamos automáticamente a la pestaña de Semántico
        self.tabs_analisis.setCurrentIndex(2)


# MENUS

    def crear_menus(self):

        archivo = self.menuBar().addMenu("&Archivo")

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

        compilar = self.menuBar().addMenu("&Compilar")
        self.agregar_fases(compilar)

# VER MENU

        ver = self.menuBar().addMenu("&Ver")

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

        toolbar_archivo = QToolBar("Archivo")
        toolbar_archivo.setIconSize(QSize(36, 36))
        toolbar_archivo.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.addToolBar(Qt.TopToolBarArea, toolbar_archivo)

        acciones = [
            ("assets/file_new.png","Nuevo Archivo",self.nuevo_archivo),
            ("assets/file_open.png","Abrir",self.abrir_archivo),
            ("assets/file_save.png","Guardar",self.guardar_archivo),
            ("assets/file_save_as.png","Guardar como",self.guardar_como)
        ]

        for icono, nombre, func in acciones:
            accion = QAction(QIcon(icono), nombre, self)
            accion.triggered.connect(func)
            toolbar_archivo.addAction(accion)

# TOOLBAR

    def crear_toolbar(self):

        toolbar = QToolBar("Compilación")
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

                if f["nombre"] == "Léxico":
                    accion.triggered.connect(self.analisis_lexico)
                elif f["nombre"] == "Sintáctico":
                    accion.triggered.connect(self.analisis_sintactico)
                elif f["nombre"] == "Semántico":
                    accion.triggered.connect(self.analisis_semantico)

                objeto.addAction(accion)


if __name__=="__main__":

    app = QApplication(sys.argv)
    w = VentanaPrincipal()
    w.show()
    sys.exit(app.exec())
