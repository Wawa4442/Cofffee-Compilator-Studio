# -*- coding: utf-8 -*-

from PySide6.QtWidgets import QPlainTextEdit, QWidget, QTextEdit, QCompleter
from PySide6.QtCore import Qt, QRect, QSize, QThread, Signal, QTimer
from PySide6.QtGui import QColor, QPainter, QFont, QTextFormat, QTextCharFormat, QSyntaxHighlighter

from lexer import Lexer


# =========================
# HILO LEXER
# =========================

class LexerWorker(QThread):
    resultado = Signal(list, list)

    def __init__(self, texto):
        super().__init__()
        self.texto = texto
        self.is_cancelled = False

    def run(self):
        lexer = Lexer(self.texto)
        tokens, errores = lexer.analizar(lambda: self.is_cancelled)
        if not self.is_cancelled:
            self.resultado.emit(tokens, errores)


# =========================
# HIGHLIGHTER
# =========================

class Highlighter(QSyntaxHighlighter):

    def __init__(self, document):
        super().__init__(document)
        self.tokens = []
        self.errores = []

        def fmt(color, underline=False):
            f = QTextCharFormat()
            f.setForeground(QColor(color))
            if underline:
                f.setUnderlineColor(QColor("red"))
                f.setUnderlineStyle(QTextCharFormat.SpellCheckUnderline)
            return f

        self.formats = {
            "RESERVADA": fmt("#569CD6"),
            "ID": fmt("#9CDCFE"),
            "NUM": fmt("#B5CEA8"),
            "SIMBOLO": fmt("#D4D4D4"),
            "OP": fmt("#D4D4D4"),
            "COMENTARIO": fmt("#6A9955"),
            "ERROR": fmt("#FF0000", True),
            "COMENTARIO_ERROR": fmt("#FF0000", True)
        }

    def setData(self, tokens, errores):
        self.tokens = tokens
        self.errores = errores
        self.rehighlight()

    def highlightBlock(self, text):

        block = self.currentBlock()
        block_pos = block.position()
        block_end = block_pos + len(text)

        prev_state = self.previousBlockState()

        if prev_state == 1:
            start_index = 0
        else:
            start_index = text.find("/*")

        while start_index >= 0:

            end_index = text.find("*/", start_index)

            if end_index == -1:
                self.setCurrentBlockState(1)

                length = len(text) - start_index

                self.setFormat(start_index, length, self.formats["COMENTARIO"])

                if not self._comentario_cerrado_global():
                    self.setFormat(start_index, length, self.formats["COMENTARIO_ERROR"])

                return

            else:
                length = end_index - start_index + 2
                self.setFormat(start_index, length, self.formats["COMENTARIO"])
                start_index = text.find("/*", start_index + length)

        self.setCurrentBlockState(0)

        for t in self.tokens:

            inicio = self._pos(t.linea, t.columna)
            fin = inicio + len(t.valor)

            if fin < block_pos or inicio > block_end:
                continue

            start = max(inicio, block_pos)
            end = min(fin, block_end)

            self.setFormat(start - block_pos, end - start,
                           self.formats.get(t.tipo, QTextCharFormat()))

        for val, linea, col in self.errores:

            inicio = self._pos(linea, col)
            fin = inicio + len(val)

            if fin < block_pos or inicio > block_end:
                continue

            start = max(inicio, block_pos)
            end = min(fin, block_end)

            self.setFormat(start - block_pos, end - start,
                           self.formats["ERROR"])

    def _pos(self, linea, col):
        doc = self.document()
        pos = 0
        for i in range(linea - 1):
            block = doc.findBlockByNumber(i)
            pos += len(block.text()) + 1
        return pos + col - 1

    def _comentario_cerrado_global(self):
        texto = self.document().toPlainText()
        return texto.count("/*") <= texto.count("*/")


# =========================
# AUTOCOMPLETADO
# =========================

class AutoCompleter(QCompleter):
    def __init__(self):
        palabras = [
            "if","else","end","do","while",
            "switch","case","int","float",
            "main","cin","cout"
        ]
        super().__init__(palabras)
        self.setCaseSensitivity(Qt.CaseInsensitive)


# =========================
# AREA NUMEROS
# =========================

class LineNumberArea(QWidget):

    def __init__(self, editor):
        super().__init__(editor)
        self.codeEditor = editor

    def sizeHint(self):
        return QSize(self.codeEditor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.codeEditor.lineNumberAreaPaintEvent(event)


# =========================
# EDITOR
# =========================

class EditorCodigo(QPlainTextEdit):

    def __init__(self):
        super().__init__()

        fuente = QFont("Consolas")
        fuente.setPointSize(11)
        self.setFont(fuente)

        self.setLineWrapMode(QPlainTextEdit.NoWrap)

        self.setStyleSheet("""
            QPlainTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
            }
        """)

        self.lineNumberArea = LineNumberArea(self)

        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)

        self.updateLineNumberAreaWidth(0)
        self.highlightCurrentLine()

        self.highlighter = Highlighter(self.document())

        self.timer = QTimer()
        self.timer.setInterval(300)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.ejecutar_lexer)

        self.textChanged.connect(self.timer.start)

        self.worker = None

        self.completer = AutoCompleter()
        self.completer.setWidget(self)
        self.completer.activated.connect(self.insert_completion)

    def insert_completion(self, completion):
        tc = self.textCursor()
        tc.select(tc.WordUnderCursor)
        tc.removeSelectedText()
        tc.insertText(completion)
        self.setTextCursor(tc)

    def keyPressEvent(self, event):
        super().keyPressEvent(event)

        cursor = self.textCursor()
        cursor.select(cursor.WordUnderCursor)
        palabra = cursor.selectedText()

        if len(palabra) >= 1:
            self.completer.setCompletionPrefix(palabra)
            self.completer.complete()

    def ejecutar_lexer(self):
        texto = self.toPlainText()

        if self.worker and self.worker.isRunning():
            self.worker.is_cancelled = True
            self.worker.resultado.disconnect()

        self.worker = LexerWorker(texto)
        self.worker.resultado.connect(self.actualizar)
        self.worker.start()

    def actualizar(self, tokens, errores):
        self.highlighter.setData(tokens, errores)

# =========================
# RESTO (SIN CAMBIOS)
# =========================

    def lineNumberAreaWidth(self):
        digits = 1
        max_value = max(1, self.blockCount())
        while max_value >= 10:
            max_value //= 10
            digits += 1
        return 3 + self.fontMetrics().horizontalAdvance('9') * digits

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(),
                                              self.lineNumberAreaWidth(), cr.height()))

    # 🔥 AQUÍ ESTÁ LA CORRECCIÓN
    def lineNumberAreaPaintEvent(self, event):

        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), QColor("#252526"))

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()

        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())

        while block.isValid() and top <= event.rect().bottom():

            if block.isVisible() and bottom >= event.rect().top():

                number = str(blockNumber + 1)
                painter.setPen(QColor("#aaaaaa"))

                painter.drawText(
                    0,
                    top,
                    self.lineNumberArea.width() - 5,
                    self.fontMetrics().height(),
                    Qt.AlignRight,
                    number
                )

            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            blockNumber += 1

    def highlightCurrentLine(self):
        extraSelections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            selection.format.setBackground(QColor("#2a2d2e"))
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        self.setExtraSelections(extraSelections)
