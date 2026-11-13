import os
import sys
import ctypes
from pathlib import Path

# 1. Registrar un App ID de Windows para que el ícono de la barra de tareas no herede el de Python
myappid = 'mycompany.myproduct.subproduct.1'  # Cadena arbitraria
try:
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except Exception:
    pass

from PySide6.QtWidgets import (
    QMainWindow, QTextEdit, QTabWidget, QToolBar,
    QSplitter, QStatusBar, QFileDialog,
    QMessageBox, QApplication, QInputDialog,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QTreeWidget, QTreeWidgetItem  # Agregados para el AST visual
)

from PySide6.QtGui import QAction, QFont, QIcon, QColor
from PySide6.QtCore import Qt, QSize

from editor import EditorCodigo
from lexer import Lexer
from parser import Parser  # Importamos nuestro nuevo analizador sintáctico
from semantic_analyzer import SemanticAnalyzer
from intermedio import GeneradorCodigoIntermedio
from cgen import CodeGeneratorTM
from tm_simulator import TinyMachineSimulator


def obtener_icono(nombre_archivo):
    """Retorna un QIcon asegurando la ruta absoluta hacia la carpeta assets."""
    dir_assets = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
    ruta = os.path.join(dir_assets, nombre_archivo)
    if os.path.exists(ruta):
        return QIcon(ruta)
    return QIcon(os.path.join("assets", nombre_archivo))


