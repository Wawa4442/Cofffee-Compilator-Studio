# -*- coding: utf-8 -*-

class NodoAST:
    """Clase base para representar los nodos del Árbol Sintáctico Abstracto."""
    def __init__(self, nombre, linea=None, columna=None, token=None, tipo_dato=None, valor_constante=None):
        self.nombre = nombre
        self.hijos = []
        self.linea = linea
        self.columna = columna
        self.token = token
        self.tipo_dato = tipo_dato          # Atributo sintetizado o de expresión ("int", "float", "bool", etc.)
        self.valor_constante = valor_constante  # Atributo sintetizado: valor evaluado en tiempo de compilación
        self.dtype = None                   # Atributo heredado (para declaraciones de variables)
        self.operador = None                # Operador ('+', '-', '>', '==', etc.)

    def agregar_hijo(self, hijo):
        if hijo:
            self.hijos.append(hijo)

    def clonar(self):
        """Crea una copia profunda del árbol para generar el AST Anotado."""
        nuevo = NodoAST(
            self.nombre,
            linea=self.linea,
            columna=self.columna,
            token=self.token,
            tipo_dato=self.tipo_dato,
            valor_constante=self.valor_constante
        )
        nuevo.dtype = self.dtype
        nuevo.operador = self.operador
        for h in self.hijos:
            nuevo.agregar_hijo(h.clonar())
        return nuevo


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
        while self.token_actual:
            # Si encontramos un terminador, avanzamos uno y paramos (listos para la sig. sentencia)
            if self.token_actual.valor in [";", "}"]:
                self.avanzar()
                return

            # Si el token actual es el INICIO de una nueva sentencia, paramos SIN consumirlo
            inicios_seguros = ["int", "float", "bool", "real", "if", "while", "do", "cin", "cout"]
            if self.token_actual.valor in inicios_seguros:
                return

            self.avanzar()

    # ==========================================
    # REGLAS DE LA GRAMÁTICA
    # ==========================================

    def analizar(self):
        """Punto de entrada del analizador."""
        arbol = self.parse_programa()
        return arbol, self.errores

    def parse_programa(self):
        nodo_programa = NodoAST("Programa", 1, 1)

        if self.token_actual and self.token_actual.valor == "main":
            tok_main = self.coincidir("RESERVADA", "main")
            if tok_main:
                nodo_programa.linea = tok_main.linea
                nodo_programa.columna = tok_main.columna
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
        """
        Parsea un elemento dentro del bloque: ya sea una declaración de variables
        o una sentencia ejecutable (asignación, control de flujo, etc.).
        Retorna el nodo correspondiente directamente sin nodos envoltorios innecesarios.
        """
        if self.token_actual and self.token_actual.valor in ["int", "float", "bool", "real"]:
            return self.parse_declaracion_variable()
        else:
            return self.parse_sentencia()

    def parse_declaracion_variable(self):
        tipo_token = self.token_actual
        linea = tipo_token.linea if tipo_token else None
        col = tipo_token.columna if tipo_token else None
        nodo = NodoAST("Declaracion_Variable", linea=linea, columna=col, token=tipo_token)
        self.avanzar()
        nodo_tipo = NodoAST(f"Tipo: {tipo_token.valor}", linea=linea, columna=col, token=tipo_token, tipo_dato=tipo_token.valor)
        nodo.agregar_hijo(nodo_tipo)

        while self.token_actual and self.token_actual.tipo == "ID":
            tok_id = self.token_actual
            nodo_id = NodoAST(f"ID: {tok_id.valor}", linea=tok_id.linea, columna=tok_id.columna, token=tok_id)
            nodo.agregar_hijo(nodo_id)
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

    def parse_condicion(self):
        """
        Parsea una condición lógica o relacional.
        Soporta condiciones con o sin paréntesis (ej. '2>3' o '(2>3)').
        """
        tiene_parentesis = False
        if self.token_actual and self.token_actual.tipo == "SIMBOLO" and self.token_actual.valor == "(":
            self.avanzar()
            tiene_parentesis = True

        nodo_exp = self.parse_expresion()

        if tiene_parentesis:
            if self.token_actual and self.token_actual.valor == ")":
                self.avanzar()
            else:
                linea = self.token_actual.linea if self.token_actual else "N/A"
                col = self.token_actual.columna if self.token_actual else "N/A"
                self.errores.append(("Error Sintáctico: Se esperaba ')' después de la condición", linea, col))

        return nodo_exp

    def parse_seleccion(self):
        tok_if = self.coincidir("RESERVADA", "if")
        if not tok_if:
            return None
        nodo = NodoAST("Sentencia_If", linea=tok_if.linea, columna=tok_if.columna, token=tok_if)

        # Condición con o sin paréntesis
        nodo.agregar_hijo(self.parse_condicion())

        # Palabra reservada 'then'
        self.coincidir("RESERVADA", "then")

        # Bloque 'then' termina cuando vemos un 'else' o un 'end'
        nodo.agregar_hijo(self.parse_lista_declaracion(["else", "end"]))

        if self.token_actual and self.token_actual.valor == "else":
            tok_else = self.token_actual
            nodo_else = NodoAST("Rama_Else", linea=tok_else.linea, columna=tok_else.columna, token=tok_else)
            self.avanzar()
            nodo_else.agregar_hijo(self.parse_lista_declaracion(["end"]))
            nodo.agregar_hijo(nodo_else)

        self.coincidir("RESERVADA", "end")

        # Consumimos el ';' opcional al final del end si existe
        if self.token_actual and self.token_actual.valor == ";":
            self.avanzar()

        return nodo

    def parse_iteracion(self):
        tok_while = self.coincidir("RESERVADA", "while")
        if not tok_while:
            return None
        nodo = NodoAST("Sentencia_While", linea=tok_while.linea, columna=tok_while.columna, token=tok_while)

        # Condición con o sin paréntesis
        nodo.agregar_hijo(self.parse_condicion())

        usa_llaves = False
        if self.token_actual and self.token_actual.valor == "{":
            self.avanzar()
            usa_llaves = True

        if usa_llaves:
            # Si abrió con llave, el bloque termina con }
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
        tok_do = self.coincidir("RESERVADA", "do")
        if not tok_do:
            return None
        nodo = NodoAST("Sentencia_Do", linea=tok_do.linea, columna=tok_do.columna, token=tok_do)

        usa_llaves = False
        if self.token_actual and self.token_actual.valor == "{":
            self.avanzar()
            usa_llaves = True

        if usa_llaves:
            nodo.agregar_hijo(self.parse_lista_declaracion(["}"]))
            self.coincidir("SIMBOLO", "}")
        else:
            # El bloque do procesa sentencias internas hasta topar con 'until'
            nodo.agregar_hijo(self.parse_lista_declaracion(["until"]))

        # Procesamos la condición de cierre
        if self.token_actual and self.token_actual.valor in ["until", "while"]:
            token_cierre = self.token_actual
            self.avanzar()
            nodo_cierre = NodoAST(f"Condicion: {token_cierre.valor}", linea=token_cierre.linea, columna=token_cierre.columna, token=token_cierre)
            nodo.agregar_hijo(nodo_cierre)
        else:
            self.coincidir("RESERVADA", "until")

        nodo.agregar_hijo(self.parse_condicion())

        if self.token_actual and self.token_actual.valor == ";":
            self.avanzar()

        return nodo

    def parse_sent_in(self):
        tok_cin = self.coincidir("RESERVADA", "cin")
        linea = tok_cin.linea if tok_cin else None
        col = tok_cin.columna if tok_cin else None
        nodo = NodoAST("Entrada_Cin", linea=linea, columna=col, token=tok_cin)

        # 1. Capturamos el token del operador de flujo
        op_token = self.coincidir("OP", ">>")
        if op_token:
            nodo.agregar_hijo(NodoAST(f"Operador: {op_token.valor}", linea=op_token.linea, columna=op_token.columna, token=op_token))

        # 2. Capturamos el ID de destino
        id_token = self.coincidir("ID")
        if id_token:
            nodo.agregar_hijo(NodoAST(f"ID Destino: {id_token.valor}", linea=id_token.linea, columna=id_token.columna, token=id_token))

        self.coincidir("SIMBOLO", ";")
        return nodo

    def parse_sent_out(self):
        tok_cout = self.coincidir("RESERVADA", "cout")
        linea = tok_cout.linea if tok_cout else None
        col = tok_cout.columna if tok_cout else None
        nodo = NodoAST("Salida_Cout", linea=linea, columna=col, token=tok_cout)

        # 1. Capturamos el token del operador de flujo
        op_token = self.coincidir("OP", "<<")
        if op_token:
            nodo.agregar_hijo(NodoAST(f"Operador: {op_token.valor}", linea=op_token.linea, columna=op_token.columna, token=op_token))

        # 2. Evaluamos y agregamos la expresión a imprimir
        nodo.agregar_hijo(self.parse_expresion())

        self.coincidir("SIMBOLO", ";")
        return nodo

    def parse_asignacion(self):
        id_token = self.coincidir("ID")
        linea = id_token.linea if id_token else None
        col = id_token.columna if id_token else None
        nodo = NodoAST("Asignacion_u_Operacion", linea=linea, columna=col, token=id_token)
        if id_token:
            nodo.agregar_hijo(NodoAST(f"ID Destino: {id_token.valor}", linea=linea, columna=col, token=id_token))

        if self.token_actual and self.token_actual.valor in ["++", "--"]:
            op_token = self.token_actual
            self.avanzar()
            nodo_unario = NodoAST(f"Operador Unario: {op_token.valor}", linea=op_token.linea, columna=op_token.columna, token=op_token)
            nodo_unario.operador = op_token.valor
            nodo.agregar_hijo(nodo_unario)
            if self.token_actual and self.token_actual.valor == ";":
                self.avanzar()
            return nodo

        self.coincidir("SIMBOLO", "=")
        nodo.agregar_hijo(self.parse_expresion())
        self.coincidir("SIMBOLO", ";")
        return nodo

    # ==========================================
    # EXPRESIONES MATEMATICAS Y LOGICAS
    # ==========================================

    def parse_expresion(self):
        """ Nivel 1: Precedencia más baja (Operadores Lógicos &&, ||) """
        nodo_izq = self.parse_expresion_relacional()

        while self.token_actual and self.token_actual.valor in ["&&", "||"]:
            op_token = self.token_actual
            self.avanzar()
            nodo_op = NodoAST(f"Operador Logico: {op_token.valor}", linea=op_token.linea, columna=op_token.columna, token=op_token)
            nodo_op.operador = op_token.valor
            nodo_op.agregar_hijo(nodo_izq)
            nodo_op.agregar_hijo(self.parse_expresion_relacional())
            nodo_izq = nodo_op

        return nodo_izq

    def parse_expresion_relacional(self):
        """ Nivel 2: Precedencia media (Operadores Relacionales ==, >, <, etc.) """
        nodo_izq = self.parse_expresion_simple()

        while self.token_actual and self.token_actual.valor in ["<", "<=", ">", ">=", "==", "!="]:
            op_token = self.token_actual
            self.avanzar()
            nodo_op = NodoAST(f"Operador Relacional: {op_token.valor}", linea=op_token.linea, columna=op_token.columna, token=op_token)
            nodo_op.operador = op_token.valor
            nodo_op.agregar_hijo(nodo_izq)
            nodo_op.agregar_hijo(self.parse_expresion_simple())
            nodo_izq = nodo_op

        return nodo_izq

    def parse_expresion_simple(self):
        nodo_izq = self.parse_termino()

        while self.token_actual and self.token_actual.valor in ["+", "-"]:
            op_token = self.token_actual
            self.avanzar()
            nodo_op = NodoAST(f"Operador Suma/Resta: {op_token.valor}", linea=op_token.linea, columna=op_token.columna, token=op_token)
            nodo_op.operador = op_token.valor
            nodo_op.agregar_hijo(nodo_izq)
            nodo_op.agregar_hijo(self.parse_termino())
            nodo_izq = nodo_op

        return nodo_izq

    def parse_termino(self):
        nodo_izq = self.parse_factor()

        while self.token_actual and self.token_actual.valor in ["*", "/", "%"]:
            op_token = self.token_actual
            self.avanzar()
            nodo_op = NodoAST(f"Operador Mult/Div: {op_token.valor}", linea=op_token.linea, columna=op_token.columna, token=op_token)
            nodo_op.operador = op_token.valor
            nodo_op.agregar_hijo(nodo_izq)
            nodo_op.agregar_hijo(self.parse_factor())
            nodo_izq = nodo_op

        return nodo_izq

    def parse_factor(self):
        nodo_izq = self.parse_componente()

        while self.token_actual and self.token_actual.valor == "^":
            op_token = self.token_actual
            self.avanzar()
            nodo_op = NodoAST(f"Operador Potencia: {op_token.valor}", linea=op_token.linea, columna=op_token.columna, token=op_token)
            nodo_op.operador = op_token.valor
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
        elif token.tipo in ["ID", "NUM", "STRING", "BOOL"] or (token.tipo == "RESERVADA" and token.valor in ["true", "false"]):
            nodo = NodoAST(f"Valor ({token.tipo}): {token.valor}", linea=token.linea, columna=token.columna, token=token)
            if token.tipo == "BOOL" or token.valor in ["true", "false"]:
                nodo.tipo_dato = "bool"
                nodo.valor_constante = (token.valor == "true")
            elif token.tipo == "NUM":
                if "." in token.valor:
                    nodo.tipo_dato = "float"
                    try:
                        nodo.valor_constante = float(token.valor)
                    except ValueError:
                        pass
                else:
                    nodo.tipo_dato = "int"
                    try:
                        nodo.valor_constante = int(token.valor)
                    except ValueError:
                        pass
            elif token.tipo == "STRING":
                nodo.tipo_dato = "string"
                nodo.valor_constante = token.valor
            self.avanzar()
            return nodo
        else:
            msg = f"Se esperaba un número o identificador, se encontró '{token.valor}'"
            self.errores.append((msg, token.linea, token.columna))
            self.avanzar()
            return NodoAST("Error: Expresion_Invalida", linea=token.linea, columna=token.columna, token=token)
