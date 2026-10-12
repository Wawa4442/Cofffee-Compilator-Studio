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
    """
    def __init__(self, nombre, tipo, linea, offset=0, ambito="main", tamano=4):
        self.nombre = nombre
        self.tipo = tipo
        self.lineas = [linea] if linea is not None else []
        self.offset = offset
        self.ambito = ambito
        self.tamano = tamano

    def agregar_linea(self, linea):
        """Registra una línea de aparición si aún no ha sido registrada."""
        if linea is not None and linea not in self.lineas:
            self.lineas.append(linea)

    def lineas_str(self):
        """Retorna las líneas de aparición como cadena formateada (ej. '2, 5, 11')."""
        return ", ".join(str(l) for l in sorted(self.lineas))

    def __repr__(self):
        return f"<Simbolo {self.nombre}:{self.tipo} offset={self.offset} lineas={self.lineas_str()}>"


class SymbolTable:
    """
    Tabla de Símbolos para el compilador.
    Soporta operaciones de inserción, búsqueda, registro de apariciones,
    detección de declaraciones duplicadas y cálculo de desplazamientos de memoria.
    """
    def __init__(self):
        self.simbolos = {}          # Diccionario {nombre: Simbolo}
        self.orden_insercion = []   # Lista con el orden de declaración
        self.offset_actual = 0      # Desplazamiento de memoria acumulado en bytes

    def insertar(self, nombre, tipo, linea, ambito="main", tamano=4):
        """
        Inserta un identificador en la tabla de símbolos.
        Retorna (True, Simbolo) si fue insertado exitosamente.
        Retorna (False, mensaje_error) si ya existía una declaración duplicada.
        """
        if nombre in self.simbolos:
            simbolo_existente = self.simbolos[nombre]
            return False, f"Declaración duplicada: el identificador '{nombre}' ya fue declarado previamente en la línea {simbolo_existente.lineas[0]}"

        # Normalizamos tipos equivalentes si aplica (ej. 'real' -> 'float')
        tipo_normalizado = "float" if tipo == "real" else tipo

        nuevo_simbolo = Simbolo(
            nombre=nombre,
            tipo=tipo_normalizado,
            linea=linea,
            offset=self.offset_actual,
            ambito=ambito,
            tamano=tamano
        )

        self.simbolos[nombre] = nuevo_simbolo
        self.orden_insercion.append(nombre)
        self.offset_actual += tamano
        return True, nuevo_simbolo

    def buscar(self, nombre):
        """Busca un símbolo por su nombre. Retorna el objeto Simbolo o None."""
        return self.simbolos.get(nombre, None)

    def contiene(self, nombre):
        """Verifica si un identificador ya está declarado."""
        return nombre in self.simbolos

    def registrar_uso(self, nombre, linea):
        """Registra una referencia/aparición de un identificador en una línea."""
        if nombre in self.simbolos:
            self.simbolos[nombre].agregar_linea(linea)
            return True
        return False

    def obtener_simbolos(self):
        """Retorna la lista de todos los símbolos registrados en orden de inserción."""
        return [self.simbolos[k] for k in self.orden_insercion]

    def limpiar(self):
        """Reinicia la tabla para un nuevo ciclo de compilación."""
        self.simbolos.clear()
        self.orden_insercion.clear()
        self.offset_actual = 0