class VentanaPrincipal(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Coffee Compiler Studio")
        self.resize(1200,900)

        # 1. ARREGLAR LOGO (Ventana y Barra de Tareas)
        base_path = Path(__file__).resolve().parent
        logo_path = os.path.join(base_path, "assets", "Coffee Logo.jpg")

        if not os.path.exists(logo_path):
            logo_path = os.path.join(base_path, "assets", "Coffee Logo.png")
        if not os.path.exists(logo_path):
            logo_path = os.path.join(base_path, "assets", "Coffee Logo.jpeg")

        if os.path.exists(logo_path):
            self.setWindowIcon(QIcon(logo_path))
            app_inst = QApplication.instance()
            if app_inst:
                app_inst.setWindowIcon(QIcon(logo_path))
        else:
            print(f"ERROR: No se encontró el logo en {logo_path}")

        # 2. NUEVA PALETA CÁLIDA, CLARA Y DE ALTO CONTRASTE (Light/Medium "Coffee Theme")
        self.setStyleSheet("""
            /* Fondo general más claro (Canela / Arena suave) */
            QMainWindow { 
                background-color: #3b2314; 
                color: #fff8f2; 
            }
            
            /* Barra de menús y toolbar en café medio que destaque */
            QMenuBar { 
                background-color: #2b170c; 
                color: #ffd8a8; 
                border-bottom: 2px solid #5a3825; 
                font-weight: bold;
            }
            QMenuBar::item {
                background-color: transparent;
                color: #ffd8a8;
                padding: 4px 10px;
            }
            QMenuBar::item:selected { 
                background-color: #5a3825; 
                color: #ffffff; 
                border-radius: 4px;
            }
            
            QToolBar { 
                background-color: #4e3223; 
                border: 2px solid #5a3825; 
                border-radius: 6px; 
                padding: 4px;
                margin: 4px;
            }
            QToolBar QToolButton {
                padding: 4px;
                border-radius: 4px;
            }
            QToolBar QToolButton:hover {
                background-color: #6b442e;
            }
            
            /* Panel lateral y principal del editor (Alto Contraste) */
            QTabWidget::pane { 
                border: 3px solid #6b442e; 
                background-color: #1a0d06; 
                border-radius: 6px;
            }
            
            /* Pestañas bien legibles y contrastadas */
            QTabBar::tab { 
                background-color: #2c160b; 
                color: #d2b48c; 
                padding: 8px 16px; 
                border: 2px solid #5a3825; 
                border-bottom: none; 
                border-top-left-radius: 6px; 
                border-top-right-radius: 6px; 
                font-weight: bold;
            }
            QTabBar::tab:selected { 
                background-color: #5a3825; 
                color: #ffffff; 
                border-color: #d4af37; 
                font-weight: bold;
            }
            QTabBar::tab:hover {
                background-color: #4e3223;
                color: #fcece0;
            }
            
            /* El Editor de Código (Oscuro profundo para sintaxis, con bordes cálidos claros) */
            QTextEdit, QPlainTextEdit { 
                background-color: #120602; 
                color: #ffecd1; 
                border: 3px solid #6b442e; 
                border-radius: 6px;
                font-size: 11pt;
                font-family: 'Consolas', 'Courier New', monospace; 
            }
            QTextEdit:focus, QPlainTextEdit:focus { 
                border: 3px solid #ffaa44; /* Borde naranja/dorado encendido al enfocar */
            }

            /* Tablas y visualizadores de análisis (Léxico, sintáctico, etc.) */
            QTableWidget, QTreeWidget, QTreeView {
                background-color: #1a0d06;
                color: #fff3e3;
                border: 3px solid #6b442e;
                gridline-color: #5a3825;
                font-family: 'Consolas', monospace;
            }
            QTreeWidget::item:hover, QTableWidget::item:hover {
                background-color: #3e2511;
            }
            QTreeWidget::item:selected, QTableWidget::item:selected {
                background-color: #8c5230;
                color: #ffffff;
            }
            QHeaderView::section { 
                background-color: #4e3223; 
                color: #ffffff; 
                font-weight: bold;
                border: 1px solid #6b442e; 
                padding: 6px;
            }

            /* Etiquetas de pestañas y textos explicativos */
            QLabel { 
                color: #ffd8a8; 
                font-weight: bold;
                font-size: 10pt;
            }

            /* Botones que de verdad resalten (Terracota y dorado) */
            QPushButton { 
                background-color: #8c5230; 
                color: #ffffff; 
                border: 2px solid #bf7d4e; 
                border-radius: 6px; 
                padding: 8px 16px; 
                font-weight: bold;
            }
            QPushButton:hover { 
                background-color: #a05e38; 
                border-color: #ffd8a8; 
            }
            QPushButton:pressed { 
                background-color: #5a2e16; 
            }

            /* Menús desplegables y cuadros de diálogo */
            QMenu {
                background-color: #2b170c;
                color: #ffd8a8;
                border: 2px solid #5a3825;
            }
            QMenu::item:selected {
                background-color: #5a3825;
                color: #ffffff;
            }
            QDialog, QMessageBox { 
                background-color: #3b2314; 
                color: #fff8f2; 
            }
            QLineEdit {
                background-color: #120602;
                color: #ffecd1;
                border: 2px solid #6b442e;
                border-radius: 4px;
                padding: 4px;
                font-family: 'Consolas', monospace;
            }
            QLineEdit:focus {
                border: 2px solid #ffaa44;
            }
            QStatusBar {
                background-color: #2b170c;
                color: #ffd8a8;
                border-top: 2px solid #5a3825;
                font-weight: bold;
            }
            QSplitter::handle {
                background-color: #5a3825;
            }
            QSplitter::handle:hover {
                background-color: #8c5230;
            }
            QScrollBar:vertical {
                background: #2b170c;
                width: 12px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #5a3825;
                min-height: 20px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover {
                background: #8c5230;
            }
            QScrollBar:horizontal {
                background: #2b170c;
                height: 12px;
                margin: 0px;
            }
            QScrollBar::handle:horizontal {
                background: #5a3825;
                min-width: 20px;
                border-radius: 4px;
            }
            QScrollBar::handle:horizontal:hover {
                background: #8c5230;
            }
        """)

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

        # Pestaña Tabla de Símbolos -> QTableWidget estructurado y desplazable
        self.tabla_simbolos = QTableWidget()
        self.tabla_simbolos.setColumnCount(5)
        self.tabla_simbolos.setHorizontalHeaderLabels([
            "Identificador", "Tipo de Dato", "Líneas de Aparición", "Offset / Desplazamiento (Bytes)", "Estado / Observaciones"
        ])
        header_simbolos = self.tabla_simbolos.horizontalHeader()
        header_simbolos.setSectionResizeMode(QHeaderView.Interactive)
        header_simbolos.setSectionsMovable(True)
        header_simbolos.setStretchLastSection(False)
        self.tabla_simbolos.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla_simbolos.verticalHeader().setVisible(False)
        self.tabla_simbolos.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.tabla_simbolos.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.tabla_simbolos.setHorizontalScrollMode(QTableWidget.ScrollPerPixel)
        self.tabla_simbolos.setVerticalScrollMode(QTableWidget.ScrollPerPixel)
        self.tabla_simbolos.setWordWrap(False)

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

    def analisis_lexico(self):

        editor = self.obtener_editor_actual()
        if not editor:
            return

        # Limpiar salidas previas de código intermedio y ejecución en cada nueva compilación
        self.res_intermedio.clear()
        self.salida_ejecucion.clear()

        codigo = editor.toPlainText()
        lexer = Lexer(codigo)
        tokens, errores = lexer.analizar()

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

    def analisis_sintactico(self, _checked=False, cambiar_pestana=True):
        # Primero ejecutamos el léxico para obtener los tokens más recientes
        resultado_lexico = self.analisis_lexico()
        if not resultado_lexico:
            return

        tokens, errores_lexicos = resultado_lexico

        # Iniciamos el parser
        parser = Parser(tokens)
        arbol, errores_sintacticos = parser.analizar()

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
        else:
            self.statusBar().showMessage("Análisis Sintáctico completado. ¡Estructura validada al 100%!", 5000)

        if cambiar_pestana:
            self.tabs_analisis.setCurrentIndex(1)
        return arbol, errores_sintacticos, errores_lexicos

# 🔥 ANALISIS SEMANTICO

    def analisis_semantico(self, _checked=False, cambiar_pestana=True):
        # 1. Ejecutar análisis sintáctico previo para validar y obtener AST
        resultado_sintactico = self.analisis_sintactico(cambiar_pestana=False)
        if not resultado_sintactico:
            return

        arbol, errores_sintacticos, errores_lexicos = resultado_sintactico
        if not arbol:
            return

        # 2. Ejecutar analizador semántico sobre el AST
        analyzer = SemanticAnalyzer()
        ast_anotado, tabla, errores_semanticos = analyzer.analizar(arbol)

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

        color_error_bg = QColor(80, 25, 20)        # Fondo café/marrón rojizo cálido para duplicados
        color_error_txt = QColor(255, 140, 140)    # Texto salmón claro de alto contraste
        color_valido_txt = QColor(140, 215, 140)   # Texto verde suave para VÁLIDO

        for row, s in enumerate(simbolos):
            item_id = QTableWidgetItem(s.nombre)
            tipo_texto = s.tipo_display() if hasattr(s, "tipo_display") else s.tipo
            item_tipo = QTableWidgetItem(tipo_texto)
            lineas_texto = s.lineas_str()
            item_lineas = QTableWidgetItem(lineas_texto)
            offset_texto = s.offset_str() if hasattr(s, "offset_str") else (f"{s.offset} B" if s.offset is not None else "-")
            item_offset = QTableWidgetItem(offset_texto)
            estado_texto = getattr(s, "estado", "VÁLIDO")
            item_estado = QTableWidgetItem(estado_texto)

            # Tooltips para inspección completa al pasar el cursor
            item_id.setToolTip(f"Identificador: {s.nombre}")
            item_tipo.setToolTip(f"Tipo: {tipo_texto}")
            item_lineas.setToolTip(f"Líneas de aparición de '{s.nombre}':\n{lineas_texto}")
            item_offset.setToolTip(f"Desplazamiento en memoria: {offset_texto}")
            item_estado.setToolTip(f"Estado / Observaciones:\n{estado_texto}")

            es_dup = getattr(s, "es_duplicado", False)
            if es_dup:
                for item in [item_id, item_tipo, item_lineas, item_offset, item_estado]:
                    item.setBackground(color_error_bg)
                    item.setForeground(color_error_txt)
            else:
                item_estado.setForeground(color_valido_txt)

            self.tabla_simbolos.setItem(row, 0, item_id)
            self.tabla_simbolos.setItem(row, 1, item_tipo)
            self.tabla_simbolos.setItem(row, 2, item_lineas)
            self.tabla_simbolos.setItem(row, 3, item_offset)
            self.tabla_simbolos.setItem(row, 4, item_estado)

        # Ajuste dinámico de columnas y filas al contenido para que ningún texto se corte
        self.tabla_simbolos.resizeColumnsToContents()
        self.tabla_simbolos.resizeRowsToContents()

        # Establecer anchos mínimos confortables para que las columnas sean amplias, legibles y desplazables
        anchos_minimos = {0: 120, 1: 130, 2: 260, 3: 160, 4: 240}
        for col_idx, ancho_min in anchos_minimos.items():
            ancho_calculado = self.tabla_simbolos.columnWidth(col_idx)
            self.tabla_simbolos.setColumnWidth(col_idx, max(ancho_calculado + 25, ancho_min))

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
            self.tabs_inferiores.setCurrentIndex(0)
            self.statusBar().showMessage(f"Análisis Semántico finalizado con {len(errores_semanticos)} error(es) semántico(s).", 5000)
        else:
            self.consola_errores.setPlainText("¡Compilación exitosa! Estructura y semántica validadas al 100% (0 errores).")
            self.statusBar().showMessage("Análisis Semántico completado con éxito. ¡0 errores!", 5000)

        if cambiar_pestana:
            self.tabs_analisis.setCurrentIndex(2)

        return ast_anotado, tabla, errores_semanticos, errores_sintacticos, errores_lexicos

# 🔥 GENERACIÓN DE CÓDIGO INTERMEDIO (.ci) Y OBJETO TINY MACHINE (.tm)

    def _obtener_rutas_salida(self):
        """
        Determina las rutas en disco para los archivos .ci y .tm a partir del
        archivo abierto en el editor actual (o en el directorio del proyecto si no se ha guardado).
        """
        ed = self.obtener_editor_actual()
        if ed and getattr(ed, "ruta_archivo", None):
            base, _ = os.path.splitext(ed.ruta_archivo)
        else:
            directorio_base = os.path.dirname(os.path.abspath(__file__))
            base = os.path.join(directorio_base, "programa_actual")
        return base + ".ci", base + ".tm"

    def generar_codigo_intermedio(self, _checked=False, cambiar_pestana=True):
        """
        Ejecuta el pipeline completo de análisis (Léxico -> Sintáctico -> Semántico)
        y, únicamente si existen 0 errores en todas las fases, genera:
          1. El archivo de Código de Tres Direcciones (.ci)
          2. El archivo de Código Objeto para la Tiny Machine (.tm)
        Mostrando el resultado en la pestaña 'Código Intermedio'.
        """
        self.res_intermedio.clear()
        resultado_sem = self.analisis_semantico(cambiar_pestana=False)
        if not resultado_sem:
            return None

        ast_anotado, tabla, errores_sem, errores_sin, errores_lex = resultado_sem
        total_errores = len(errores_lex) + len(errores_sin) + len(errores_sem)

        if total_errores > 0:
            mensaje_bloqueo = (
                "====================================================================\n"
                "  GENERACIÓN DE CÓDIGO CANCELADA: SE DETECTARON ERRORES PREVIOS\n"
                "====================================================================\n"
                f"  - Errores Léxicos:     {len(errores_lex)}\n"
                f"  - Errores Sintácticos: {len(errores_sin)}\n"
                f"  - Errores Semánticos:  {len(errores_sem)}\n\n"
                "Por favor, corrija los errores reportados en la pestaña 'Errores'\n"
                "antes de generar código intermedio (.ci) o código objeto (.tm)."
            )
            self.res_intermedio.setPlainText(mensaje_bloqueo)
            self.tabs_inferiores.setCurrentIndex(0)
            if cambiar_pestana:
                self.tabs_analisis.setCurrentIndex(3)
            self.statusBar().showMessage("Generación de código abortada por errores de análisis.", 5000)
            return None

        ruta_ci, ruta_tm = self._obtener_rutas_salida()

        # 1. Generar Código Intermedio de Tres Direcciones (.ci)
        gen_ci = GeneradorCodigoIntermedio()
        codigo_ci = gen_ci.generarCodigoIntermedio(ast_anotado, ruta_archivo_ci=ruta_ci)

        # 2. Generar Código Objeto para la Tiny Machine (.tm)
        gen_tm = CodeGeneratorTM(tabla_simbolos=tabla, trace_code=True)
        codigo_tm = gen_tm.codeGen(ast_anotado, codefile_path=ruta_tm)

        # 3. Formatear y mostrar ambos resultados en la pestaña 'Código Intermedio'
        vista_combinada = (
            "========================================================================\n"
            f"  1. CÓDIGO OBJETO TINY MACHINE (.tm) -> {os.path.basename(ruta_tm)}\n"
            "========================================================================\n"
            f"{codigo_tm}\n"
            "========================================================================\n"
            f"  2. CÓDIGO INTERMEDIO DE TRES DIRECCIONES (.ci) -> {os.path.basename(ruta_ci)}\n"
            "========================================================================\n"
            f"{codigo_ci}"
        )
        self.res_intermedio.setPlainText(vista_combinada)

        if cambiar_pestana:
            self.tabs_analisis.setCurrentIndex(3)

        self.statusBar().showMessage(
            f"Código generado con éxito: {os.path.basename(ruta_tm)} y {os.path.basename(ruta_ci)}",
            5000
        )
        return ruta_tm, codigo_tm, ruta_ci, codigo_ci

# 🔥 EJECUCIÓN EN EL SIMULADOR TINY MACHINE (TM)

    def ejecutar_programa(self):
        """
        Compila el código actual, verifica que existan 0 errores, genera el
        archivo .tm y lo ejecuta en el simulador de la Tiny Machine (tm_simulator.py),
        interactuando con el usuario para instrucciones IN y mostrando los
        resultados de OUT en la pestaña 'Ejecución'.
        """
        self.salida_ejecucion.clear()

        resultado_gen = self.generar_codigo_intermedio(cambiar_pestana=False)
        if not resultado_gen:
            self.salida_ejecucion.setPlainText(
                "[EJECUCIÓN ABORTADA]\n"
                "No es posible ejecutar la Máquina Virtual Tiny Machine porque el\n"
                "programa contiene errores léxicos, sintácticos o semánticos.\n"
                "Revise la pestaña 'Errores'."
            )
            self.tabs_inferiores.setCurrentIndex(0)
            return

        ruta_tm, codigo_tm, ruta_ci, _ = resultado_gen

        # Enfocar la pestaña de Código Intermedio arriba y Ejecución abajo
        self.tabs_analisis.setCurrentIndex(3)
        self.tabs_inferiores.setCurrentIndex(1)

        simulador = TinyMachineSimulator()
        ok, info = simulador.cargar_archivo_tm(ruta_tm)
        if not ok:
            self.salida_ejecucion.setPlainText(f"[ERROR AL CARGAR ARCHIVO .TM]\n{info}")
            return

        # Callback interactivo para la instrucción RO 'IN' de la Tiny Machine
        def solicitar_entrada_tm(nombre_var, comentario_inst):
            while True:
                texto, aceptado = QInputDialog.getText(
                    self,
                    "Entrada Tiny Machine (Instrucción IN)",
                    f"Ingrese el valor numérico para '{nombre_var}':\n({comentario_inst})"
                )
                if not aceptado:
                    return 0, False
                texto = texto.strip()
                try:
                    valor = float(texto) if "." in texto else int(texto)
                    return valor, True
                except ValueError:
                    QMessageBox.warning(
                        self,
                        "Valor inválido",
                        f"'{texto}' no es un número válido. Ingrese un valor entero o decimal (ej. 10 o 3.14)."
                    )

        # Callback en tiempo real para actualizar la pestaña 'Ejecución'
        def mostrar_linea_ejecucion(linea):
            self.salida_ejecucion.append(linea)
            QApplication.processEvents()

        self.salida_ejecucion.append(f"Archivo ejecutado: {ruta_tm}\n")
        resultado_sim = simulador.ejecutar(
            input_callback=solicitar_entrada_tm,
            output_callback=mostrar_linea_ejecucion
        )

        if resultado_sim["exito"]:
            self.statusBar().showMessage(
                f"Ejecución en Tiny Machine finalizada con éxito ({resultado_sim['pasos']} instrucciones ejecutadas).",
                6000
            )
        elif resultado_sim["estado"] == "CANCELADO":
            self.statusBar().showMessage("Ejecución en Tiny Machine cancelada por el usuario.", 5000)
        else:
            self.statusBar().showMessage("Error en tiempo de ejecución en la Tiny Machine.", 5000)


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
            ("file_new.png", "Nuevo Archivo", self.nuevo_archivo),
            ("file_open.png", "Abrir", self.abrir_archivo),
            ("file_save.png", "Guardar", self.guardar_archivo),
            ("file_save_as.png", "Guardar como", self.guardar_como)
        ]

        for icono_nombre, nombre, func in acciones:
            accion = QAction(obtener_icono(icono_nombre), nombre, self)
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
            {"nombre": "Léxico", "icono": "lexico.png"},
            {"nombre": "Sintáctico", "icono": "sintactico.png"},
            {"nombre": "Semántico", "icono": "semantico.png"},
            {"nombre": "Intermedio", "icono": "intermedio.png"},
            {"nombre": "Ejecutar", "icono": "ejecutar.png"}
        ]

        for f in fases:
            icono = obtener_icono(f["icono"])
            accion = QAction(icono, f["nombre"], self)

            if f["nombre"] == "Léxico":
                accion.triggered.connect(self.analisis_lexico)
            elif f["nombre"] == "Sintáctico":
                accion.triggered.connect(lambda _=False: self.analisis_sintactico(cambiar_pestana=True))
            elif f["nombre"] == "Semántico":
                accion.triggered.connect(lambda _=False: self.analisis_semantico(cambiar_pestana=True))
            elif f["nombre"] == "Intermedio":
                accion.triggered.connect(lambda _=False: self.generar_codigo_intermedio(cambiar_pestana=True))
            elif f["nombre"] == "Ejecutar":
                accion.triggered.connect(self.ejecutar_programa)

            objeto.addAction(accion)


if __name__=="__main__":

    app = QApplication(sys.argv)
    w = VentanaPrincipal()
    w.show()
    sys.exit(app.exec())