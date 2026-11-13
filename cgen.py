# -*- coding: utf-8 -*-
"""
===============================================================================
MÓDULO: cgen.py (Equivalente a cgen.h y cgen.c de Kenneth C. Louden)
PROYECTO: Coffee Compiler Studio - Fase Final (Generador de Código TM)
===============================================================================
Descripción:
    Implementa el generador de código objeto para la máquina virtual
    Tiny Machine (TM). Recorre el Árbol Sintáctico Abstracto (AST) validado
    por el analizador semántico y consulta la Tabla de Símbolos (SymbolTable)
    para traducir el programa fuente en un archivo de instrucciones .tm.

Estructuras soportadas:
    1. Secuenciales:
       - Declaración de variables y mapeo a memoria global (gp = 5).
       - Entrada estándar (cin >> id) mediante instrucción RO 'IN'.
       - Salida estándar (cout << exp) mediante instrucción RO 'OUT'.
       - Asignaciones (id = exp) e incremento/decremento unario (id++, id--).
    2. Selectivas:
       - Sentencias condicionales 'if ... then ... end' e
         'if ... then ... else ... end' usando backpatching con
         emitSkip, emitBackup, emitRestore y emitRM_Abs.
    3. Repetitivas:
       - Ciclos 'while (cond) { ... }' con evaluación previa y salto atrás.
       - Ciclos 'do { ... } until (cond);' con evaluación posterior y salto
         condicional hacia atrás.
    4. Expresiones:
       - Aritméticas: +, -, *, /, % (módulo entero), ^ (potencia iterativa).
       - Relacionales: <, <=, >, >=, ==, !=.
       - Lógicas: && (AND), || (OR).
===============================================================================
"""

from code_tm import CodeEmitterTM, pc, mp, gp, ac, ac1


