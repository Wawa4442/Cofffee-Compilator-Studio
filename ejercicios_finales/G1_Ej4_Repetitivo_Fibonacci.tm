* Compilacion de Coffee Compiler Studio para Tiny Machine (.tm)
* Archivo objeto: C:/Users/hecto/Documents/Cofffe/Cofffee-Compilator-Studio/ejercicios_finales/G1_Ej4_Repetitivo_Fibonacci.tm
* Preludio estandar:
  0:  LD     6,0(0) 	* cargar mp con la direccion maxima desde localidad 0
  1:  ST     0,0(0) 	* limpiar localidad 0
* Fin del preludio estandar.
* Variable 'n' (int) asignada en dMem[gp+0] (offset 0 B)
* Variable 'i' (int) asignada en dMem[gp+1] (offset 4 B)
* Variable 'a' (int) asignada en dMem[gp+2] (offset 8 B)
* Variable 'b' (int) asignada en dMem[gp+3] (offset 12 B)
* Variable 'siguiente' (int) asignada en dMem[gp+4] (offset 16 B)
* Variable 'resultado' (int) asignada en dMem[gp+5] (offset 20 B)
* -> cin (lectura)
  2:  IN     0,0,0 	* leer valor para 'n' (int)
  3:  ST     0,0(5) 	* cin: almacenar valor en 'n'
* <- cin
* -> if
* -> operador (<=)
* -> identificador (n)
  4:  LD     0,0(5) 	* cargar valor de 'n'
* <- identificador
  5:  ST     0,0(6) 	* op: push operando izquierdo en temporal
* -> constante (1)
  6:  LDC    0,1(0) 	* cargar constante 1
* <- constante
  7:  LD     1,0(6) 	* op: cargar operando izquierdo en ac1
  8:  SUB    0,1,0 	* op <= (comparar ac1 - ac)
  9:  JLE    0,2(7) 	* saltar a caso verdadero si <=
 10:  LDC    0,0(0) 	* caso falso (ac = 0)
 11:  LDA    7,1(7) 	* saltar caso verdadero
 12:  LDC    0,1(0) 	* caso verdadero (ac = 1)
* <- operador (<=)
 13:  JEQ    0,3(7) 	* if: jmp a else si condicion es falsa
* if: el salto hacia else/fin va aqui
* -> asignacion a 'resultado'
* -> constante (0)
 14:  LDC    0,0(0) 	* cargar constante 0
* <- constante
 15:  ST     0,5(5) 	* asignar: guardar valor en 'resultado'
* <- asignacion a 'resultado'
 16:  LDA    7,46(7) 	* if: jmp al final
* if: el salto hacia el final va aqui
* if: rama else
* -> if
* -> operador (==)
* -> identificador (n)
 17:  LD     0,0(5) 	* cargar valor de 'n'
* <- identificador
 18:  ST     0,0(6) 	* op: push operando izquierdo en temporal
* -> constante (2)
 19:  LDC    0,2(0) 	* cargar constante 2
* <- constante
 20:  LD     1,0(6) 	* op: cargar operando izquierdo en ac1
 21:  SUB    0,1,0 	* op == (comparar ac1 - ac)
 22:  JEQ    0,2(7) 	* saltar a caso verdadero si ==
 23:  LDC    0,0(0) 	* caso falso (ac = 0)
 24:  LDA    7,1(7) 	* saltar caso verdadero
 25:  LDC    0,1(0) 	* caso verdadero (ac = 1)
* <- operador (==)
 26:  JEQ    0,3(7) 	* if: jmp a else si condicion es falsa
* if: el salto hacia else/fin va aqui
* -> asignacion a 'resultado'
* -> constante (1)
 27:  LDC    0,1(0) 	* cargar constante 1
* <- constante
 28:  ST     0,5(5) 	* asignar: guardar valor en 'resultado'
* <- asignacion a 'resultado'
 29:  LDA    7,33(7) 	* if: jmp al final
