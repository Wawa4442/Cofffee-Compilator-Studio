# -*- coding: utf-8 -*-
"""
===============================================================================
MÓDULO: intermedio.py (Equivalente a intermedio.h e intermedio.c)
PROYECTO: Coffee Compiler Studio - Fase Final (Código de Tres Direcciones .ci)
===============================================================================
Descripción:
    Recorre el Árbol Sintáctico Abstracto (AST) validado semánticamente y
    emite una representación intermedia didáctica en formato de Código de
    Tres Direcciones (archivo .ci).

    Utiliza:
      - Temporales simbólicos: t1, t2, t3, ... (nuevoTemporal)
      - Etiquetas simbólicas:  L1, L2, L3, ... (nuevaEtiqueta)
      - Cuádruplos / instrucciones explícitas:
          READ <id>
          WRITE <temp/val>
          <id> = <temp/val>
          <temp> = <op1> <operador> <op2>
          LABEL <Ln>
          IF_FALSE <cond> GOTO <Ln>
          IF_TRUE <cond> GOTO <Ln>
          GOTO <Ln>
===============================================================================
"""


class GeneradorCodigoIntermedio:
    """
    Generador de Código Intermedio de Tres Direcciones (.ci).
    """

    def __init__(self):
        self.contador_temporales = 0
        self.contador_etiquetas = 0
        self.lineas = []

    def limpiar(self):
        """Reinicia contadores y buffer de líneas para una nueva compilación."""
        self.contador_temporales = 0
        self.contador_etiquetas = 0
        self.lineas.clear()

    def nuevoTemporal(self) -> str:
        """Crea y retorna un nuevo nombre de variable temporal (t1, t2, ...)."""
        self.contador_temporales += 1
        return f"t{self.contador_temporales}"

    def nuevaEtiqueta(self) -> str:
        """Crea y retorna una nueva etiqueta simbólica de salto (L1, L2, ...)."""
        self.contador_etiquetas += 1
        return f"L{self.contador_etiquetas}"

    def emitir(self, instruccion: str):
        """Agrega una instrucción de tres direcciones al listado."""
        self.lineas.append(f"    {instruccion}")

    def emitir_etiqueta(self, etiqueta: str):
        """Agrega una etiqueta simbólica al listado."""
        self.lineas.append(f"LABEL {etiqueta}:")

    def emitir_comentario(self, texto: str):
        """Agrega un comentario descriptivo al código intermedio."""
        self.lineas.append(f"# {texto}")

    # =========================================================================
    # PUNTO DE ENTRADA PRINCIPAL
    # =========================================================================

    def generarCodigoIntermedio(self, ast_raiz, ruta_archivo_ci=None) -> str:
        """
        Recorre el AST completo y genera el código intermedio de 3 direcciones.
        Si se proporciona 'ruta_archivo_ci', guarda el resultado en disco (.ci).
        """
        self.limpiar()
        self.emitir_comentario("==========================================================")
        self.emitir_comentario("CÓDIGO INTERMEDIO DE TRES DIRECCIONES (.ci)")
        self.emitir_comentario("Coffee Compiler Studio - Compiladores II UAA")
        self.emitir_comentario("==========================================================")
        self.lineas.append("BEGIN_MAIN")

        if ast_raiz:
            self.cGen(ast_raiz)

        self.lineas.append("END_MAIN")
        contenido = "\n".join(self.lineas) + "\n"

        if ruta_archivo_ci:
            try:
                with open(ruta_archivo_ci, "w", encoding="utf-8") as f:
                    f.write(contenido)
            except Exception:
                pass

        return contenido

    # =========================================================================
    # RECORRIDO DEL AST (SENTENCIAS Y EXPRESIONES)
    # =========================================================================

    def cGen(self, nodo):
        """Despachador general para nodos del AST."""
        if not nodo:
            return

        nombre = nodo.nombre

        if nombre in ["Programa", "Bloque_Sentencias", "Declaracion", "Rama_Else"]:
            for hijo in nodo.hijos:
                self.cGen(hijo)

        elif nombre == "Declaracion_Variable":
            self.genDecl(nodo)

        elif nombre in [
            "Entrada_Cin",
            "Salida_Cout",
            "Asignacion_u_Operacion",
            "Sentencia_If",
            "Sentencia_While",
            "Sentencia_Do"
        ]:
            self.genStmt(nodo)

        else:
            for hijo in nodo.hijos:
                self.cGen(hijo)

    def genDecl(self, nodo):
        """Emite información declarativa para variables."""
        if not nodo.hijos:
            return
        primer_hijo = nodo.hijos[0]
        tipo = primer_hijo.nombre.split(":", 1)[1].strip() if ":" in primer_hijo.nombre else "var"
        ids = []
        for h in nodo.hijos[1:]:
            if "ID:" in h.nombre:
                ids.append(h.nombre.split(":", 1)[1].strip())
        if ids:
            self.emitir_comentario(f"Declaración ({tipo}): {', '.join(ids)}")

    def genStmt(self, nodo):
        """Genera código de 3 direcciones para los distintos tipos de sentencias."""
        nombre = nodo.nombre

        # 1. Entrada (cin >> id;)
        if nombre == "Entrada_Cin":
            for hijo in nodo.hijos:
                if "ID Destino:" in hijo.nombre:
                    var_name = hijo.nombre.split(":", 1)[1].strip()
                    self.emitir(f"READ {var_name}")

        # 2. Salida (cout << expr;)
        elif nombre == "Salida_Cout":
            for hijo in nodo.hijos:
                if not hijo.nombre.startswith("Operador:"):
                    res = self.genExp(hijo)
                    self.emitir(f"WRITE {res}")

        # 3. Asignación o incremento/decremento unario
        elif nombre == "Asignacion_u_Operacion":
            if not nodo.hijos:
                return
            hijo_id = nodo.hijos[0]
            var_name = hijo_id.nombre.split(":", 1)[1].strip() if ":" in hijo_id.nombre else hijo_id.nombre

            if len(nodo.hijos) > 1 and "Operador Unario:" in nodo.hijos[1].nombre:
                op_unario = nodo.hijos[1].nombre.split(":", 1)[1].strip()
                temp = self.nuevoTemporal()
                if op_unario == "++":
                    self.emitir(f"{temp} = {var_name} + 1")
                else:
                    self.emitir(f"{temp} = {var_name} - 1")
                self.emitir(f"{var_name} = {temp}")
            elif len(nodo.hijos) > 1:
                res_exp = self.genExp(nodo.hijos[1])
                self.emitir(f"{var_name} = {res_exp}")

        # 4. Selección (if ... then ... [else ...] end)
        elif nombre == "Sentencia_If":
            if len(nodo.hijos) < 2:
                return
            nodo_cond = nodo.hijos[0]
            nodo_then = nodo.hijos[1]
            nodo_else = nodo.hijos[2] if len(nodo.hijos) > 2 else None

            cond_temp = self.genExp(nodo_cond)

            if nodo_else:
                etiq_else = self.nuevaEtiqueta()
                etiq_fin = self.nuevaEtiqueta()
                self.emitir(f"IF_FALSE {cond_temp} GOTO {etiq_else}")
                self.cGen(nodo_then)
                self.emitir(f"GOTO {etiq_fin}")
                self.emitir_etiqueta(etiq_else)
                self.cGen(nodo_else)
                self.emitir_etiqueta(etiq_fin)
            else:
                etiq_fin = self.nuevaEtiqueta()
                self.emitir(f"IF_FALSE {cond_temp} GOTO {etiq_fin}")
                self.cGen(nodo_then)
                self.emitir_etiqueta(etiq_fin)

        # 5. Iteración (while (cond) { ... })
        elif nombre == "Sentencia_While":
            if len(nodo.hijos) < 2:
                return
            nodo_cond = nodo.hijos[0]
            nodo_cuerpo = nodo.hijos[1]

            etiq_inicio = self.nuevaEtiqueta()
            etiq_fin = self.nuevaEtiqueta()

            self.emitir_etiqueta(etiq_inicio)
            cond_temp = self.genExp(nodo_cond)
            self.emitir(f"IF_FALSE {cond_temp} GOTO {etiq_fin}")
            self.cGen(nodo_cuerpo)
            self.emitir(f"GOTO {etiq_inicio}")
            self.emitir_etiqueta(etiq_fin)

        # 6. Repetición (do ... until (cond);)
        elif nombre == "Sentencia_Do":
            nodo_cuerpo = None
            tipo_cierre = "until"
            nodo_cond = None

            for hijo in nodo.hijos:
                if hijo.nombre == "Bloque_Sentencias":
                    nodo_cuerpo = hijo
                elif "Condicion:" in hijo.nombre:
                    tipo_cierre = hijo.nombre.split(":", 1)[1].strip()
                else:
                    nodo_cond = hijo

            etiq_inicio = self.nuevaEtiqueta()
            self.emitir_etiqueta(etiq_inicio)
            if nodo_cuerpo:
                self.cGen(nodo_cuerpo)
            if nodo_cond:
                cond_temp = self.genExp(nodo_cond)
                if tipo_cierre == "until":
                    self.emitir(f"IF_FALSE {cond_temp} GOTO {etiq_inicio}")
                else:
                    self.emitir(f"IF_TRUE {cond_temp} GOTO {etiq_inicio}")

    def genExp(self, nodo) -> str:
        """
        Evalúa un nodo de expresión, emite las instrucciones de 3 direcciones
        necesarias y retorna el nombre del temporal o valor resultante.
        """
        if not nodo:
            return "0"

        nombre = nodo.nombre

        # Nodos hoja (Literales e Identificadores)
        if nombre.startswith("Valor ("):
            val_str = nombre.split(":", 1)[1].strip() if ":" in nombre else nombre
            if "Valor (BOOL):" in nombre or "Valor (RESERVADA):" in nombre:
                return "1" if val_str == "true" else "0"
            return val_str

        # Nodos de operadores binarios (Aritméticos, Relacionales, Lógicos)
        if (
            nombre.startswith("Operador Suma/Resta:")
            or nombre.startswith("Operador Mult/Div:")
            or nombre.startswith("Operador Potencia:")
            or nombre.startswith("Operador Relacional:")
            or nombre.startswith("Operador Logico:")
        ):
            op = nombre.split(":", 1)[1].strip()
            if len(nodo.hijos) == 2:
                izq = self.genExp(nodo.hijos[0])
                der = self.genExp(nodo.hijos[1])
                temp = self.nuevoTemporal()
                self.emitir(f"{temp} = {izq} {op} {der}")
                return temp

        if nodo.hijos:
            return self.genExp(nodo.hijos[0])

        return "0"
