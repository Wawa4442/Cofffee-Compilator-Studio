# -*- coding: utf-8 -*-

from symbol_table import SymbolTable


class ErrorSemantico:
    """Encapsula la información de un error semántico detectado."""
    def __init__(self, mensaje, linea, columna):
        self.mensaje = mensaje
        self.linea = linea if linea is not None else "N/A"
        self.columna = columna if columna is not None else "N/A"

    def __str__(self):
        return f"Error Semántico: {self.mensaje} en línea {self.linea}, columna {self.columna}"


class SemanticAnalyzer:
    """
    Analizador Semántico del Compilador.
    Responsabilidades:
      - Construir y consultar la Tabla de Símbolos.
      - Generar el Árbol Sintáctico Anotado con atributos sintetizados y heredados.
      - Plegado de constantes (Constant Folding) para expresiones estáticas.
      - Verificación y promoción de tipos (int, float, bool).
      - Validación de tipos en condiciones de estructuras de control (if, while, until).
      - Detección y reporte detallado de errores semánticos sin abortar el análisis.
    """
    def __init__(self):
        self.tabla = SymbolTable()
        self.errores = []           # Lista de ErrorSemantico
        self.ast_anotado = None

    def analizar(self, ast_original):
        """
        Ejecuta el análisis semántico sobre una copia profunda del AST original.
        Retorna:
          - ast_anotado: Árbol anotado con tipos y valores constantes.
          - tabla: Tabla de símbolos poblada.
          - errores: Lista de tuplas (mensaje, linea, columna).
        """
        self.tabla.limpiar()
        self.errores.clear()
        self.ast_anotado = None

        if not ast_original:
            return None, self.tabla, []

        # Clonamos el AST para preservar el AST sintáctico original intacto
        self.ast_anotado = ast_original.clonar()

        # Recorrido principal
        self.visitar(self.ast_anotado)

        # Retornamos los errores como tuplas compatibles con la consola del IDE
        lista_errores = [(e.mensaje, e.linea, e.columna) for e in self.errores]
        return self.ast_anotado, self.tabla, lista_errores

    def reportar_error(self, mensaje, linea, columna):
        """Registra un error semántico sin detener el flujo de análisis."""
        self.errores.append(ErrorSemantico(mensaje, linea, columna))

    # =========================================================================
    # RECORRIDO DEL AST (VISITOR)
    # =========================================================================

    def visitar(self, nodo):
        """Despachador de nodos del AST."""
        if not nodo:
            return

        nombre = nodo.nombre

        if nombre == "Programa":
            for hijo in nodo.hijos:
                self.visitar(hijo)

        elif nombre == "Bloque_Sentencias":
            for hijo in nodo.hijos:
                self.visitar(hijo)

        elif nombre in ("Declaracion", "Sentencia"):
            for hijo in nodo.hijos:
                self.visitar(hijo)

        elif nombre == "Declaracion_Variable":
            self.visitar_declaracion_variable(nodo)

        elif nombre in ("Asignacion_u_Operacion", "Asignacion", "Incremento_Decremento"):
            self.visitar_asignacion(nodo)

        elif nombre == "Sentencia_If":
            self.visitar_if(nodo)

        elif nombre == "Rama_Else":
            for hijo in nodo.hijos:
                self.visitar(hijo)

        elif nombre == "Sentencia_While":
            self.visitar_while(nodo)

        elif nombre == "Sentencia_Do":
            self.visitar_do(nodo)

        elif nombre == "Entrada_Cin":
            self.visitar_cin(nodo)

        elif nombre == "Salida_Cout":
            self.visitar_cout(nodo)

        else:
            # Por defecto, visitar los hijos si no es un nodo especial
            for hijo in nodo.hijos:
                self.visitar(hijo)

    # =========================================================================
    # DECLARACIONES Y TABLA DE SÍMBOLOS
    # =========================================================================

    def visitar_declaracion_variable(self, nodo):
        """
        Procesa una declaración de variables (ej. 'int x, y, z;').
        Propaga el atributo heredado dtype hacia los identificadores declarados
        e inserta cada uno en la tabla de símbolos.
        """
        if not nodo.hijos:
            return

        # El primer hijo indica el tipo (ej. 'Tipo: int')
        primer_hijo = nodo.hijos[0]
        tipo_declarado = primer_hijo.tipo_dato
        if not tipo_declarado:
            # Extraer de 'Tipo: int'
            if ":" in primer_hijo.nombre:
                tipo_declarado = primer_hijo.nombre.split(":", 1)[1].strip()

        # Normalizamos 'real' a 'float'
        if tipo_declarado == "real":
            tipo_declarado = "float"

        primer_hijo.tipo_dato = tipo_declarado
        nodo.tipo_dato = tipo_declarado
        nodo.dtype = tipo_declarado

        # Los siguientes hijos son los identificadores declarados
        for hijo in nodo.hijos[1:]:
            if "ID:" in hijo.nombre:
                nombre_id = hijo.nombre.split(":", 1)[1].strip()
                hijo.tipo_dato = tipo_declarado
                hijo.dtype = tipo_declarado

                # Intentamos insertar en la tabla de símbolos
                exito, resultado = self.tabla.insertar(
                    nombre=nombre_id,
                    tipo=tipo_declarado,
                    linea=hijo.linea
                )
                if not exito:
                    self.reportar_error(resultado, hijo.linea, hijo.columna)
                    self.tabla.registrar_uso(nombre_id, hijo.linea)
                    hijo.tipo_dato = "ERROR_TYPE"
                    nodo.tipo_dato = "ERROR_TYPE"

    # =========================================================================
    # ASIGNACIONES Y OPERADORES UNARIOS
    # =========================================================================

    def anotar(self, nodo, tipo, valor=None):
        """Un nodo inválido nunca conserva un valor constante ni una conversión."""
        nodo.tipo_dato = tipo
        nodo.valor_constante = valor if tipo != "ERROR_TYPE" else None
        if tipo == "ERROR_TYPE":
            nodo.conversion = None
        return nodo.tipo_dato, nodo.valor_constante

    def visitar_asignacion(self, nodo):
        if not nodo.hijos:
            return
        hijo_id = nodo.hijos[0]
        nombre_id = hijo_id.nombre.split(":", 1)[1].strip()
        simbolo = self.tabla.buscar(nombre_id)
        tipo_var = simbolo.tipo if simbolo else "ERROR_TYPE"
        if simbolo:
            self.tabla.registrar_uso(nombre_id, hijo_id.linea)
        else:
            self.reportar_error(f"Variable '{nombre_id}' no declarada",
                                hijo_id.linea, hijo_id.columna)
        self.anotar(hijo_id, tipo_var)

        if len(nodo.hijos) < 2:
            self.anotar(nodo, "ERROR_TYPE")
            return
        expresion = nodo.hijos[1]
        if expresion.nombre.startswith("Operador Unario:"):
            if tipo_var != "ERROR_TYPE" and tipo_var not in ("int", "float"):
                self.reportar_error(
                    f"Operador unario '{expresion.operador}' no permitido para variable de tipo '{tipo_var}'",
                    expresion.linea, expresion.columna)
                tipo_var = "ERROR_TYPE"
            self.anotar(expresion, tipo_var)
            self.anotar(nodo, tipo_var)
            return

        # Evaluar siempre el origen, incluso si el destino no existe.
        tipo_exp, valor = self.evaluar_expresion(expresion)
        if "ERROR_TYPE" in (tipo_var, tipo_exp):
            self.anotar(nodo, "ERROR_TYPE")
            return
        if tipo_var == tipo_exp:
            self.anotar(nodo, tipo_var, valor)
        elif tipo_var == "float" and tipo_exp == "int":
            nodo.conversion = "int -> float (asignación)"
            self.anotar(nodo, "float", float(valor) if valor is not None else None)
        else:
            self.reportar_error(
                f"Incompatibilidad de tipos en asignación: no se puede asignar '{tipo_exp}' a la variable '{nombre_id}' de tipo '{tipo_var}'",
                hijo_id.linea, hijo_id.columna)
            self.anotar(nodo, "ERROR_TYPE")

    # =========================================================================
    # ESTRUCTURAS DE CONTROL (IF, WHILE, DO-UNTIL)
    # =========================================================================

    def visitar_if(self, nodo):
        """Verifica que la condición del 'if' sea estrictamente de tipo 'bool'."""
        if not nodo.hijos:
            return

        # Primer hijo: Condición
        nodo_cond = nodo.hijos[0]
        tipo_cond, val_cond = self.evaluar_expresion(nodo_cond)
        if tipo_cond != "bool":
            self.anotar(nodo, "ERROR_TYPE")

        if tipo_cond != "ERROR_TYPE" and tipo_cond != "bool":
            self.reportar_error(
                f"Tipo incorrecto en la condición de 'if': se requiere expresión booleana, se obtuvo '{tipo_cond}'",
                nodo_cond.linea or nodo.linea,
                nodo_cond.columna or nodo.columna
            )

        # Visitar rama Then y Else
        for hijo in nodo.hijos[1:]:
            self.visitar(hijo)

    def visitar_while(self, nodo):
        """Verifica que la condición del 'while' sea estrictamente booleana."""
        if not nodo.hijos:
            return

        nodo_cond = nodo.hijos[0]
        tipo_cond, val_cond = self.evaluar_expresion(nodo_cond)
        if tipo_cond != "bool":
            self.anotar(nodo, "ERROR_TYPE")

        if tipo_cond != "ERROR_TYPE" and tipo_cond != "bool":
            self.reportar_error(
                f"Tipo incorrecto en la condición de 'while': se requiere expresión booleana, se obtuvo '{tipo_cond}'",
                nodo_cond.linea or nodo.linea,
                nodo_cond.columna or nodo.columna
            )

        for hijo in nodo.hijos[1:]:
            self.visitar(hijo)

    def visitar_do(self, nodo):
        """Verifica el cuerpo y la condición de cierre del bucle 'do ... until'."""
        if not nodo.hijos:
            return

        # Los hijos contienen: Bloque_Sentencias, Condicion: until/while, y la Expresión de condición
        for hijo in nodo.hijos:
            if hijo.nombre == "Bloque_Sentencias":
                self.visitar(hijo)
            elif "Condicion:" in hijo.nombre:
                pass
            else:
                # Es el nodo de la condición
                tipo_cond, val_cond = self.evaluar_expresion(hijo)
                if tipo_cond != "bool":
                    self.anotar(nodo, "ERROR_TYPE")
                if tipo_cond != "ERROR_TYPE" and tipo_cond != "bool":
                    self.reportar_error(
                        f"Tipo incorrecto en la condición de cierre de ciclo: se requiere expresión booleana, se obtuvo '{tipo_cond}'",
                        hijo.linea or nodo.linea,
                        hijo.columna or nodo.columna
                    )

    # =========================================================================
    # ENTRADA Y SALIDA (CIN, COUT)
    # =========================================================================

    def visitar_cin(self, nodo):
        """Verifica que el identificador leído en 'cin >> id;' esté declarado."""
        for hijo in nodo.hijos:
            if "ID Destino:" in hijo.nombre:
                nombre_id = hijo.nombre.split(":", 1)[1].strip()
                simbolo = self.tabla.buscar(nombre_id)
                if not simbolo:
                    self.reportar_error(
                        f"Variable '{nombre_id}' no declarada en sentencia 'cin'",
                        hijo.linea or nodo.linea,
                        hijo.columna or nodo.columna
                    )
                    hijo.tipo_dato = "ERROR_TYPE"
                else:
                    self.tabla.registrar_uso(nombre_id, hijo.linea or nodo.linea)
                    hijo.tipo_dato = simbolo.tipo
                nodo.tipo_dato = hijo.tipo_dato

    def visitar_cout(self, nodo):
        """Evalúa la expresión a imprimir en 'cout << exp;'."""
        for hijo in nodo.hijos:
            if not hijo.nombre.startswith("Operador:"):
                tipo_exp, val_exp = self.evaluar_expresion(hijo)
                nodo.tipo_dato = tipo_exp
                nodo.valor_constante = val_exp

    # =========================================================================
    # EVALUACIÓN DE EXPRESIONES, TIPOS Y CONSTANT FOLDING
    # =========================================================================

    def evaluar_expresion(self, nodo):
        """Sintetiza tipo y valor, y propaga ERROR_TYPE sin errores en cascada."""
        if nodo is None:
            return "ERROR_TYPE", None
        nombre = nodo.nombre
        if nombre.startswith("Valor ("):
            lexema = nombre.split(":", 1)[1].strip()
            if nombre.startswith("Valor (NUM):"):
                tipo = "float" if "." in lexema else "int"
                valor = float(lexema) if tipo == "float" else int(lexema)
                return self.anotar(nodo, tipo, valor)
            if nombre.startswith("Valor (BOOL):") or lexema in ("true", "false"):
                return self.anotar(nodo, "bool", lexema == "true")
            if nombre.startswith("Valor (STRING):"):
                return self.anotar(nodo, "string", lexema)
            if nombre.startswith("Valor (ID):"):
                simbolo = self.tabla.buscar(lexema)
                if simbolo is None:
                    self.reportar_error(f"Variable '{lexema}' no declarada", nodo.linea, nodo.columna)
                    return self.anotar(nodo, "ERROR_TYPE")
                self.tabla.registrar_uso(lexema, nodo.linea)
                return self.anotar(nodo, simbolo.tipo)

        logico = nombre.startswith("Operador Logico:")
        relacional = nombre.startswith("Operador Relacional:")
        aritmetico = nombre.startswith(("Operador Suma/Resta:", "Operador Mult/Div:", "Operador Potencia:"))
        if logico or relacional or aritmetico:
            if len(nodo.hijos) != 2:
                return self.anotar(nodo, "ERROR_TYPE")
            op = nombre.split(":", 1)[1].strip()
            t1, v1 = self.evaluar_expresion(nodo.hijos[0])
            t2, v2 = self.evaluar_expresion(nodo.hijos[1])
            numericos = ("int", "float")

            if logico:
                for hijo, tipo in zip(nodo.hijos, (t1, t2)):
                    if tipo not in ("bool", "ERROR_TYPE"):
                        self.reportar_error(
                            f"El operando de '{op}' debe ser booleano, se obtuvo '{tipo}'",
                            hijo.linea, hijo.columna)
                if t1 != "bool" or t2 != "bool":
                    return self.anotar(nodo, "ERROR_TYPE")
                valor = None
                if v1 is not None and v2 is not None:
                    valor = (v1 and v2) if op == "&&" else (v1 or v2)
                return self.anotar(nodo, "bool", valor)

            if "ERROR_TYPE" in (t1, t2):
                return self.anotar(nodo, "ERROR_TYPE")
            if relacional:
                # Orden: numéricos. Igualdad: numéricos o dos booleanos.
                valido = t1 in numericos and t2 in numericos
                if op in ("==", "!="):
                    valido = valido or t1 == t2 == "bool"
                if not valido:
                    self.reportar_error(
                        f"No se pueden comparar tipos '{t1}' y '{t2}' con el operador '{op}'",
                        nodo.linea, nodo.columna)
                    return self.anotar(nodo, "ERROR_TYPE")
                if t1 != t2:
                    nodo.conversion = "int -> float (comparación)"
                    if v1 is not None: v1 = float(v1)
                    if v2 is not None: v2 = float(v2)
                valor = None
                if v1 is not None and v2 is not None:
                    if op == "<": valor = v1 < v2
                    elif op == "<=": valor = v1 <= v2
                    elif op == ">": valor = v1 > v2
                    elif op == ">=": valor = v1 >= v2
                    elif op == "==": valor = v1 == v2
                    elif op == "!=": valor = v1 != v2
                return self.anotar(nodo, "bool", valor)

            if t1 not in numericos or t2 not in numericos:
                self.reportar_error(
                    f"Uso indebido del operador aritmético '{op}' con operandos de tipo '{t1}' y '{t2}'",
                    nodo.linea, nodo.columna)
                return self.anotar(nodo, "ERROR_TYPE")
            if op == "%" and (t1 != "int" or t2 != "int"):
                self.reportar_error("El operador módulo '%' requiere operandos enteros", nodo.linea, nodo.columna)
                return self.anotar(nodo, "ERROR_TYPE")
            if op in ("/", "%") and v2 == 0:
                self.reportar_error("División o módulo entre cero en tiempo de compilación", nodo.linea, nodo.columna)
                return self.anotar(nodo, "ERROR_TYPE")

            tipo = "float" if "float" in (t1, t2) else "int"
            if t1 != t2:
                nodo.conversion = "int -> float (operando aritmético)"
                if v1 is not None: v1 = float(v1)
                if v2 is not None: v2 = float(v2)
            if op == "^" and tipo == "int" and (v2 is None or v2 < 0):
                tipo = "float"
                nodo.conversion = "int -> float (potencia con exponente negativo o desconocido)"
            valor = None
            if v1 is not None and v2 is not None:
                try:
                    if op == "+": valor = v1 + v2
                    elif op == "-": valor = v1 - v2
                    elif op == "*": valor = v1 * v2
                    elif op == "/": valor = v1 // v2 if tipo == "int" else v1 / v2
                    elif op == "%": valor = v1 % v2
                    elif op == "^": valor = v1 ** v2
                    if isinstance(valor, complex):
                        self.reportar_error("La potencia produce un valor complejo, fuera de int/float", nodo.linea, nodo.columna)
                        return self.anotar(nodo, "ERROR_TYPE")
                    valor = float(valor) if tipo == "float" else int(valor)
                except (ArithmeticError, ValueError) as exc:
                    self.reportar_error(f"No se puede evaluar la expresión constante: {exc}", nodo.linea, nodo.columna)
                    return self.anotar(nodo, "ERROR_TYPE")
            return self.anotar(nodo, tipo, valor)

        if nodo.hijos:
            tipo, valor = self.evaluar_expresion(nodo.hijos[0])
            return self.anotar(nodo, tipo, valor)
        return self.anotar(nodo, "ERROR_TYPE")