* if: el salto hacia el final va aqui
* if: rama else
* -> asignacion a 'a'
* -> constante (0)
 30:  LDC    0,0(0) 	* cargar constante 0
* <- constante
 31:  ST     0,2(5) 	* asignar: guardar valor en 'a'
* <- asignacion a 'a'
* -> asignacion a 'b'
* -> constante (1)
 32:  LDC    0,1(0) 	* cargar constante 1
* <- constante
 33:  ST     0,3(5) 	* asignar: guardar valor en 'b'
* <- asignacion a 'b'
* -> asignacion a 'i'
* -> constante (3)
 34:  LDC    0,3(0) 	* cargar constante 3
* <- constante
 35:  ST     0,1(5) 	* asignar: guardar valor en 'i'
* <- asignacion a 'i'
* -> while
* while: evaluar condicion
* -> operador (<=)
* -> identificador (i)
 36:  LD     0,1(5) 	* cargar valor de 'i'
* <- identificador
 37:  ST     0,0(6) 	* op: push operando izquierdo en temporal
* -> identificador (n)
 38:  LD     0,0(5) 	* cargar valor de 'n'
* <- identificador
 39:  LD     1,0(6) 	* op: cargar operando izquierdo en ac1
 40:  SUB    0,1,0 	* op <= (comparar ac1 - ac)
 41:  JLE    0,2(7) 	* saltar a caso verdadero si <=
 42:  LDC    0,0(0) 	* caso falso (ac = 0)
 43:  LDA    7,1(7) 	* saltar caso verdadero
 44:  LDC    0,1(0) 	* caso verdadero (ac = 1)
* <- operador (<=)
 45:  JEQ    0,15(7) 	* while: salir del ciclo si condicion es falsa
* while: salto hacia el final si es falso
* -> asignacion a 'siguiente'
* -> operador (+)
* -> identificador (a)
 46:  LD     0,2(5) 	* cargar valor de 'a'
* <- identificador
 47:  ST     0,0(6) 	* op: push operando izquierdo en temporal
* -> identificador (b)
 48:  LD     0,3(5) 	* cargar valor de 'b'
* <- identificador
 49:  LD     1,0(6) 	* op: cargar operando izquierdo en ac1
 50:  ADD    0,1,0 	* op +
* <- operador (+)
 51:  ST     0,4(5) 	* asignar: guardar valor en 'siguiente'
* <- asignacion a 'siguiente'
* -> asignacion a 'a'
* -> identificador (b)
 52:  LD     0,3(5) 	* cargar valor de 'b'
* <- identificador
 53:  ST     0,2(5) 	* asignar: guardar valor en 'a'
* <- asignacion a 'a'
* -> asignacion a 'b'
* -> identificador (siguiente)
 54:  LD     0,4(5) 	* cargar valor de 'siguiente'
* <- identificador
 55:  ST     0,3(5) 	* asignar: guardar valor en 'b'
* <- asignacion a 'b'
* -> operador unario i++
 56:  LD     0,1(5) 	* cargar 'i'
 57:  LDC    1,1(0) 	* cargar constante 1
 58:  ADD    0,0,1 	* incrementar 'i'
 59:  ST     0,1(5) 	* guardar nuevo valor en 'i'
* <- operador unario i++
 60:  LDA    7,-25(7) 	* while: regresar al inicio del ciclo
* <- while
* -> asignacion a 'resultado'
* -> identificador (b)
 61:  LD     0,3(5) 	* cargar valor de 'b'
* <- identificador
 62:  ST     0,5(5) 	* asignar: guardar valor en 'resultado'
* <- asignacion a 'resultado'
* <- if
* <- if
* -> cout (escritura)
* -> identificador (resultado)
 63:  LD     0,5(5) 	* cargar valor de 'resultado'
* <- identificador
 64:  OUT    0,0,0 	* cout: escribir valor de ac
* <- cout
* Fin de la ejecucion.
 65:  HALT   0,0,0 
