# -*- coding: utf-8 -*-
"""
===============================================================================
MÓDULO: code_tm.py (Equivalente a code.h y code.c de Kenneth C. Louden)
PROYECTO: Coffee Compiler Studio - Fase Final (Generación de Código TM)
===============================================================================
Descripción:
    Provee las utilidades de bajo nivel para emitir instrucciones objeto
    hacia la máquina virtual Tiny Machine (TM), así como el control de
    localidades de instrucción (emitLoc y highEmitLoc) para saltos hacia
    adelante (backpatching) y saltos hacia atrás.

Convención de Registros de la Tiny Machine (Louden):
    - ac  (0): Acumulador principal para evaluación de expresiones.
    - ac1 (1): Acumulador secundario para operandos binarios.
    - gp  (5): Global Pointer. Apunta a la base de la memoria de datos (dMem[0])
               donde se almacenan las variables globales según su offset en la
               Tabla de Símbolos.
    - mp  (6): Memory Pointer. Apunta al tope superior de la memoria de datos
               (dMem[DADDR_SIZE - 1]) y crece hacia abajo para almacenar
               resultados temporales de subexpresiones (tmpOffset).
    - pc  (7): Program Counter. Contiene la localidad de la instrucción en
               ejecución.

Adaptación Académica (Soporte Híbrido Entero / punto flotante en TM):
    En el diseño original de Louden para el lenguaje TINY, todas las variables
    son enteras. En nuestro lenguaje (Coffee Compiler Studio), la gramática y
    los casos de estudio oficiales incluyen tipos 'int', 'float'/'real' y 'bool'
    (por ejemplo: cálculo de áreas con PI=3.1416, temperaturas, descuentos del
    15% = 0.15, impuestos y promedios).
    Por ello, la instrucción RM 'LDC' (Load Constant) y las celdas de registro
    y memoria de la TM se extendieron de manera transparente para admitir tanto
    constantes enteras como reales en punto flotante, manteniendo intacto el
    repertorio de opcodes y el formato sintáctico estándar:
        <loc>: <OP> <r>,<d>(<s>)
===============================================================================
"""

# =============================================================================
# DEFINICIÓN DE REGISTROS DE LA TINY MACHINE
# =============================================================================
pc = 7   # Contador de programa (Program Counter)
mp = 6   # Puntero de memoria para temporales (Memory Pointer)
gp = 5   # Puntero global para variables de la Tabla de Símbolos (Global Pointer)
ac = 0   # Acumulador principal
ac1 = 1  # Segundo acumulador


