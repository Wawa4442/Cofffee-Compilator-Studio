class NodoAST:
    """Clase base para representar los nodos del Árbol Sintáctico Abstracto."""
    def __init__(self, nombre):
        self.nombre = nombre
        self.hijos = []

    def agregar_hijo(self, hijo):
        if hijo:
            self.hijos.append(hijo)


class Parser:
    """Analizador Sintáctico Descendente Recursivo."""
    def __init__(self, tokens):
        # Filtramos los comentarios porque no aportan a la sintaxis
        self.tokens = [t for t in tokens if t.tipo != "COMENTARIO"]
        self.pos = 0
        self.errores = []
        self.token_actual = self.tokens[self.pos] if self.tokens else None

    def avanzar(self):
        """Avanza al siguiente token en la lista."""
        self.pos += 1
        if self.pos < len(self.tokens):
            self.token_actual = self.tokens[self.pos]
        else:
            self.token_actual = None

    def coincidir(self, tipo_esperado, valor_esperado=None):
        """
        Verifica si el token actual coincide con lo esperado.
        Si coincide, avanza. Si no, entra en Modo Pánico.
        """
        if self.token_actual and self.token_actual.tipo == tipo_esperado:
            if valor_esperado is None or self.token_actual.valor == valor_esperado:
                token = self.token_actual
                self.avanzar()
                return token

        # Modo Pánico - Captura de Error Sintáctico
        valor_actual = self.token_actual.valor if self.token_actual else "EOF"
        linea = self.token_actual.linea if self.token_actual else "N/A"
        col = self.token_actual.columna if self.token_actual else "N/A"

        esperado = valor_esperado if valor_esperado else tipo_esperado
        msg_error = f"Error Sintáctico: Se esperaba '{esperado}', pero se encontró '{valor_actual}'"
        self.errores.append((msg_error, linea, col))

        # Intento de recuperación saltando tokens hasta un punto seguro
        self.sincronizar()
        return None

    def sincronizar(self):
        """
        Recuperación de errores: salta tokens hasta encontrar
        un final de sentencia (;) o cierre de bloque (}).
        """
        while self.token_actual and self.token_actual.valor not in [";", "}"]:
            self.avanzar()

        if self.token_actual and self.token_actual.valor in [";", "}"]:
            self.avanzar()

    # ==========================================
    # REGLAS DE LA GRAMÁTICA
    # ==========================================

    def analizar(self):
        """Punto de entrada del analizador."""
        arbol = self.parse_programa()
        return arbol, self.errores

    def parse_programa(self):
        nodo_programa = NodoAST("Programa")

        if self.token_actual and self.token_actual.valor == "main":
            self.coincidir("RESERVADA", "main")
            self.coincidir("SIMBOLO", "{")

            # Ahora el main indica estrictamente que su bloque termina con "}"
            nodo_programa.agregar_hijo(self.parse_lista_declaracion(["}"]))

            self.coincidir("SIMBOLO", "}")
        else:
            self.errores.append(("Error Sintáctico: Todo programa debe iniciar con 'main {'", 1, 1))
            self.sincronizar()

        return nodo_programa

    def parse_lista_declaracion(self, terminadores_esperados):
        nodo = NodoAST("Bloque_Sentencias")
        # El bloque lee sentencias MIENTRAS el token no sea uno de los terminadores indicados
        while self.token_actual and self.token_actual.valor not in terminadores_esperados:
            nodo_decl = self.parse_declaracion()
            if nodo_decl:
                nodo.agregar_hijo(nodo_decl)
            else:
                self.avanzar()
        return nodo

    def parse_declaracion(self):
        nodo = NodoAST("Declaracion")
        if self.token_actual and self.token_actual.valor in ["int", "float", "bool", "real"]:
            nodo.agregar_hijo(self.parse_declaracion_variable())
        else:
            nodo.agregar_hijo(self.parse_sentencia())
        return nodo

    def parse_declaracion_variable(self):
        nodo = NodoAST("Declaracion_Variable")
        tipo_token = self.token_actual
        self.avanzar()
        nodo.agregar_hijo(NodoAST(f"Tipo: {tipo_token.valor}"))

        while self.token_actual and self.token_actual.tipo == "ID":
            nodo.agregar_hijo(NodoAST(f"ID: {self.token_actual.valor}"))
            self.avanzar()

            if self.token_actual and self.token_actual.valor == ",":
                self.avanzar()
            else:
                break

        self.coincidir("SIMBOLO", ";")
        return nodo

    def parse_sentencia(self):
        if not self.token_actual:
            return None

        val = self.token_actual.valor
        if val == "if":
            return self.parse_seleccion()
        elif val == "while":
            return self.parse_iteracion()
        elif val == "do":
            return self.parse_repeticion()
        elif val == "cin":
            return self.parse_sent_in()
        elif val == "cout":
            return self.parse_sent_out()
        elif self.token_actual.tipo == "ID":
            return self.parse_asignacion()
        else:
            self.errores.append((f"Error Sintáctico: Inicio de sentencia no válido '{val}'", self.token_actual.linea, self.token_actual.columna))
            self.sincronizar()
            return None

    # ==========================================
    # ESTRUCTURAS DE CONTROL
    # ==========================================

    def parse_seleccion(self):
        nodo = NodoAST("Sentencia_If")
        self.coincidir("RESERVADA", "if")
        self.coincidir("SIMBOLO", "(")
        nodo.agregar_hijo(self.parse_expresion())
        self.coincidir("SIMBOLO", ")")
        self.coincidir("RESERVADA", "then")

        # El then termina cuando vemos un else o un end
        nodo.agregar_hijo(self.parse_lista_declaracion(["else", "end"]))

        if self.token_actual and self.token_actual.valor == "else":
            nodo_else = NodoAST("Rama_Else")
            self.avanzar()
            # El else termina cuando vemos un end
            nodo_else.agregar_hijo(self.parse_lista_declaracion(["end"]))
            nodo.agregar_hijo(nodo_else)

        self.coincidir("RESERVADA", "end")
        self.coincidir("SIMBOLO", ";")
        return nodo

    def parse_iteracion(self):
        nodo = NodoAST("Sentencia_While")
        self.coincidir("RESERVADA", "while")
        self.coincidir("SIMBOLO", "(")
        nodo.agregar_hijo(self.parse_expresion())
        self.coincidir("SIMBOLO", ")")

        usa_llaves = False
        if self.token_actual and self.token_actual.valor == "{":
            self.avanzar()
            usa_llaves = True

        if usa_llaves:
            # Si abrio con llave, el bloque termina con }
            nodo.agregar_hijo(self.parse_lista_declaracion(["}"]))
            self.coincidir("SIMBOLO", "}")
        else:
            # Si no, termina con end
            nodo.agregar_hijo(self.parse_lista_declaracion(["end"]))
            self.coincidir("RESERVADA", "end")

        if self.token_actual and self.token_actual.valor == ";":
            self.avanzar()

        return nodo

    def parse_repeticion(self):
        nodo = NodoAST("Sentencia_Do")
        self.coincidir("RESERVADA", "do")

        # El bloque do termina forzosamente al toparse con while o until
        nodo.agregar_hijo(self.parse_lista_declaracion(["while", "until"]))

        if self.token_actual and self.token_actual.valor in ["while", "until"]:
            token_cierre = self.token_actual
            self.avanzar()
            nodo.agregar_hijo(NodoAST(f"Condicion: {token_cierre.valor}"))
        else:
            self.coincidir("RESERVADA", "while")

        self.coincidir("SIMBOLO", "(")
        nodo.agregar_hijo(self.parse_expresion())
        self.coincidir("SIMBOLO", ")")
        self.coincidir("SIMBOLO", ";")
        return nodo

    def parse_sent_in(self):
        nodo = NodoAST("Entrada_Cin")
        self.coincidir("RESERVADA", "cin")
        self.coincidir("OP", ">>")
        id_token = self.coincidir("ID")
        if id_token:
            nodo.agregar_hijo(NodoAST(f"ID: {id_token.valor}"))
        self.coincidir("SIMBOLO", ";")
        return nodo

    def parse_sent_out(self):
        nodo = NodoAST("Salida_Cout")
        self.coincidir("RESERVADA", "cout")
        self.coincidir("OP", "<<")
        nodo.agregar_hijo(self.parse_expresion())
        self.coincidir("SIMBOLO", ";")
        return nodo

    def parse_asignacion(self):
        nodo = NodoAST("Asignacion_u_Operacion")
        id_token = self.coincidir("ID")
        if id_token:
            nodo.agregar_hijo(NodoAST(f"ID Destino: {id_token.valor}"))

        if self.token_actual and self.token_actual.valor in ["++", "--"]:
            op_token = self.token_actual
            self.avanzar()
            nodo.agregar_hijo(NodoAST(f"Operador Unario: {op_token.valor}"))
            self.coincidir("SIMBOLO", ";")
            return nodo

        self.coincidir("SIMBOLO", "=")
        nodo.agregar_hijo(self.parse_expresion())
        self.coincidir("SIMBOLO", ";")
        return nodo

    # ==========================================
    # EXPRESIONES MATEMATICAS Y LOGICAS
    # ==========================================

    def parse_expresion(self):
            nodo_izq = self.parse_expresion_simple()

            # 🔥 EL CAMBIO ESTÁ AQUÍ: Cambiamos 'if' por 'while' para permitir
            # encadenar múltiples condiciones (ej. a < b && c != 0 || d > 1)
            while self.token_actual and self.token_actual.valor in ["<", "<=", ">", ">=", "==", "!=", "&&", "||"]:
                nodo_op = NodoAST(f"Operador Relacional/Logico: {self.token_actual.valor}")
                self.avanzar()
                nodo_op.agregar_hijo(nodo_izq)
                nodo_op.agregar_hijo(self.parse_expresion_simple())
                nodo_izq = nodo_op

            return nodo_izq

    def parse_expresion_simple(self):
        nodo_izq = self.parse_termino()

        while self.token_actual and self.token_actual.valor in ["+", "-"]:
            nodo_op = NodoAST(f"Operador Suma/Resta: {self.token_actual.valor}")
            self.avanzar()
            nodo_op.agregar_hijo(nodo_izq)
            nodo_op.agregar_hijo(self.parse_termino())
            nodo_izq = nodo_op

        return nodo_izq

    def parse_termino(self):
        nodo_izq = self.parse_factor()

        while self.token_actual and self.token_actual.valor in ["*", "/", "%"]:
            nodo_op = NodoAST(f"Operador Mult/Div: {self.token_actual.valor}")
            self.avanzar()
            nodo_op.agregar_hijo(nodo_izq)
            nodo_op.agregar_hijo(self.parse_factor())
            nodo_izq = nodo_op

        return nodo_izq

    def parse_factor(self):
        nodo_izq = self.parse_componente()

        while self.token_actual and self.token_actual.valor == "^":
            nodo_op = NodoAST(f"Operador Potencia: {self.token_actual.valor}")
            self.avanzar()
            nodo_op.agregar_hijo(nodo_izq)
            nodo_op.agregar_hijo(self.parse_componente())
            nodo_izq = nodo_op

        return nodo_izq

    def parse_componente(self):
        if not self.token_actual:
            return NodoAST("Error_Componente_Vacio")

        token = self.token_actual

        if token.tipo == "SIMBOLO" and token.valor == "(":
            self.avanzar()
            nodo = self.parse_expresion()
            self.coincidir("SIMBOLO", ")")
            return nodo
        elif token.tipo in ["ID", "NUM", "STRING"]:
            nodo = NodoAST(f"Valor ({token.tipo}): {token.valor}")
            self.avanzar()
            return nodo
        else:
            self.errores.append((f"Error Sintáctico: Se esperaba ID, NUM o '(', pero se encontró '{token.valor}'", token.linea, token.columna))
            self.sincronizar()
            return NodoAST(f"Error_{token.valor}")