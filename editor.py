# -*- coding: utf-8 -*-

from PySide6.QtWidgets import QPlainTextEdit, QWidget, QTextEdit
from PySide6.QtCore import Qt, QRect, QSize
from PySide6.QtGui import QColor, QPainter, QFont, QTextFormat


# =========================
# AREA NUMEROS
# =========================

class LineNumberArea(QWidget):

    def __init__(self, editor):
        super().__init__(editor)
        self.codeEditor = editor


    def sizeHint(self):
        return QSize(
            self.codeEditor.lineNumberAreaWidth(),
            0
        )


    def paintEvent(self, event):
        self.codeEditor.lineNumberAreaPaintEvent(event)



# =========================
# EDITOR CODIGO
# =========================

class EditorCodigo(QPlainTextEdit):

    def __init__(self):
        super().__init__()

        # Fuente monoespaciada
        fuente = QFont("Consolas")
        fuente.setPointSize(11)
        self.setFont(fuente)


        # SIN ajuste de línea
        self.setLineWrapMode(QPlainTextEdit.NoWrap)


        # =========================
        # COLORES TEMA OSCURO
        # =========================

        self.setStyleSheet("""

            QPlainTextEdit {

                background-color: #1e1e1e;
                color: #ffffff;
                selection-background-color: #264f78;
                selection-color: white;

            }

        """)


        # Area números línea
        self.lineNumberArea = LineNumberArea(self)


        self.blockCountChanged.connect(
            self.updateLineNumberAreaWidth
        )

        self.updateRequest.connect(
            self.updateLineNumberArea
        )

        self.cursorPositionChanged.connect(
            self.highlightCurrentLine
        )


        self.updateLineNumberAreaWidth(0)

        self.highlightCurrentLine()



# =========================
# ANCHO NUMEROS
# =========================

    def lineNumberAreaWidth(self):

        digits = 1

        max_value = max(
            1,
            self.blockCount()
        )

        while max_value >= 10:
            max_value //= 10
            digits += 1

        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits

        return space



# =========================
# MARGEN
# =========================

    def updateLineNumberAreaWidth(self, _):

        self.setViewportMargins(
            self.lineNumberAreaWidth(),
            0,
            0,
            0
        )



# =========================
# ACTUALIZAR NUMEROS
# =========================

    def updateLineNumberArea(self, rect, dy):

        if dy:
            self.lineNumberArea.scroll(0, dy)

        else:
            self.lineNumberArea.update(
                0,
                rect.y(),
                self.lineNumberArea.width(),
                rect.height()
            )

        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)



# =========================
# RESIZE
# =========================

    def resizeEvent(self, event):

        super().resizeEvent(event)

        cr = self.contentsRect()

        self.lineNumberArea.setGeometry(

            QRect(
                cr.left(),
                cr.top(),
                self.lineNumberAreaWidth(),
                cr.height()
            )

        )



# =========================
# PINTAR NUMEROS
# =========================

    def lineNumberAreaPaintEvent(self, event):

        painter = QPainter(self.lineNumberArea)

        # Fondo oscuro números
        painter.fillRect(
            event.rect(),
            QColor("#252526")
        )


        block = self.firstVisibleBlock()

        blockNumber = block.blockNumber()

        top = round(
            self.blockBoundingGeometry(block)
            .translated(self.contentOffset())
            .top()
        )


        bottom = top + round(
            self.blockBoundingRect(block)
            .height()
        )


        while block.isValid() and top <= event.rect().bottom():

            if block.isVisible() and bottom >= event.rect().top():

                number = str(blockNumber + 1)

                # Color números línea claro
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

            bottom = top + round(
                self.blockBoundingRect(block).height()
            )

            blockNumber += 1



# =========================
# LINEA ACTUAL
# =========================

    def highlightCurrentLine(self):

        extraSelections = []

        if not self.isReadOnly():

            selection = QTextEdit.ExtraSelection()

            # Azul oscuro visible en fondo negro
            color = QColor("#2a2d2e")

            selection.format.setBackground(color)

            selection.format.setProperty(
                QTextFormat.FullWidthSelection,
                True
            )

            selection.cursor = self.textCursor()

            selection.cursor.clearSelection()

            extraSelections.append(selection)


        self.setExtraSelections(extraSelections)
