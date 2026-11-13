* Compilacion de Coffee Compiler Studio para Tiny Machine (.tm)
* Archivo objeto: C:/Users/hecto/Documents/Cofffe/Cofffee-Compilator-Studio/ejercicios_finales/G1_Ej2_Selectivo_PositivoNegativoNulo.tm
* Preludio estandar:
  0:  LD     6,0(0) 	* cargar mp con la direccion maxima desde localidad 0
  1:  ST     0,0(0) 	* limpiar localidad 0
* Fin del preludio estandar.
* Variable 'num' (int) asignada en dMem[gp+0] (offset 0 B)
* Variable 'resultado' (int) asignada en dMem[gp+1] (offset 4 B)
* -> cin (lectura)
  2:  IN     0,0,0 	* leer valor para 'num' (int)
  3:  ST     0,0(5) 	* cin: almacenar valor en 'num'
* <- cin
* -> if
* -> operador (>)
* -> identificador (num)
  4:  LD     0,0(5) 	* cargar valor de 'num'
* <- identificador
  5:  ST     0,0(6) 	* op: push operando izquierdo en temporal
* -> constante (0)
  6:  LDC    0,0(0) 	* cargar constante 0
* <- constante
  7:  LD     1,0(6) 	* op: cargar operando izquierdo en ac1
  8:  SUB    0,1,0 	* op > (comparar ac1 - ac)
  9:  JGT    0,2(7) 	* saltar a caso verdadero si >
 10:  LDC    0,0(0) 	* caso falso (ac = 0)
 11:  LDA    7,1(7) 	* saltar caso verdadero
 12:  LDC    0,1(0) 	* caso verdadero (ac = 1)
* <- operador (>)
 13:  JEQ    0,3(7) 	* if: jmp a else si condicion es falsa
* if: el salto hacia else/fin va aqui
* -> asignacion a 'resultado'
* -> constante (0)
 14:  LDC    0,0(0) 	* cargar constante 0
* <- constante
 15:  ST     0,1(5) 	* asignar: guardar valor en 'resultado'
* <- asignacion a 'resultado'
 16:  LDA    7,15(7) 	* if: jmp al final
* if: el salto hacia el final va aqui
* if: rama else
* -> if
* -> operador (<)
* -> identificador (num)
 17:  LD     0,0(5) 	* cargar valor de 'num'
* <- identificador
 18:  ST     0,0(6) 	* op: push operando izquierdo en temporal
* -> constante (0)
 19:  LDC    0,0(0) 	* cargar constante 0
* <- constante
 20:  LD     1,0(6) 	* op: cargar operando izquierdo en ac1
 21:  SUB    0,1,0 	* op < (comparar ac1 - ac)
 22:  JLT    0,2(7) 	* saltar a caso verdadero si <
 23:  LDC    0,0(0) 	* caso falso (ac = 0)
 24:  LDA    7,1(7) 	* saltar caso verdadero
 25:  LDC    0,1(0) 	* caso verdadero (ac = 1)
* <- operador (<)
 26:  JEQ    0,3(7) 	* if: jmp a else si condicion es falsa
* if: el salto hacia else/fin va aqui
* -> asignacion a 'resultado'
* -> constante (1)
 27:  LDC    0,1(0) 	* cargar constante 1
* <- constante
 28:  ST     0,1(5) 	* asignar: guardar valor en 'resultado'
* <- asignacion a 'resultado'
 29:  LDA    7,2(7) 	* if: jmp al final
* if: el salto hacia el final va aqui
* if: rama else
* -> asignacion a 'resultado'
* -> constante (2)
 30:  LDC    0,2(0) 	* cargar constante 2
* <- constante
 31:  ST     0,1(5) 	* asignar: guardar valor en 'resultado'
* <- asignacion a 'resultado'
* <- if
* <- if
* -> cout (escritura)
* -> identificador (resultado)
 32:  LD     0,1(5) 	* cargar valor de 'resultado'
* <- identificador
 33:  OUT    0,0,0 	* cout: escribir valor de ac
* <- cout
* Fin de la ejecucion.
 34:  HALT   0,0,0 
