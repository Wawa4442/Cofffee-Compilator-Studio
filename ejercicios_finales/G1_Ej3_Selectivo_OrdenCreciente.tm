* Compilacion de Coffee Compiler Studio para Tiny Machine (.tm)
* Archivo objeto: C:/Users/hecto/Documents/Cofffe/Cofffee-Compilator-Studio/ejercicios_finales/G1_Ej3_Selectivo_OrdenCreciente.tm
* Preludio estandar:
  0:  LD     6,0(0) 	* cargar mp con la direccion maxima desde localidad 0
  1:  ST     0,0(0) 	* limpiar localidad 0
* Fin del preludio estandar.
* Variable 'a' (int) asignada en dMem[gp+0] (offset 0 B)
* Variable 'b' (int) asignada en dMem[gp+1] (offset 4 B)
* Variable 'c' (int) asignada en dMem[gp+2] (offset 8 B)
* Variable 'creciente' (int) asignada en dMem[gp+3] (offset 12 B)
* -> cin (lectura)
  2:  IN     0,0,0 	* leer valor para 'a' (int)
  3:  ST     0,0(5) 	* cin: almacenar valor en 'a'
* <- cin
* -> cin (lectura)
  4:  IN     0,0,0 	* leer valor para 'b' (int)
  5:  ST     0,1(5) 	* cin: almacenar valor en 'b'
* <- cin
* -> cin (lectura)
  6:  IN     0,0,0 	* leer valor para 'c' (int)
  7:  ST     0,2(5) 	* cin: almacenar valor en 'c'
* <- cin
* -> if
* -> operador (&&)
* -> operador (<)
* -> identificador (a)
  8:  LD     0,0(5) 	* cargar valor de 'a'
* <- identificador
  9:  ST     0,0(6) 	* op: push operando izquierdo en temporal
* -> identificador (b)
 10:  LD     0,1(5) 	* cargar valor de 'b'
* <- identificador
 11:  LD     1,0(6) 	* op: cargar operando izquierdo en ac1
 12:  SUB    0,1,0 	* op < (comparar ac1 - ac)
 13:  JLT    0,2(7) 	* saltar a caso verdadero si <
 14:  LDC    0,0(0) 	* caso falso (ac = 0)
 15:  LDA    7,1(7) 	* saltar caso verdadero
 16:  LDC    0,1(0) 	* caso verdadero (ac = 1)
* <- operador (<)
 17:  ST     0,0(6) 	* op: push operando izquierdo en temporal
* -> operador (<)
* -> identificador (b)
 18:  LD     0,1(5) 	* cargar valor de 'b'
* <- identificador
 19:  ST     0,-1(6) 	* op: push operando izquierdo en temporal
* -> identificador (c)
 20:  LD     0,2(5) 	* cargar valor de 'c'
* <- identificador
 21:  LD     1,-1(6) 	* op: cargar operando izquierdo en ac1
 22:  SUB    0,1,0 	* op < (comparar ac1 - ac)
 23:  JLT    0,2(7) 	* saltar a caso verdadero si <
 24:  LDC    0,0(0) 	* caso falso (ac = 0)
 25:  LDA    7,1(7) 	* saltar caso verdadero
 26:  LDC    0,1(0) 	* caso verdadero (ac = 1)
* <- operador (<)
 27:  LD     1,0(6) 	* op: cargar operando izquierdo en ac1
 28:  JEQ    1,3(7) 	* AND: si izq es falso (0), saltar a falso
 29:  JEQ    0,2(7) 	* AND: si der es falso (0), saltar a falso
 30:  LDC    0,1(0) 	* AND: ambos verdaderos (ac = 1)
 31:  LDA    7,1(7) 	* AND: saltar caso falso
 32:  LDC    0,0(0) 	* AND: caso falso (ac = 0)
* <- operador (&&)
 33:  JEQ    0,3(7) 	* if: jmp a else si condicion es falsa
* if: el salto hacia else/fin va aqui
* -> asignacion a 'creciente'
* -> constante (1)
 34:  LDC    0,1(0) 	* cargar constante 1
* <- constante
 35:  ST     0,3(5) 	* asignar: guardar valor en 'creciente'
* <- asignacion a 'creciente'
 36:  LDA    7,2(7) 	* if: jmp al final
* if: el salto hacia el final va aqui
* if: rama else
* -> asignacion a 'creciente'
* -> constante (0)
 37:  LDC    0,0(0) 	* cargar constante 0
* <- constante
 38:  ST     0,3(5) 	* asignar: guardar valor en 'creciente'
* <- asignacion a 'creciente'
* <- if
* -> cout (escritura)
* -> identificador (creciente)
 39:  LD     0,3(5) 	* cargar valor de 'creciente'
* <- identificador
 40:  OUT    0,0,0 	* cout: escribir valor de ac
* <- cout
* Fin de la ejecucion.
 41:  HALT   0,0,0 
