/****************************************************/
/* Archivo: code.h                                  */
/* Utilidades de emision de codigo para la          */
/* Tiny Machine (TM) - Coffee Compiler Studio       */
/* Basado en Kenneth C. Louden                      */
/****************************************************/

#ifndef _CODE_H_
#define _CODE_H_

/* pc = program counter (contador de programa) */
#define pc 7

/* mp = "memory pointer" apunta al tope de la memoria (para almacenamiento temporal) */
#define mp 6

/* gp = "global pointer" apunta al fondo de la memoria para almacenamiento de variables globales */
#define gp 5

/* acumulador */
#define ac 0

/* 2do acumulador */
#define ac1 1

/* Utilidades de emision de codigo */

/* Imprime una linea de comentario con el comentario c en el archivo de codigo */
void emitComment( const char * c );

/* Emite una instruccion TM de solo-registro (RO)
 * op = el codigo de operacion
 * r = registro objetivo
 * s = 1er registro fuente
 * t = 2do registro fuente
 * c = comentario a ser impreso si TraceCode es TRUE
 */
void emitRO( const char *op, int r, int s, int t, const char *c );

/* Emite una instruccion TM de registro-a-memoria (RM)
 * op = el codigo de operacion
 * r = registro objetivo
 * d = desplazamiento numerico (soporta constantes enteras y flotantes en LDC)
 * s = registro base
 * c = comentario a ser impreso si TraceCode es TRUE
 */
void emitRM( const char * op, int r, double d, int s, const char *c );

/* Salta "howMany" localidades de codigo para posterior backpatch.
 * Tambien devuelve la localidad de codigo actual.
 */
int emitSkip( int howMany );

/* Retrocede a loc = una localidad previamente saltada */
void emitBackup( int loc );

/* Restaura la localidad de codigo actual a la localidad mas alta no emitida */
void emitRestore( void );

/* Convierte una referencia absoluta a una referencia relativa al pc
 * al emitir una instruccion TM de registro-a-memoria
 * op = el codigo de operacion
 * r = registro objetivo
 * a = la localidad absoluta en memoria
 * c = comentario a ser impreso si TraceCode es TRUE
 */
void emitRM_Abs( const char *op, int r, int a, const char * c );

#endif
