# -*- coding: utf-8 -*-
"""
===============================================================================
MÓDULO: tm_simulator.py (Equivalente a tm.c de Kenneth C. Louden)
PROYECTO: Coffee Compiler Studio - Simulador de la Máquina Virtual Tiny Machine
===============================================================================
Descripción:
    Implementa la máquina virtual Tiny Machine (TM) encargada de cargar en
    memoria de instrucciones (iMem) y ejecutar paso a paso exclusivamente
    el archivo objeto '.tm' generado por cgen.py.

Arquitectura de la Tiny Machine:
    - IADDR_SIZE = 4096 (Tamaño de la memoria de instrucciones iMem)
    - DADDR_SIZE = 4096 (Tamaño de la memoria de datos dMem)
    - NO_REGS    = 8    (Registros r0..r7, donde r7 es el Program Counter 'pc',
                         r6 es 'mp' y r5 es 'gp')
    - Inicialización estándar:
        * Todos los registros r0..r7 inician en 0.
        * dMem[0] inicia con el valor (DADDR_SIZE - 1) para que el preludio
          estándar (0: LD 6,0(0)) cargue automáticamente el puntero 'mp' en el
          tope superior de la memoria de datos.

JUSTIFICACIÓN ACADÉMICA DE LA EXTENSIÓN HÍBRIDA (INT / FLOAT) EN TM:
    1. En la especificación original de Kenneth C. Louden (Compiler Construction:
       Principles and Practice), el lenguaje TINY sólo contempla el tipo 'int',
       por lo que 'dMem[]', 'reg[]' y el operando 'iarg2' de 'LDC' se declaran
       como 'int'.
    2. Sin embargo, la gramática oficial de nuestro proyecto y el banco de 12
       grupos de ejercicios finales requieren soporte completo para números
       reales ('float' / 'real'), incluyendo constantes con punto decimal
       (ej. PI = 3.1416, porcentajes 0.15, 0.40, costos 7.59, 3.03, fórmulas
       de conversión de temperatura y promedios).
    3. Por ello, esta implementación mantiene el 100% del conjunto de
       instrucciones oficial de Louden (RO: HALT, IN, OUT, ADD, SUB, MUL, DIV;
       RM: LD, ST, LDA, LDC, JLT, JLE, JGT, JGE, JEQ, JNE) y su direccionamiento
       relativo a registros, permitiendo que las celdas de registro y de datos
       almacenen valores numéricos enteros (int) o de punto flotante (float)
       según el tipo de operando:
         - Si ambos operandos de DIV son enteros ('int'), realiza división
           entera truncada hacia cero (preservando algoritmos enteros como el
           operador módulo '%' y la conjetura de Ulam).
         - Si al menos uno de los operandos es 'float', realiza división en
           punto flotante de precisión real.
===============================================================================
"""

import re
import sys


# Constantes de arquitectura de la máquina TM
IADDR_SIZE = 4096
DADDR_SIZE = 4096
NO_REGS = 8
PC_REG = 7

# Clasificación de instrucciones (idéntica a OpClass en tm.c)
OPCLASS_RO = "RO"  # Register-Only: r, s, t
OPCLASS_RM = "RM"  # Register-Memory: r, d(s)

OPCODES_RO = {"HALT", "IN", "OUT", "ADD", "SUB", "MUL", "DIV"}
OPCODES_RM = {"LD", "ST", "LDA", "LDC", "JLT", "JLE", "JGT", "JGE", "JEQ", "JNE"}


class InstruccionTM:
    """Representa una instrucción cargada en la memoria iMem de la Tiny Machine."""

    def __init__(self, loc: int, iop: str, iarg1: int, iarg2, iarg3: int, comentario: str = ""):
        self.loc = loc
        self.iop = iop
        self.opclass = OPCLASS_RO if iop in OPCODES_RO else OPCLASS_RM
        self.iarg1 = iarg1  # Registro r
        self.iarg2 = iarg2  # Registro s (en RO) o desplazamiento/constante d (en RM)
        self.iarg3 = iarg3  # Registro t (en RO) o registro base s (en RM)
        self.comentario = comentario

    def __repr__(self):
        if self.opclass == OPCLASS_RO:
            return f"{self.loc:3d}: {self.iop:5s} {self.iarg1},{self.iarg2},{self.iarg3}"
        return f"{self.loc:3d}: {self.iop:5s} {self.iarg1},{self.iarg2}({self.iarg3})"


