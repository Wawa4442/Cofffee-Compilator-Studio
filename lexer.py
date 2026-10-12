class Token:
    def __init__(self, tipo, valor, linea, columna):
        self.tipo = tipo
        self.valor = valor
        self.linea = linea
        self.columna = columna

    def __str__(self):
        return f"{self.tipo}('{self.valor}') [{self.linea}:{self.columna}]"


class Lexer:

    def __init__(self, codigo):
        self.codigo = codigo
        self.linea = 1
        self.columna = 1

        # CT-7: Diccionario actualizado con PDF y prueba de la maestra
        self.reservadas = {
            "if", "then", "else", "end", "do", "while", "until",
            "switch", "case", "int", "float", "bool", "real",
            "main", "cin", "cout", "true", "false"
        }

    def analizar(self, is_cancelled=None):
        tokens = []
        errores = []

        i = 0

        while i < len(self.codigo):
            # Verificación de cancelación para el hilo del editor
            if is_cancelled and is_cancelled():
                return [], []

            c = self.codigo[i]

            # ESPACIOS Y SALTOS DE LÍNEA
            if c.isspace():
                if c == "\n":
                    self.linea += 1
                    self.columna = 1
                else:
                    self.columna += 1
                i += 1
                continue

            # STRINGS
            if c == '"':
                inicio = i
                col = self.columna
                i += 1
                self.columna += 1

                while i < len(self.codigo) and self.codigo[i] != '"':
                    if self.codigo[i] == "\n":
                        errores.append(("string sin cerrar", self.linea, col))
                        break
                    i += 1
                    self.columna += 1

                i += 1
                self.columna += 1

                tokens.append(Token("STRING", self.codigo[inicio:i], self.linea, col))
                continue

            # COMENTARIOS
            if i+1 < len(self.codigo):
                if self.codigo[i:i+2] == "//":
                    col = self.columna
                    inicio = i
                    while i < len(self.codigo) and self.codigo[i] != "\n":
                        i += 1
                        self.columna += 1
                    tokens.append(Token("COMENTARIO", self.codigo[inicio:i], self.linea, col))
                    continue

                if self.codigo[i:i+2] == "/*":
                    col = self.columna
                    inicio = i
                    i += 2
                    self.columna += 2

                    cerrado = False

                    while i+1 < len(self.codigo):
                        if self.codigo[i:i+2] == "*/":
                            cerrado = True
                            i += 2
                            self.columna += 2
                            break
                        if self.codigo[i] == "\n":
                            self.linea += 1
                            self.columna = 1
                        else:
                            self.columna += 1
                        i += 1

                    if not cerrado:
                        errores.append(("comentario sin cerrar", self.linea, col))

                    tokens.append(Token("COMENTARIO", self.codigo[inicio:i], self.linea, col))
                    continue

            # IDENTIFICADORES Y PALABRAS RESERVADAS
            if c.isalpha() or c == '_':
                inicio = i
                col = self.columna

                while i < len(self.codigo) and (self.codigo[i].isalnum() or self.codigo[i] == '_'):
                    i += 1
                    self.columna += 1

                palabra = self.codigo[inicio:i]

                if palabra in ["true", "false"]:
                    tokens.append(Token("BOOL", palabra, self.linea, col))
                elif palabra in self.reservadas:
                    tokens.append(Token("RESERVADA", palabra, self.linea, col))
                else:
                    tokens.append(Token("ID", palabra, self.linea, col))

                continue

            # NÚMEROS
            if c.isdigit():
                inicio = i
                col = self.columna
                puntos = 0

                while i < len(self.codigo) and (self.codigo[i].isdigit() or self.codigo[i] == "."):
                    if self.codigo[i] == ".":
                        puntos += 1
                        if puntos > 1:
                            break
                    i += 1
                    self.columna += 1

                num = self.codigo[inicio:i]
                if num.endswith("."):
                    errores.append((num, self.linea, col))
                else:
                    tokens.append(Token("NUM", num, self.linea, col))

                continue

            # DOBLES Y SIMBOLOS
            # Se agrega ^ y % exigidos en la gramática
            if c in "+-*/%=<>(){};,!&|^":
                j = i + 1

                # Verificamos operadores dobles estrictamente juntos (ej. ==, <=, <<)
                if j < len(self.codigo):
                    doble = c + self.codigo[j]
                    if doble in ["++", "--", "==", "!=", "<=", ">=", "&&", "||", "<<", ">>"]:
                        tokens.append(Token("OP", doble, self.linea, self.columna))
                        i += 2
                        self.columna += 2
                        continue

                # Si no es un operador doble, se toma como símbolo simple
                tokens.append(Token("SIMBOLO", c, self.linea, self.columna))
                i += 1
                self.columna += 1
                continue

            # ERROR LÉXICO (caracteres no reconocidos, ej: @)
            errores.append((c, self.linea, self.columna))
            i += 1
            self.columna += 1

        return tokens, errores