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

        elif nombre == "Declaracion":
            for hijo in nodo.hijos:
                self.visitar(hijo)

        elif nombre == "Declaracion_Variable":
            self.visitar_declaracion_variable(nodo)

        elif nombre == "Asignacion_u_Operacion":
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

        nodo.tipo_dato = tipo_declarado
        nodo.dtype = tipo_declarado

        # Los siguientes hijos son los identificadores declarados
        for hijo in nodo.hijos[1:]:
            if "ID:" in hijo.nombre:
                nombre_id = hijo.nombre.split(":", 1)[1].strip()
                hijo.tipo_dato = tipo_declarado
                hijo.dtype = tipo_declarado

                # Intentamos insertar en la tabla de símbolos
                lin = hijo.linea or nodo.linea
                col = hijo.columna or nodo.columna
                exito, resultado = self.tabla.insertar(
                    nombre=nombre_id,
                    tipo=tipo_declarado,
                    linea=lin,
                    columna=col
                )
                if not exito:
                    hijo.tipo_dato = "ERROR_TYPE"
                    self.reportar_error(resultado, lin, col)

    # =========================================================================
    # ASIGNACIONES Y OPERADORES UNARIOS
    # =========================================================================

    def visitar_asignacion(self, nodo):
        """
        Procesa asignaciones ('x = exp;') y operaciones unarias ('a++;').
        Valida que el identificador esté declarado y comprueba la compatibilidad
        de tipos entre la variable destino y la expresión origen.
        """
        if not nodo.hijos:
            return

        # Primer hijo: 'ID Destino: <nombre>'
        hijo_id = nodo.hijos[0]
        nombre_id = hijo_id.nombre.split(":", 1)[1].strip() if ":" in hijo_id.nombre else hijo_id.nombre

        # Búsqueda en la Tabla de Símbolos
        simbolo = self.tabla.buscar(nombre_id)
        if not simbolo:
            self.reportar_error(
                f"Variable '{nombre_id}' no declarada",
                hijo_id.linea or nodo.linea,
                hijo_id.columna or nodo.columna
            )
            tipo_var = "ERROR_TYPE"
        else:
            tipo_var = simbolo.tipo
            self.tabla.registrar_uso(nombre_id, hijo_id.linea or nodo.linea)

        hijo_id.tipo_dato = tipo_var

        # Caso 1: Operador unario (++ o --)
        if len(nodo.hijos) > 1 and "Operador Unario:" in nodo.hijos[1].nombre:
            nodo_op = nodo.hijos[1]
            op = nodo_op.nombre.split(":", 1)[1].strip()
            nodo_op.tipo_dato = tipo_var
            nodo.tipo_dato = tipo_var

            if tipo_var != "ERROR_TYPE" and tipo_var not in ["int", "float", "real"]:
                self.reportar_error(
                    f"Operador unario '{op}' no permitido para variable de tipo '{tipo_var}'",
                    nodo_op.linea or nodo.linea,
                    nodo_op.columna or nodo.columna
                )
            return

        # Caso 2: Asignación ordinaria ('=')
        if len(nodo.hijos) > 1:
            nodo_exp = nodo.hijos[1]
            tipo_exp, val_exp = self.evaluar_expresion(nodo_exp)

            es_compatible = True

            # Verificación de compatibilidad de tipos
            if tipo_var == "ERROR_TYPE" or tipo_exp == "ERROR_TYPE":
                es_compatible = False
            elif tipo_var == "int" and tipo_exp == "float":
                # Error crítico: asignación de flotante a entero con pérdida de precisión
                self.reportar_error(
                    f"Incompatibilidad de tipos en asignación: no se puede asignar un valor 'float' a la variable entera '{nombre_id}'",
                    hijo_id.linea or nodo.linea,
                    hijo_id.columna or nodo.columna
                )
                es_compatible = False
            elif tipo_var == "bool" and tipo_exp != "bool":
                self.reportar_error(
                    f"Incompatibilidad de tipos en asignación: se esperaba expresión booleana para '{nombre_id}', pero se obtuvo '{tipo_exp}'",
                    hijo_id.linea or nodo.linea,
                    hijo_id.columna or nodo.columna
                )
                es_compatible = False
            elif tipo_var in ["float", "real"] and tipo_exp == "int":
                # Promoción implícita válida: int -> float
                es_compatible = True
            elif tipo_var != tipo_exp:
                self.reportar_error(
                    f"Incompatibilidad de tipos: no se puede asignar '{tipo_exp}' a variable '{nombre_id}' de tipo '{tipo_var}'",
                    hijo_id.linea or nodo.linea,
                    hijo_id.columna or nodo.columna
                )
                es_compatible = False

            if es_compatible:
                nodo.tipo_dato = tipo_var
                nodo.valor_constante = val_exp
            else:
                nodo.tipo_dato = "ERROR_TYPE"
                nodo.valor_constante = None

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
        """
        Evalúa recursivamente un nodo de expresión en el AST.
        Calcula:
          - tipo resultante (sintetizado).
          - valor constante si los operandos son literales (Constant Folding).
        Anota directamente en el nodo: nodo.tipo_dato y nodo.valor_constante.
        Retorna: (tipo, valor_constante)
        """
        if not nodo:
            return "ERROR_TYPE", None

        nombre = nodo.nombre

        # ---------------------------------------------------------------------
        # 1. VALORES HOJA (LITERALES E IDENTIFICADORES)
        # ---------------------------------------------------------------------
        if nombre.startswith("Valor ("):
            if "Valor (NUM):" in nombre:
                val_str = nombre.split(":", 1)[1].strip()
                if "." in val_str:
                    tipo = "float"
                    val = float(val_str)
                else:
                    tipo = "int"
                    val = int(val_str)
                nodo.tipo_dato = tipo
                nodo.valor_constante = val
                return tipo, val

            elif "Valor (BOOL):" in nombre or "Valor (RESERVADA):" in nombre:
                val_str = nombre.split(":", 1)[1].strip()
                if val_str in ["true", "false"]:
                    tipo = "bool"
                    val = (val_str == "true")
                    nodo.tipo_dato = tipo
                    nodo.valor_constante = val
                    return tipo, val

            elif "Valor (STRING):" in nombre:
                val_str = nombre.split(":", 1)[1].strip()
                nodo.tipo_dato = "string"
                nodo.valor_constante = val_str
                return "string", val_str

            elif "Valor (ID):" in nombre:
                nombre_id = nombre.split(":", 1)[1].strip()
                simbolo = self.tabla.buscar(nombre_id)
                if not simbolo:
                    self.reportar_error(
                        f"Variable '{nombre_id}' no declarada",
                        nodo.linea,
                        nodo.columna
                    )
                    nodo.tipo_dato = "ERROR_TYPE"
                    return "ERROR_TYPE", None
                else:
                    self.tabla.registrar_uso(nombre_id, nodo.linea)
                    nodo.tipo_dato = simbolo.tipo
                    nodo.valor_constante = None  # Variable dinámica
                    return simbolo.tipo, None

        # ---------------------------------------------------------------------
        # 2. OPERADORES LÓGICOS (&&, ||)
        # ---------------------------------------------------------------------
        if nombre.startswith("Operador Logico:"):
            op = nombre.split(":", 1)[1].strip()
            if len(nodo.hijos) == 2:
                t1, v1 = self.evaluar_expresion(nodo.hijos[0])
                t2, v2 = self.evaluar_expresion(nodo.hijos[1])

                if t1 != "ERROR_TYPE" and t1 != "bool":
                    self.reportar_error(
                        f"El operando izquierdo de '{op}' debe ser booleano, se obtuvo '{t1}'",
                        nodo.hijos[0].linea or nodo.linea,
                        nodo.hijos[0].columna or nodo.columna
                    )
                if t2 != "ERROR_TYPE" and t2 != "bool":
                    self.reportar_error(
                        f"El operando derecho de '{op}' debe ser booleano, se obtuvo '{t2}'",
                        nodo.hijos[1].linea or nodo.linea,
                        nodo.hijos[1].columna or nodo.columna
                    )

                nodo.tipo_dato = "bool"
                if v1 is not None and v2 is not None:
                    if op == "&&":
                        nodo.valor_constante = bool(v1 and v2)
                    elif op == "||":
                        nodo.valor_constante = bool(v1 or v2)
                return "bool", nodo.valor_constante

        # ---------------------------------------------------------------------
        # 3. OPERADORES RELACIONALES (<, <=, >, >=, ==, !=)
        # ---------------------------------------------------------------------
        if nombre.startswith("Operador Relacional:"):
            op = nombre.split(":", 1)[1].strip()
            if len(nodo.hijos) == 2:
                t1, v1 = self.evaluar_expresion(nodo.hijos[0])
                t2, v2 = self.evaluar_expresion(nodo.hijos[1])

                nodo.tipo_dato = "bool"

                # Validación de tipos en comparación
                if t1 != "ERROR_TYPE" and t2 != "ERROR_TYPE":
                    es_num1 = t1 in ["int", "float", "real"]
                    es_num2 = t2 in ["int", "float", "real"]

                    if es_num1 != es_num2:
                        self.reportar_error(
                            f"No se pueden comparar tipos incompatibles '{t1}' y '{t2}' con el operador '{op}'",
                            nodo.linea,
                            nodo.columna
                        )

                # Constant folding para comparaciones relacionales
                if v1 is not None and v2 is not None:
                    try:
                        if op == "<": nodo.valor_constante = bool(v1 < v2)
                        elif op == "<=": nodo.valor_constante = bool(v1 <= v2)
                        elif op == ">": nodo.valor_constante = bool(v1 > v2)
                        elif op == ">=": nodo.valor_constante = bool(v1 >= v2)
                        elif op == "==": nodo.valor_constante = bool(v1 == v2)
                        elif op == "!=": nodo.valor_constante = bool(v1 != v2)
                    except Exception:
                        nodo.valor_constante = None

                return "bool", nodo.valor_constante

        # ---------------------------------------------------------------------
        # 4. OPERADORES ARITMÉTICOS (+, -, *, /, %, ^)
        # ---------------------------------------------------------------------
        if (nombre.startswith("Operador Suma/Resta:") or
            nombre.startswith("Operador Mult/Div:") or
            nombre.startswith("Operador Potencia:")):

            op = nombre.split(":", 1)[1].strip()
            if len(nodo.hijos) == 2:
                t1, v1 = self.evaluar_expresion(nodo.hijos[0])
                t2, v2 = self.evaluar_expresion(nodo.hijos[1])

                if t1 == "ERROR_TYPE" or t2 == "ERROR_TYPE":
                    nodo.tipo_dato = "ERROR_TYPE"
                    return "ERROR_TYPE", None

                # Verificamos que ambos sean numéricos
                es_num1 = t1 in ["int", "float", "real"]
                es_num2 = t2 in ["int", "float", "real"]

                if not es_num1 or not es_num2:
                    self.reportar_error(
                        f"Uso indebido del operador aritmético '{op}' con operandos de tipo '{t1}' y '{t2}'",
                        nodo.linea,
                        nodo.columna
                    )
                    nodo.tipo_dato = "ERROR_TYPE"
                    return "ERROR_TYPE", None

                # Regla de Módulo (%)
                if op == "%" and (t1 != "int" or t2 != "int"):
                    self.reportar_error(
                        f"El operador módulo '%' requiere operandos enteros, se encontró '{t1}' y '{t2}'",
                        nodo.linea,
                        nodo.columna
                    )

                # Tipo resultante con promoción int -> float
                if t1 in ["float", "real"] or t2 in ["float", "real"]:
                    tipo_resultante = "float"
                else:
                    tipo_resultante = "int"

                nodo.tipo_dato = tipo_resultante

                # Constant Folding (evaluación estática)
                if v1 is not None and v2 is not None:
                    try:
                        if op == "+":
                            res = v1 + v2
                        elif op == "-":
                            res = v1 - v2
                        elif op == "*":
                            res = v1 * v2
                        elif op == "/":
                            if v2 == 0:
                                self.reportar_error("División entre cero en tiempo de compilación", nodo.linea, nodo.columna)
                                res = None
                            else:
                                if tipo_resultante == "int":
                                    res = int(v1 // v2)
                                else:
                                    res = float(v1) / float(v2)
                        elif op == "%":
                            if v2 == 0:
                                self.reportar_error("Módulo con divisor cero en tiempo de compilación", nodo.linea, nodo.columna)
                                res = None
                            else:
                                res = int(v1) % int(v2)
                        elif op == "^":
                            res = v1 ** v2
                        else:
                            res = None

                        if res is not None:
                            if tipo_resultante == "float":
                                res = float(res)
                            elif tipo_resultante == "int":
                                res = int(res)

                        nodo.valor_constante = res
                    except Exception:
                        nodo.valor_constante = None

                return tipo_resultante, nodo.valor_constante

        # Si no coincide con ninguno, evaluamos el primer hijo (ej. paréntesis u otros nodos)
        if nodo.hijos:
            t, v = self.evaluar_expresion(nodo.hijos[0])
            nodo.tipo_dato = t
            nodo.valor_constante = v
            return t, v

        return "ERROR_TYPE", None