class CodeGeneratorTM:
    """
    Generador de Código Objeto para la Tiny Machine (.tm).
    """

    def __init__(self, tabla_simbolos, trace_code=True):
        self.tabla = tabla_simbolos
        self.emitter = CodeEmitterTM(trace_code=trace_code)
        # tmpOffset es el desplazamiento en la pila de temporales relativa a mp (reg 6).
        # Se decrementa al apilar un temporal y se incrementa al desapilarlo.
        self.tmpOffset = 0

    # =========================================================================
    # CONSULTA A LA TABLA DE SÍMBOLOS (Equivalente a st_lookup)
    # =========================================================================

    def st_lookup(self, nombre_id: str) -> int:
        """
        Consulta la Tabla de Símbolos (SymbolTable) y retorna la localidad
        de palabra (0, 1, 2, ...) relativa al registro gp (5).
        En nuestra Tabla de Símbolos cada variable tiene un offset en bytes
        (0, 4, 8, ...), por lo que su localidad en dMem es offset // 4.
        """
        if not self.tabla:
            return 0
        simbolo = self.tabla.buscar(nombre_id)
        if simbolo and simbolo.offset is not None:
            return simbolo.offset // 4
        return -1

    def obtener_tipo_simbolo(self, nombre_id: str) -> str:
        """Retorna el tipo de dato registrado en la Tabla de Símbolos ('int', 'float', 'bool')."""
        if not self.tabla:
            return "int"
        simbolo = self.tabla.buscar(nombre_id)
        if simbolo:
            return simbolo.tipo
        return "int"

    # =========================================================================
    # FUNCIÓN PRINCIPAL DE GENERACIÓN (Equivalente a codeGen en cgen.c)
    # =========================================================================

    def codeGen(self, syntaxTree, codefile_path=None) -> str:
        """
        Genera el código objeto Tiny Machine (.tm) recorriendo el AST.
        Incluye el preludio estándar de inicialización de registros (mp y dMem[0])
        y la instrucción final de parada HALT.
        """
        self.emitter.limpiar()
        self.tmpOffset = 0

        self.emitter.emitComment("Compilacion de Coffee Compiler Studio para Tiny Machine (.tm)")
        if codefile_path:
            self.emitter.emitComment(f"Archivo objeto: {codefile_path}")

        # 1. Preludio estándar de la Tiny Machine (Louden)
        self.emitter.emitComment("Preludio estandar:")
        self.emitter.emitRM("LD", mp, 0, ac, "cargar mp con la direccion maxima desde localidad 0")
        self.emitter.emitRM("ST", ac, 0, ac, "limpiar localidad 0")
        self.emitter.emitComment("Fin del preludio estandar.")

        # 2. Recorrido del Árbol Sintáctico Abstracto
        self.cGen(syntaxTree)

        # 3. Epílogo: Instrucción de parada HALT
        self.emitter.emitComment("Fin de la ejecucion.")
        self.emitter.emitRO("HALT", 0, 0, 0, "")

        codigo_tm = self.emitter.obtener_codigo_tm(ordenado_por_localidad=True)

        if codefile_path:
            try:
                with open(codefile_path, "w", encoding="utf-8") as f:
                    f.write(codigo_tm)
            except Exception:
                pass

        return codigo_tm

    # =========================================================================
    # DESPACHADOR RECURSIVO DEL AST (cGen)
    # =========================================================================

    def cGen(self, tree):
        """
        Recorre recursivamente los nodos de bloque y despacha sentencias
        individuales o expresiones.
        """
        if not tree:
            return

        nombre = tree.nombre

        if nombre in ["Programa", "Bloque_Sentencias", "Declaracion", "Rama_Else"]:
            for hijo in tree.hijos:
                self.cGen(hijo)

        elif nombre == "Declaracion_Variable":
            self.genDecl(tree)

        elif nombre in [
            "Entrada_Cin",
            "Salida_Cout",
            "Asignacion_u_Operacion",
            "Sentencia_If",
            "Sentencia_While",
            "Sentencia_Do"
        ]:
            self.genStmt(tree)

        else:
            self.genExp(tree)

    # =========================================================================
    # GENERACIÓN DE DECLARACIONES Y SENTENCIAS (genStmt)
    # =========================================================================

    def genDecl(self, tree):
        """
        Documenta en los comentarios del archivo .tm las localidades de memoria
        asignadas en la Tabla de Símbolos para cada variable declarada.
        """
        if not tree.hijos:
            return
        for hijo in tree.hijos[1:]:
            if "ID:" in hijo.nombre:
                var_name = hijo.nombre.split(":", 1)[1].strip()
                loc = self.st_lookup(var_name)
                tipo = self.obtener_tipo_simbolo(var_name)
                if loc >= 0:
                    self.emitter.emitComment(
                        f"Variable '{var_name}' ({tipo}) asignada en dMem[gp+{loc}] (offset {loc * 4} B)"
                    )

    def genStmt(self, tree):
        """
        Genera instrucciones TM para un nodo de sentencia (cin, cout, assign,
        if, while, do-until).
        """
        nombre = tree.nombre

        # ---------------------------------------------------------------------
        # 1. ENTRADA: cin >> id;
        # ---------------------------------------------------------------------
        if nombre == "Entrada_Cin":
            self.emitter.emitComment("-> cin (lectura)")
            var_name = None
            for hijo in tree.hijos:
                if "ID Destino:" in hijo.nombre:
                    var_name = hijo.nombre.split(":", 1)[1].strip()
                    break

            if var_name:
                loc = self.st_lookup(var_name)
                tipo_var = self.obtener_tipo_simbolo(var_name)
                self.emitter.emitRO("IN", ac, 0, 0, f"leer valor para '{var_name}' ({tipo_var})")
                if tipo_var in ["float", "real"]:
                    self.emitter.emitRM("LDC", ac1, 0.0, 0, "constante 0.0 para promover a float")
                    self.emitter.emitRO("ADD", ac, ac, ac1, f"convertir '{var_name}' a float")
                self.emitter.emitRM("ST", ac, loc, gp, f"cin: almacenar valor en '{var_name}'")
            self.emitter.emitComment("<- cin")

        # ---------------------------------------------------------------------
        # 2. SALIDA: cout << expr;
        # ---------------------------------------------------------------------
        elif nombre == "Salida_Cout":
            self.emitter.emitComment("-> cout (escritura)")
            for hijo in tree.hijos:
                if not hijo.nombre.startswith("Operador:"):
                    self.genExp(hijo)
                    self.emitter.emitRO("OUT", ac, 0, 0, "cout: escribir valor de ac")
            self.emitter.emitComment("<- cout")

        # ---------------------------------------------------------------------
        # 3. ASIGNACIÓN O INCREMENTO/DECREMENTO UNARIO: id = expr; | id++; | id--;
        # ---------------------------------------------------------------------
        elif nombre == "Asignacion_u_Operacion":
            if not tree.hijos:
                return
            hijo_id = tree.hijos[0]
            var_name = hijo_id.nombre.split(":", 1)[1].strip() if ":" in hijo_id.nombre else hijo_id.nombre
            loc = self.st_lookup(var_name)
            tipo_var = self.obtener_tipo_simbolo(var_name)

            # Caso A: Operador unario (++ / --)
            if len(tree.hijos) > 1 and "Operador Unario:" in tree.hijos[1].nombre:
                op_unario = tree.hijos[1].nombre.split(":", 1)[1].strip()
                self.emitter.emitComment(f"-> operador unario {var_name}{op_unario}")
                self.emitter.emitRM("LD", ac, loc, gp, f"cargar '{var_name}'")
                self.emitter.emitRM("LDC", ac1, 1, 0, "cargar constante 1")
                if op_unario == "++":
                    self.emitter.emitRO("ADD", ac, ac, ac1, f"incrementar '{var_name}'")
                else:
                    self.emitter.emitRO("SUB", ac, ac, ac1, f"decrementar '{var_name}'")
                self.emitter.emitRM("ST", ac, loc, gp, f"guardar nuevo valor en '{var_name}'")
                self.emitter.emitComment(f"<- operador unario {var_name}{op_unario}")

            # Caso B: Asignación estándar (id = expr;)
            elif len(tree.hijos) > 1:
                self.emitter.emitComment(f"-> asignacion a '{var_name}'")
                nodo_exp = tree.hijos[1]
                self.genExp(nodo_exp)
                if tipo_var in ["float", "real"]:
                    self.emitter.emitRM("LDC", ac1, 0.0, 0, "asegurar representacion float")
                    self.emitter.emitRO("ADD", ac, ac, ac1, f"promover resultado a float para '{var_name}'")
                self.emitter.emitRM("ST", ac, loc, gp, f"asignar: guardar valor en '{var_name}'")
                self.emitter.emitComment(f"<- asignacion a '{var_name}'")

        # ---------------------------------------------------------------------
        # 4. ESTRUCTURA SELECTIVA: if <cond> then <bloque_then> [else <bloque_else>] end
        # ---------------------------------------------------------------------
        elif nombre == "Sentencia_If":
            if len(tree.hijos) < 2:
                return
            self.emitter.emitComment("-> if")
            p1 = tree.hijos[0]  # Condición
            p2 = tree.hijos[1]  # Bloque Then
            p3 = tree.hijos[2] if len(tree.hijos) > 2 else None  # Rama Else opcional

            # Evaluar la expresión de condición (deja 1 o 0 en ac)
            self.genExp(p1)
            # Reservar espacio para el salto condicional hacia el else (o al final si no hay else)
            savedLoc1 = self.emitter.emitSkip(1)
            self.emitter.emitComment("if: el salto hacia else/fin va aqui")

            # Generar código para la rama Then
            self.cGen(p2)

            if p3 is not None:
                # Si existe rama Else, reservamos el salto incondicional al final tras ejecutar Then
                savedLoc2 = self.emitter.emitSkip(1)
                self.emitter.emitComment("if: el salto hacia el final va aqui")

                # Parchar el salto condicional (savedLoc1) hacia el inicio del Else
                currentLoc = self.emitter.emitSkip(0)
                self.emitter.emitBackup(savedLoc1)
                self.emitter.emitRM_Abs("JEQ", ac, currentLoc, "if: jmp a else si condicion es falsa")
                self.emitter.emitRestore()

                # Generar código para la rama Else
                self.emitter.emitComment("if: rama else")
                self.cGen(p3)

                # Parchar el salto incondicional (savedLoc2) hacia el final del If
                currentLoc = self.emitter.emitSkip(0)
                self.emitter.emitBackup(savedLoc2)
                self.emitter.emitRM_Abs("LDA", pc, currentLoc, "if: jmp al final")
                self.emitter.emitRestore()
            else:
                # Si NO existe rama Else, sólo parchamos savedLoc1 hacia el final del If
                currentLoc = self.emitter.emitSkip(0)
                self.emitter.emitBackup(savedLoc1)
                self.emitter.emitRM_Abs("JEQ", ac, currentLoc, "if: jmp al final si condicion es falsa")
                self.emitter.emitRestore()

            self.emitter.emitComment("<- if")

        # ---------------------------------------------------------------------
        # 5. ESTRUCTURA REPETITIVA: while (<cond>) { <bloque> }
        # ---------------------------------------------------------------------
        elif nombre == "Sentencia_While":
            if len(tree.hijos) < 2:
                return
            self.emitter.emitComment("-> while")
            nodo_cond = tree.hijos[0]
            nodo_cuerpo = tree.hijos[1]

            # Localidad de inicio donde se re-evalúa la condición en cada iteración
            locInicio = self.emitter.emitSkip(0)
            self.emitter.emitComment("while: evaluar condicion")
            self.genExp(nodo_cond)

            # Reservar instrucción para saltar fuera del ciclo cuando la condición sea falsa (0)
            savedLocFin = self.emitter.emitSkip(1)
            self.emitter.emitComment("while: salto hacia el final si es falso")

            # Generar el cuerpo del ciclo while
            self.cGen(nodo_cuerpo)

            # Salto incondicional hacia atrás para volver a evaluar la condición
            self.emitter.emitRM_Abs("LDA", pc, locInicio, "while: regresar al inicio del ciclo")

            # Parchar el salto condicional de salida (savedLocFin) hacia la localidad actual
            locFin = self.emitter.emitSkip(0)
            self.emitter.emitBackup(savedLocFin)
            self.emitter.emitRM_Abs("JEQ", ac, locFin, "while: salir del ciclo si condicion es falsa")
            self.emitter.emitRestore()
            self.emitter.emitComment("<- while")

        # ---------------------------------------------------------------------
        # 6. ESTRUCTURA REPETITIVA: do { <bloque> } until (<cond>);
        # ---------------------------------------------------------------------
        elif nombre == "Sentencia_Do":
            self.emitter.emitComment("-> do-until")
            nodo_cuerpo = None
            tipo_cierre = "until"
            nodo_cond = None

            for hijo in tree.hijos:
                if hijo.nombre == "Bloque_Sentencias":
                    nodo_cuerpo = hijo
                elif "Condicion:" in hijo.nombre:
                    tipo_cierre = hijo.nombre.split(":", 1)[1].strip()
                else:
                    nodo_cond = hijo

            # Guardar la dirección de inicio del cuerpo para el salto hacia atrás
            locInicio = self.emitter.emitSkip(0)
            self.emitter.emitComment("do: inicio del cuerpo del ciclo")

            if nodo_cuerpo:
                self.cGen(nodo_cuerpo)

            if nodo_cond:
                self.emitter.emitComment(f"do: evaluar condicion de cierre ({tipo_cierre})")
                self.genExp(nodo_cond)
                if tipo_cierre == "until":
                    # En repeat/do-until se repite mientras la condición de paro sea FALSA (ac == 0)
                    self.emitter.emitRM_Abs("JEQ", ac, locInicio, "do-until: regresar al inicio si condicion es falsa")
                else:
                    # En do-while se repite mientras la condición sea VERDADERA (ac != 0)
                    self.emitter.emitRM_Abs("JNE", ac, locInicio, "do-while: regresar al inicio si condicion es verdadera")

            self.emitter.emitComment("<- do-until")

    # =========================================================================
    # GENERACIÓN DE EXPRESIONES (genExp)
    # =========================================================================

    def genExp(self, tree):
        """
        Genera código TM para evaluar cualquier expresión aritmética,
        relacional o lógica, dejando siempre el resultado en el acumulador ac (0).
        """
        if not tree:
            return

        nombre = tree.nombre

        # ---------------------------------------------------------------------
        # 1. NODOS HOJA: Constantes numéricas, booleanas e identificadores
        # ---------------------------------------------------------------------
        if nombre.startswith("Valor ("):
            if "Valor (NUM):" in nombre:
                val_str = nombre.split(":", 1)[1].strip()
                self.emitter.emitComment(f"-> constante ({val_str})")
                if "." in val_str:
                    val = float(val_str)
                else:
                    val = int(val_str)
                self.emitter.emitRM("LDC", ac, val, 0, f"cargar constante {val_str}")
                self.emitter.emitComment("<- constante")
                return

            elif "Valor (BOOL):" in nombre or "Valor (RESERVADA):" in nombre:
                val_str = nombre.split(":", 1)[1].strip()
                val_num = 1 if val_str == "true" else 0
                self.emitter.emitComment(f"-> booleano ({val_str})")
                self.emitter.emitRM("LDC", ac, val_num, 0, f"cargar booleano {val_str} ({val_num})")
                self.emitter.emitComment("<- booleano")
                return

            elif "Valor (ID):" in nombre:
                var_name = nombre.split(":", 1)[1].strip()
                self.emitter.emitComment(f"-> identificador ({var_name})")
                loc = self.st_lookup(var_name)
                self.emitter.emitRM("LD", ac, loc, gp, f"cargar valor de '{var_name}'")
                self.emitter.emitComment("<- identificador")
                return

        # ---------------------------------------------------------------------
        # 2. OPERADORES BINARIOS (Aritméticos, Relacionales y Lógicos)
        # ---------------------------------------------------------------------
        if (
            nombre.startswith("Operador Suma/Resta:")
            or nombre.startswith("Operador Mult/Div:")
            or nombre.startswith("Operador Potencia:")
            or nombre.startswith("Operador Relacional:")
            or nombre.startswith("Operador Logico:")
        ):
            op = nombre.split(":", 1)[1].strip()
            if len(tree.hijos) < 2:
                return

            self.emitter.emitComment(f"-> operador ({op})")
            p1 = tree.hijos[0]  # Operando izquierdo
            p2 = tree.hijos[1]  # Operando derecho

            # Evaluar operando izquierdo (deja el resultado en ac)
            self.genExp(p1)

            # Guardar el operando izquierdo en la pila de temporales (dMem[mp + tmpOffset])
            self.emitter.emitRM("ST", ac, self.tmpOffset, mp, "op: push operando izquierdo en temporal")
            self.tmpOffset -= 1

            # Evaluar operando derecho (deja el resultado en ac)
            self.genExp(p2)

            # Recuperar el operando izquierdo desde la pila de temporales hacia ac1
            self.tmpOffset += 1
            self.emitter.emitRM("LD", ac1, self.tmpOffset, mp, "op: cargar operando izquierdo en ac1")

            # --- A. Operadores Aritméticos Básicos (+, -, *, /) ---
            if op == "+":
                self.emitter.emitRO("ADD", ac, ac1, ac, "op +")
            elif op == "-":
                self.emitter.emitRO("SUB", ac, ac1, ac, "op -")
            elif op == "*":
                self.emitter.emitRO("MUL", ac, ac1, ac, "op *")
            elif op == "/":
                # Si el nodo de división fue inferido como float por el analizador semántico,
                # garantizamos que ac1 sea float para que DIV realice división real exacta.
                if getattr(tree, "tipo_dato", None) in ["float", "real"]:
                    self.emitter.emitRM("ST", ac, self.tmpOffset, mp, "div: resguardar divisor")
                    self.emitter.emitRM("LDC", ac, 0.0, 0, "div: constante 0.0")
                    self.emitter.emitRO("ADD", ac1, ac1, ac, "div: asegurar dividendo float")
                    self.emitter.emitRM("LD", ac, self.tmpOffset, mp, "div: restaurar divisor")
                self.emitter.emitRO("DIV", ac, ac1, ac, "op /")

            # --- B. Operador Módulo Entero (%) -> ac = ac1 - (ac1 / ac) * ac ---
            elif op == "%":
                self.emitter.emitRM("ST", ac1, self.tmpOffset, mp, "mod: guardar dividendo a")
                self.emitter.emitRM("ST", ac, self.tmpOffset - 1, mp, "mod: guardar divisor b")
                self.emitter.emitRO("DIV", ac, ac1, ac, "mod: cociente entero q = a / b")
                self.emitter.emitRM("LD", ac1, self.tmpOffset - 1, mp, "mod: recuperar divisor b")
                self.emitter.emitRO("MUL", ac, ac, ac1, "mod: producto p = q * b")
                self.emitter.emitRM("LD", ac1, self.tmpOffset, mp, "mod: recuperar dividendo a")
                self.emitter.emitRO("SUB", ac, ac1, ac, "mod: residuo r = a - (a / b) * b")

            # --- C. Operador Potencia (^) -> multiplicación iterativa ac1 ^ ac ---
            elif op == "^":
                offset_base = self.tmpOffset
                offset_exp = self.tmpOffset - 1
                self.emitter.emitRM("ST", ac1, offset_base, mp, "pow: guardar base")
                self.emitter.emitRM("ST", ac, offset_exp, mp, "pow: guardar exponente")
                self.emitter.emitRM("LDC", ac, 1, 0, "pow: inicializar acumulador en 1")
                locLoop = self.emitter.emitSkip(0)
                self.emitter.emitRM("LD", ac1, offset_exp, mp, "pow: cargar contador exponente")
                savedExit = self.emitter.emitSkip(1)
                self.emitter.emitRM("LD", ac1, offset_base, mp, "pow: cargar base")
                self.emitter.emitRO("MUL", ac, ac, ac1, "pow: multiplicar acumulador por base")
                self.emitter.emitRM("LD", ac1, offset_exp, mp, "pow: cargar exponente")
                self.emitter.emitRM("LDA", ac1, -1, ac1, "pow: decrementar exponente en 1")
                self.emitter.emitRM("ST", ac1, offset_exp, mp, "pow: actualizar exponente")
                self.emitter.emitRM_Abs("LDA", pc, locLoop, "pow: repetir ciclo de potencia")
                locEnd = self.emitter.emitSkip(0)
                self.emitter.emitBackup(savedExit)
                self.emitter.emitRM_Abs("JLE", ac1, locEnd, "pow: terminar si exponente <= 0")
                self.emitter.emitRestore()

            # --- D. Operadores Relacionales (<, <=, >, >=, ==, !=) ---
            elif op in ["<", "<=", ">", ">=", "==", "!="]:
                self.emitter.emitRO("SUB", ac, ac1, ac, f"op {op} (comparar ac1 - ac)")
                mapa_saltos = {
                    "<": "JLT",
                    "<=": "JLE",
                    ">": "JGT",
                    ">=": "JGE",
                    "==": "JEQ",
                    "!=": "JNE"
                }
                instruccion_salto = mapa_saltos[op]
                self.emitter.emitRM(instruccion_salto, ac, 2, pc, f"saltar a caso verdadero si {op}")
                self.emitter.emitRM("LDC", ac, 0, 0, "caso falso (ac = 0)")
                self.emitter.emitRM("LDA", pc, 1, pc, "saltar caso verdadero")
                self.emitter.emitRM("LDC", ac, 1, 0, "caso verdadero (ac = 1)")

            # --- E. Operadores Lógicos (&&, ||) ---
            elif op == "&&":
                self.emitter.emitRM("JEQ", ac1, 3, pc, "AND: si izq es falso (0), saltar a falso")
                self.emitter.emitRM("JEQ", ac, 2, pc, "AND: si der es falso (0), saltar a falso")
                self.emitter.emitRM("LDC", ac, 1, 0, "AND: ambos verdaderos (ac = 1)")
                self.emitter.emitRM("LDA", pc, 1, pc, "AND: saltar caso falso")
                self.emitter.emitRM("LDC", ac, 0, 0, "AND: caso falso (ac = 0)")

            elif op == "||":
                self.emitter.emitRM("JNE", ac1, 3, pc, "OR: si izq es verdadero (!=0), saltar a verdadero")
                self.emitter.emitRM("JNE", ac, 2, pc, "OR: si der es verdadero (!=0), saltar a verdadero")
                self.emitter.emitRM("LDC", ac, 0, 0, "OR: ambos falsos (ac = 0)")
                self.emitter.emitRM("LDA", pc, 1, pc, "OR: saltar caso verdadero")
                self.emitter.emitRM("LDC", ac, 1, 0, "OR: caso verdadero (ac = 1)")

            self.emitter.emitComment(f"<- operador ({op})")
            return

        # Si es un nodo envoltorio, evaluar su primer hijo
        if tree.hijos:
            self.genExp(tree.hijos[0])