def formatear_numero_tm(valor) -> str:
    """
    Formatea un valor numérico de salida (OUT) de forma limpia:
    - Si es int, lo imprime como entero.
    - Si es float, elimina errores de redondeo IEEE-754 (ej. 7.590000000000001 -> 7.59),
      conservando los decimales significativos.
    """
    if isinstance(valor, int):
        return str(valor)
    if isinstance(valor, float):
        # Redondear a 6 decimales para eliminar ruido binario de punto flotante
        redondeado = round(valor, 6)
        texto = f"{redondeado:.6f}".rstrip("0").rstrip(".")
        return texto if texto != "-0" else "0"
    return str(valor)


class TinyMachineSimulator:
    """
    Simulador de la máquina virtual Tiny Machine (TM).
    Lee un archivo o cadena '.tm', carga iMem y ejecuta el ciclo Fetch-Execute.
    """

    # Expresión regular para instrucciones RO:  12: ADD 0,1,0   * comentario
    REGEX_RO = re.compile(
        r"^\s*(\d+)\s*:\s*([A-Z]+)\s+(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)\s*(?:\*(.*))?$"
    )
    # Expresión regular para instrucciones RM:  15: LDC 0,3.1416(0)  * comentario
    REGEX_RM = re.compile(
        r"^\s*(\d+)\s*:\s*([A-Z]+)\s+(-?\d+)\s*,\s*(-?\d+(?:\.\d+)?)\s*\(\s*(-?\d+)\s*\)\s*(?:\*(.*))?$"
    )

    def __init__(self, max_steps=500000):
        self.max_steps = max_steps
        self.iMem = [None] * IADDR_SIZE
        self.dMem = [0] * DADDR_SIZE
        self.reg = [0] * NO_REGS
        self.reiniciar_maquina()

    def reiniciar_maquina(self):
        """Inicializa iMem, dMem y los 8 registros al estado de arranque estándar."""
        self.iMem = [
            InstruccionTM(loc, "HALT", 0, 0, 0, "memoria vacia")
            for loc in range(IADDR_SIZE)
        ]
        self.dMem = [0] * DADDR_SIZE
        # Convención oficial de Louden: dMem[0] almacena la dirección máxima DADDR_SIZE - 1
        self.dMem[0] = DADDR_SIZE - 1
        self.reg = [0] * NO_REGS

    # =========================================================================
    # CARGADOR DE ARCHIVOS .TM (Equivalente a readInstructions en tm.c)
    # =========================================================================

    def cargar_codigo_tm(self, contenido_tm: str):
        """
        Analiza el contenido de un archivo .tm línea por línea, ignorando
        comentarios que inician con '*' y cargando cada instrucción en iMem[loc].
        Retorna (True, num_instrucciones_cargadas) o (False, mensaje_error).
        """
        self.reiniciar_maquina()
        lineas = contenido_tm.splitlines()
        cargadas = 0

        for num_linea, linea_cruda in enumerate(lineas, start=1):
            linea = linea_cruda.strip()
            if not linea or linea.startswith("*"):
                continue

            # Intentar empatar con instrucción RO (r, s, t)
            m_ro = self.REGEX_RO.match(linea)
            if m_ro:
                loc = int(m_ro.group(1))
                op = m_ro.group(2).upper()
                r = int(m_ro.group(3))
                s = int(m_ro.group(4))
                t = int(m_ro.group(5))
                comentario = (m_ro.group(6) or "").strip()

                if op not in OPCODES_RO:
                    return False, f"Error en línea {num_linea} del archivo .tm: Opcode RO desconocido '{op}'"
                if not (0 <= loc < IADDR_SIZE):
                    return False, f"Error en línea {num_linea} del archivo .tm: Localidad iMem[{loc}] fuera de rango"

                self.iMem[loc] = InstruccionTM(loc, op, r, s, t, comentario)
                cargadas += 1
                continue

            # Intentar empatar con instrucción RM (r, d(s))
            m_rm = self.REGEX_RM.match(linea)
            if m_rm:
                loc = int(m_rm.group(1))
                op = m_rm.group(2).upper()
                r = int(m_rm.group(3))
                d_str = m_rm.group(4)
                d = float(d_str) if "." in d_str else int(d_str)
                s = int(m_rm.group(5))
                comentario = (m_rm.group(6) or "").strip()

                if op not in OPCODES_RM:
                    return False, f"Error en línea {num_linea} del archivo .tm: Opcode RM desconocido '{op}'"
                if not (0 <= loc < IADDR_SIZE):
                    return False, f"Error en línea {num_linea} del archivo .tm: Localidad iMem[{loc}] fuera de rango"

                self.iMem[loc] = InstruccionTM(loc, op, r, d, s, comentario)
                cargadas += 1
                continue

            return False, f"Error de formato en línea {num_linea} del archivo .tm: '{linea}'"

        return True, cargadas

    def cargar_archivo_tm(self, ruta_tm: str):
        """Lee un archivo .tm desde disco y carga sus instrucciones en iMem."""
        try:
            with open(ruta_tm, "r", encoding="utf-8") as f:
                contenido = f.read()
            return self.cargar_codigo_tm(contenido)
        except Exception as e:
            return False, f"No se pudo abrir el archivo .tm '{ruta_tm}': {e}"

    # =========================================================================
    # CICLO DE EJECUCIÓN FETCH-EXECUTE (Equivalente a stepTM / doCommand en tm.c)
    # =========================================================================

    def ejecutar(self, input_callback=None, output_callback=None):
        """
        Ejecuta el programa cargado en iMem comenzando desde pc = 0 hasta
        encontrar la instrucción HALT o un error de ejecución.

        Parámetros:
          - input_callback(etiqueta_variable) -> (valor_numerico, ok_bool):
            Función invocada cuando se ejecuta la instrucción 'IN'.
          - output_callback(texto_salida):
            Función invocada cada vez que se emite una línea en 'IN' o 'OUT'.

        Retorna un diccionario con:
          - 'exito': bool
          - 'estado': 'HALT' | 'CANCELADO' | 'ERROR'
          - 'pasos': int (instrucciones ejecutadas)
          - 'salidas': list[str] (valores impresos por OUT)
          - 'log': str (bitácora completa de ejecución)
        """
        pasos = 0
        salidas_out = []
        lineas_log = []

        def registrar_log(msg: str):
            lineas_log.append(msg)
            if output_callback:
                output_callback(msg)

        registrar_log("==========================================================")
        registrar_log("  SIMULADOR TINY MACHINE (TM) - EJECUCIÓN DE CÓDIGO .TM")
        registrar_log("==========================================================")

        while pasos < self.max_steps:
            pc_actual = int(self.reg[PC_REG])
            if not (0 <= pc_actual < IADDR_SIZE):
                msg_err = f"[ERROR TM] Dirección de instrucción fuera de límites: pc = {pc_actual}"
                registrar_log(msg_err)
                return {
                    "exito": False,
                    "estado": "ERROR",
                    "pasos": pasos,
                    "salidas": salidas_out,
                    "log": "\n".join(lineas_log)
                }

            inst = self.iMem[pc_actual]
            # Avanzar PC antes de ejecutar la instrucción (convención oficial de tm.c: reg[PC_REG]++)
            self.reg[PC_REG] = pc_actual + 1
            pasos += 1

            op = inst.iop
            r = inst.iarg1

            # -----------------------------------------------------------------
            # INSTRUCCIONES REGISTRO-ÚNICAMENTE (RO)
            # -----------------------------------------------------------------
            if inst.opclass == OPCLASS_RO:
                s = inst.iarg2
                t = inst.iarg3

                if op == "HALT":
                    registrar_log("----------------------------------------------------------")
                    registrar_log(f"HALT alcanzado en instrucción {pc_actual} ({pasos} pasos ejecutados).")
                    registrar_log("Estado final: Ejecución completada exitosamente.")
                    return {
                        "exito": True,
                        "estado": "HALT",
                        "pasos": pasos,
                        "salidas": salidas_out,
                        "log": "\n".join(lineas_log)
                    }

                elif op == "IN":
                    # Extraer el nombre de la variable desde el comentario si existe (ej. leer valor para 'radio')
                    nombre_var = "dato"
                    m_var = re.search(r"'([^']+)'", inst.comentario)
                    if m_var:
                        nombre_var = m_var.group(1)

                    if input_callback:
                        val_leido, ok = input_callback(nombre_var, inst.comentario)
                        if not ok:
                            registrar_log(f"\n[AVISO] Ejecución cancelada por el usuario al solicitar '{nombre_var}'.")
                            return {
                                "exito": False,
                                "estado": "CANCELADO",
                                "pasos": pasos,
                                "salidas": salidas_out,
                                "log": "\n".join(lineas_log)
                            }
                        self.reg[r] = val_leido
                    else:
                        # Modo consola estándar
                        raw = input(f"TM IN -> Ingrese valor para '{nombre_var}': ").strip()
                        self.reg[r] = float(raw) if "." in raw else int(raw)

                    registrar_log(f"IN  (lectura)   -> {nombre_var} = {formatear_numero_tm(self.reg[r])}")

                elif op == "OUT":
                    val_str = formatear_numero_tm(self.reg[r])
                    salidas_out.append(val_str)
                    registrar_log(f"OUT (resultado) => {val_str}")

                elif op == "ADD":
                    self.reg[r] = self.reg[s] + self.reg[t]

                elif op == "SUB":
                    self.reg[r] = self.reg[s] - self.reg[t]

                elif op == "MUL":
                    self.reg[r] = self.reg[s] * self.reg[t]

                elif op == "DIV":
                    divisor = self.reg[t]
                    if divisor == 0 or divisor == 0.0:
                        msg_err = f"[ERROR TM] División entre cero en instrucción {pc_actual}."
                        registrar_log(msg_err)
                        return {
                            "exito": False,
                            "estado": "ERROR",
                            "pasos": pasos,
                            "salidas": salidas_out,
                            "log": "\n".join(lineas_log)
                        }
                    dividendo = self.reg[s]
                    # Si ambos operandos son int, división entera truncada hacia cero (como en C)
                    if isinstance(dividendo, int) and isinstance(divisor, int):
                        self.reg[r] = int(dividendo / divisor)
                    else:
                        self.reg[r] = float(dividendo) / float(divisor)

            # -----------------------------------------------------------------
            # INSTRUCCIONES REGISTRO-MEMORIA (RM)
            # -----------------------------------------------------------------
            else:
                d = inst.iarg2
                s = inst.iarg3

                if op == "LDC":
                    self.reg[r] = d
                    continue

                # Para el resto de instrucciones RM, la dirección efectiva es m = d + reg[s]
                m = int(d) + int(self.reg[s])

                if op == "LDA":
                    self.reg[r] = m

                elif op == "LD":
                    if not (0 <= m < DADDR_SIZE):
                        msg_err = f"[ERROR TM] Violación de memoria de datos en LD (dMem[{m}]) en inst {pc_actual}."
                        registrar_log(msg_err)
                        return {
                            "exito": False,
                            "estado": "ERROR",
                            "pasos": pasos,
                            "salidas": salidas_out,
                            "log": "\n".join(lineas_log)
                        }
                    self.reg[r] = self.dMem[m]

                elif op == "ST":
                    if not (0 <= m < DADDR_SIZE):
                        msg_err = f"[ERROR TM] Violación de memoria de datos en ST (dMem[{m}]) en inst {pc_actual}."
                        registrar_log(msg_err)
                        return {
                            "exito": False,
                            "estado": "ERROR",
                            "pasos": pasos,
                            "salidas": salidas_out,
                            "log": "\n".join(lineas_log)
                        }
                    self.dMem[m] = self.reg[r]

                elif op == "JLT":
                    if self.reg[r] < 0:
                        self.reg[PC_REG] = m

                elif op == "JLE":
                    if self.reg[r] <= 0:
                        self.reg[PC_REG] = m

                elif op == "JGT":
                    if self.reg[r] > 0:
                        self.reg[PC_REG] = m

                elif op == "JGE":
                    if self.reg[r] >= 0:
                        self.reg[PC_REG] = m

                elif op == "JEQ":
                    if abs(self.reg[r]) < 1e-9:
                        self.reg[PC_REG] = m

                elif op == "JNE":
                    if abs(self.reg[r]) >= 1e-9:
                        self.reg[PC_REG] = m

        msg_timeout = (
            f"[ERROR TM] Límite de seguridad excedido ({self.max_steps} instrucciones). "
            "Posible ciclo infinito en el programa."
        )
        registrar_log(msg_timeout)
        return {
            "exito": False,
            "estado": "ERROR",
            "pasos": pasos,
            "salidas": salidas_out,
            "log": "\n".join(lineas_log)
        }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python tm_simulator.py <archivo.tm>")
        sys.exit(1)

    sim = TinyMachineSimulator()
    ok, info = sim.cargar_archivo_tm(sys.argv[1])
    if not ok:
        print(info)
        sys.exit(1)

    res = sim.ejecutar(output_callback=print)
