* Compilacion de Coffee Compiler Studio para Tiny Machine (.tm)
* Archivo objeto: C:\Users\hecto\Documents\Cofffe\Cofffee-Compilator-Studio\programa_actual.tm
* Preludio estandar:
  0:  LD     6,0(0) 	* cargar mp con la direccion maxima desde localidad 0
  1:  ST     0,0(0) 	* limpiar localidad 0
* Fin del preludio estandar.
* Variable 'x' (int) asignada en dMem[gp+0] (offset 0 B)
* Variable 'y' (int) asignada en dMem[gp+1] (offset 4 B)
* -> asignacion a 'x'
* -> constante (10)
  2:  LDC    0,10(0) 	* cargar constante 10
* <- constante
  3:  ST     0,0(5) 	* asignar: guardar valor en 'x'
* <- asignacion a 'x'
* -> asignacion a 'y'
* -> constante (20)
  4:  LDC    0,20(0) 	* cargar constante 20
* <- constante
  5:  ST     0,1(5) 	* asignar: guardar valor en 'y'
* <- asignacion a 'y'
* -> cout (escritura)
* -> operador (+)
* -> identificador (x)
  6:  LD     0,0(5) 	* cargar valor de 'x'
* <- identificador
  7:  ST     0,0(6) 	* op: push operando izquierdo en temporal
* -> identificador (y)
  8:  LD     0,1(5) 	* cargar valor de 'y'
* <- identificador
  9:  LD     1,0(6) 	* op: cargar operando izquierdo en ac1
 10:  ADD    0,1,0 	* op +
* <- operador (+)
 11:  OUT    0,0,0 	* cout: escribir valor de ac
* <- cout
* Fin de la ejecucion.
 12:  HALT   0,0,0 
