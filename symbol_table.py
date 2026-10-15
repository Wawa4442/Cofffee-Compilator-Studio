# -*- coding: utf-8 -*-

class Simbolo:
    """
    Representa una entrada en la Tabla de Símbolos.
    Almacena:
      - nombre: lexema del identificador.
      - tipo: tipo de dato ("int", "float", "bool", etc.).
      - lineas: lista de líneas donde aparece el identificador (declaración y usos).
      - offset: desplazamiento de memoria acumulado (en bytes).
      - ambito: ámbito o scope ("main" o contexto local).
      - tamano: tamaño del tipo de dato en memoria (en bytes).
      - es_duplicado: bandera booleana indicando si es una redeclaración inválida.
      - estado: estado de validez ("VÁLIDO", "ERROR: DUPLICADO...", etc.).
      - mensaje_error: mensaje explicativo si se trata de un error semántico.
    """
    def __init__(self, nombre, tipo, linea, offset=0, ambito="main", tamano=4,
                 es_duplicado=False, estado="VÁLIDO", mensaje_error=None):
        self.nombre = nombre
        self.tipo = tipo
        self.lineas = [linea] if linea is not None else []
        self.offset = offset
        self.ambito = ambito
        self.tamano = tamano
        self.es_duplicado = es_duplicado
        self.estado = estado
        self.mensaje_error = mensaje_error

    def agregar_linea(self, linea):
        """Registra cada ocurrencia o aparición del identificador en una línea."""
        if linea is not None:
            self.lineas.append(linea)

    def lineas_str(self):
        """Retorna las líneas de aparición como cadena formateada (ej. '2, 5, 11')."""
        return ", ".join(str(l) for l in sorted(self.lineas))

    def offset_str(self):
        """Retorna el desplazamiento en formato legible para la tabla (ej. '0 B' o '-')."""
        if self.es_duplicado or self.offset is None:
            return "-"
        return f"{self.offset} B"

    def tipo_display(self):
        """Retorna el tipo formateado, evidenciando si es duplicado."""
        if self.es_duplicado:
            return f"{self.tipo} [DUPLICADO]"
        return self.tipo

    def __repr__(self):
        info_dup = f" [{self.estado}]" if self.es_duplicado else ""
        return f"<Simbolo {self.nombre}:{self.tipo} offset={self.offset_str()} lineas={self.lineas_str()}{info_dup}>"


class SymbolTable:
    """
    Tabla de Símbolos para el compilador.
    Soporta operaciones de inserción, búsqueda, registro de apariciones,
    detección de declaraciones duplicadas y cálculo de desplazamientos de memoria.
    """
    def __init__(self):
        self.simbolos = {}          # Diccionario {nombre: Simbolo_valido} para consultas de tipos
        self.orden_insercion = []   # Lista con el orden de declaración válida
        self.entradas = []          # Lista completa de todas las entradas (válidas y duplicadas)
        self.offset_actual = 0      # Desplazamiento de memoria acumulado en bytes

    def insertar(self, nombre, tipo, linea, columna=None, ambito="main", tamano=4):
        """
        Inserta un identificador en la tabla de símbolos.
        - Si es la primera declaración: lo registra como VÁLIDO y asigna memoria (offset).
        - Si es un intento duplicado: registra la ocurrencia errónea en `self.entradas`
          para evidencia visual y auditoría, pero NO sobreescribe el símbolo original
          ni asigna memoria adicional, preservando la coherencia semántica subsiguiente.
        Retorna:
          (True, Simbolo) si fue insertado exitosamente.
          (False, mensaje_error) si ya existía una declaración duplicada.
        """
        tipo_normalizado = "float" if tipo == "real" else tipo

        if nombre in self.simbolos:
            simbolo_existente = self.simbolos[nombre]
            linea_orig = simbolo_existente.lineas[0] if simbolo_existente.lineas else "N/A"
            msg_error = f"Declaración duplicada: el identificador '{nombre}' ya fue declarado previamente en la línea {linea_orig}"

            simbolo_dup = Simbolo(
                nombre=nombre,
                tipo=tipo_normalizado,
                linea=linea,
                offset=None,
                ambito=ambito,
                tamano=tamano,
                es_duplicado=True,
                estado=f"ERROR: DUPLICADO (Declarado en línea {linea_orig})",
                mensaje_error=msg_error
            )
            self.entradas.append(simbolo_dup)
            return False, msg_error

        nuevo_simbolo = Simbolo(
            nombre=nombre,
            tipo=tipo_normalizado,
            linea=linea,
            offset=self.offset_actual,
            ambito=ambito,
            tamano=tamano,
            es_duplicado=False,
            estado="VÁLIDO"
        )

        self.simbolos[nombre] = nuevo_simbolo
        self.orden_insercion.append(nombre)
        self.entradas.append(nuevo_simbolo)
        self.offset_actual += tamano
        return True, nuevo_simbolo

    def buscar(self, nombre):
        """Busca un símbolo por su nombre. Retorna el objeto Simbolo válido o None."""
        return self.simbolos.get(nombre, None)

    def contiene(self, nombre):
        """Verifica si un identificador ya está declarado válidamente."""
        return nombre in self.simbolos

    def registrar_uso(self, nombre, linea):
        """Registra una referencia/aparición de un identificador en una línea sobre el símbolo válido."""
        if nombre in self.simbolos:
            self.simbolos[nombre].agregar_linea(linea)
            return True
        return False

    def obtener_simbolos(self):
        """Retorna la lista de todas las entradas registradas (incluyendo duplicados) para visualización."""
        return list(self.entradas)

    def obtener_simbolos_validos(self):
        """Retorna únicamente los símbolos válidos (no duplicados)."""
        return [s for s in self.entradas if not s.es_duplicado]

    def obtener_duplicados(self):
        """Retorna únicamente los registros de declaraciones duplicadas."""
        return [s for s in self.entradas if s.es_duplicado]

    def limpiar(self):
        """Reinicia la tabla para un nuevo ciclo de compilación."""
        self.simbolos.clear()
        self.orden_insercion.clear()
        self.entradas.clear()
        self.offset_actual = 0