class CodeEmitterTM:
    """
    Administrador de emisión de instrucciones para la Tiny Machine (.tm).
    Encapsula el estado de emitLoc y highEmitLoc (de code.c) para permitir
    múltiples compilaciones limpias dentro de la sesión del IDE sin residuos
    globales entre ejecuciones.
    """

    def __init__(self, trace_code=True):
        self.TraceCode = trace_code
        # Localidad de instrucción actual
        self.emitLoc = 0
        # Localidad de instrucción más alta emitida hasta el momento
        self.highEmitLoc = 0
        # Diccionario {loc: linea_instruccion} para presentar el archivo .tm ordenado
        self.instrucciones = {}
        # Comentarios asociados a la localidad actual {loc: [comentarios]}
        self.comentarios = {}
        # Flujo cronológico de emisión (exactamente como printf en code.c)
        self.flujo_lineas = []

    def limpiar(self):
        """Reinicia los contadores y buffers de código antes de una nueva compilación."""
        self.emitLoc = 0
        self.highEmitLoc = 0
        self.instrucciones.clear()
        self.comentarios.clear()
        self.flujo_lineas.clear()

    def emitComment(self, c: str):
        """
        Imprime una línea de comentario en el archivo de código objeto (.tm).
        Equivalente a: void emitComment(char * c) en code.c.
        """
        if self.TraceCode:
            linea = f"* {c}"
            self.comentarios.setdefault(self.emitLoc, []).append(linea)
            self.flujo_lineas.append(linea)

    def emitRO(self, op: str, r: int, s: int, t: int, c: str):
        """
        Emite una instrucción TM de tipo Registro-Únicamente (Register-Only).
        Formato: <emitLoc>:  <op>  <r>,<s>,<t>    * <comentario>
        Operadores RO: IN, OUT, ADD, SUB, MUL, DIV, HALT.
        """
        comentario = f"\t* {c}" if self.TraceCode and c else ""
        linea = f"{self.emitLoc:3d}:  {op:5s}  {r},{s},{t} {comentario}"
        self.instrucciones[self.emitLoc] = linea
        self.flujo_lineas.append(linea)
        self.emitLoc += 1
        if self.highEmitLoc < self.emitLoc:
            self.highEmitLoc = self.emitLoc

    def emitRM(self, op: str, r: int, d, s: int, c: str):
        """
        Emite una instrucción TM de tipo Registro-Memoria (Register-Memory).
        Formato: <emitLoc>:  <op>  <r>,<d>(<s>)    * <comentario>
        Operadores RM: LD, LDA, LDC, ST, JLT, JLE, JGT, JGE, JEQ, JNE.
        Nota: 'd' puede ser int o float (en el caso de LDC para constantes reales).
        """
        if isinstance(d, float):
            # Formatear flotante sin ceros residuales innecesarios pero conservando punto decimal
            d_str = f"{d:.6f}".rstrip("0")
            if d_str.endswith("."):
                d_str += "0"
        else:
            d_str = str(int(d))

        comentario = f"\t* {c}" if self.TraceCode and c else ""
        linea = f"{self.emitLoc:3d}:  {op:5s}  {r},{d_str}({s}) {comentario}"
        self.instrucciones[self.emitLoc] = linea
        self.flujo_lineas.append(linea)
        self.emitLoc += 1
        if self.highEmitLoc < self.emitLoc:
            self.highEmitLoc = self.emitLoc

    def emitSkip(self, howMany: int) -> int:
        """
        Salta 'howMany' localidades de código para ser parchadas posteriormente
        (backpatching) y devuelve la localidad actual antes del salto.
        Equivalente a: int emitSkip(int howMany) en code.c.
        """
        i = self.emitLoc
        self.emitLoc += howMany
        if self.highEmitLoc < self.emitLoc:
            self.highEmitLoc = self.emitLoc
        return i

    def emitBackup(self, loc: int):
        """
        Retrocede la localidad actual a una localidad previamente reservada con emitSkip.
        Equivalente a: void emitBackup(int loc) en code.c.
        """
        if loc > self.highEmitLoc:
            self.emitComment("BUG en emitBackup: localidad mayor que highEmitLoc")
        self.emitLoc = loc

    def emitRestore(self):
        """
        Restaura la localidad actual a la localidad más alta no emitida (highEmitLoc).
        Equivalente a: void emitRestore(void) en code.c.
        """
        self.emitLoc = self.highEmitLoc

    def emitRM_Abs(self, op: str, r: int, a: int, c: str):
        """
        Convierte una referencia absoluta 'a' a una referencia relativa al
        contador de programa (pc = 7) al emitir una instrucción RM de salto.
        Fórmula de Louden: d = a - (emitLoc + 1).
        Equivalente a: void emitRM_Abs(char *op, int r, int a, char *c) en code.c.
        """
        desplazamiento = a - (self.emitLoc + 1)
        comentario = f"\t* {c}" if self.TraceCode and c else ""
        linea = f"{self.emitLoc:3d}:  {op:5s}  {r},{desplazamiento}({pc}) {comentario}"
        self.instrucciones[self.emitLoc] = linea
        self.flujo_lineas.append(linea)
        self.emitLoc += 1
        if self.highEmitLoc < self.emitLoc:
            self.highEmitLoc = self.emitLoc

    def obtener_codigo_tm(self, ordenado_por_localidad=True) -> str:
        """
        Retorna el contenido completo del archivo .tm listo para guardarse en disco
        y ejecutarse en el simulador Tiny Machine.
        """
        if not ordenado_por_localidad:
            return "\n".join(self.flujo_lineas) + "\n"

        salida = []
        max_loc = self.highEmitLoc
        for loc in range(max_loc):
            if loc in self.comentarios:
                for com in self.comentarios[loc]:
                    salida.append(com)
            if loc in self.instrucciones:
                salida.append(self.instrucciones[loc])
        # Comentarios finales emitidos después de la última instrucción (ej. Fin de ejecución)
        if max_loc in self.comentarios:
            for com in self.comentarios[max_loc]:
                salida.append(com)
        return "\n".join(salida) + "\n"
