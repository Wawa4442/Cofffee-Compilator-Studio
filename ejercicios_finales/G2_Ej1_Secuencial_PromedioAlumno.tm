* Compilacion de Coffee Compiler Studio para Tiny Machine (.tm)
* Archivo objeto: C:\Users\hecto\Documents\Cofffe\Cofffee-Compilator-Studio\ejercicios_finales\G2_Ej1_Secuencial_PromedioAlumno.tm
* Preludio estandar:
  0:  LD     6,0(0) 	* cargar mp con la direccion maxima desde localidad 0
  1:  ST     0,0(0) 	* limpiar localidad 0
* Fin del preludio estandar.
* Variable 'matricula' (int) asignada en dMem[gp+0] (offset 0 B)
* Variable 'cal1' (float) asignada en dMem[gp+1] (offset 4 B)
* Variable 'cal2' (float) asignada en dMem[gp+2] (offset 8 B)
* Variable 'cal3' (float) asignada en dMem[gp+3] (offset 12 B)
* Variable 'cal4' (float) asignada en dMem[gp+4] (offset 16 B)
* Variable 'cal5' (float) asignada en dMem[gp+5] (offset 20 B)
* Variable 'promedio' (float) asignada en dMem[gp+6] (offset 24 B)
* -> cin (lectura)
  2:  IN     0,0,0 	* leer valor para 'matricula' (int)
  3:  ST     0,0(5) 	* cin: almacenar valor en 'matricula'
* <- cin
* -> cin (lectura)
  4:  IN     0,0,0 	* leer valor para 'cal1' (float)
  5:  LDC    1,0.0(0) 	* constante 0.0 para promover a float
  6:  ADD    0,0,1 	* convertir 'cal1' a float
  7:  ST     0,1(5) 	* cin: almacenar valor en 'cal1'
* <- cin
* -> cin (lectura)
  8:  IN     0,0,0 	* leer valor para 'cal2' (float)
  9:  LDC    1,0.0(0) 	* constante 0.0 para promover a float
 10:  ADD    0,0,1 	* convertir 'cal2' a float
 11:  ST     0,2(5) 	* cin: almacenar valor en 'cal2'
* <- cin
* -> cin (lectura)
 12:  IN     0,0,0 	* leer valor para 'cal3' (float)
 13:  LDC    1,0.0(0) 	* constante 0.0 para promover a float
 14:  ADD    0,0,1 	* convertir 'cal3' a float
 15:  ST     0,3(5) 	* cin: almacenar valor en 'cal3'
* <- cin
* -> cin (lectura)
 16:  IN     0,0,0 	* leer valor para 'cal4' (float)
 17:  LDC    1,0.0(0) 	* constante 0.0 para promover a float
 18:  ADD    0,0,1 	* convertir 'cal4' a float
 19:  ST     0,4(5) 	* cin: almacenar valor en 'cal4'
* <- cin
* -> cin (lectura)
 20:  IN     0,0,0 	* leer valor para 'cal5' (float)
 21:  LDC    1,0.0(0) 	* constante 0.0 para promover a float
 22:  ADD    0,0,1 	* convertir 'cal5' a float
 23:  ST     0,5(5) 	* cin: almacenar valor en 'cal5'
* <- cin
* -> asignacion a 'promedio'
* -> operador (/)
* -> operador (+)
* -> operador (+)
* -> operador (+)
* -> operador (+)
* -> identificador (cal1)
 24:  LD     0,1(5) 	* cargar valor de 'cal1'
* <- identificador
 25:  ST     0,0(6) 	* op: push operando izquierdo en temporal
* -> identificador (cal2)
 26:  LD     0,2(5) 	* cargar valor de 'cal2'
* <- identificador
 27:  LD     1,0(6) 	* op: cargar operando izquierdo en ac1
 28:  ADD    0,1,0 	* op +
* <- operador (+)
 29:  ST     0,0(6) 	* op: push operando izquierdo en temporal
* -> identificador (cal3)
 30:  LD     0,3(5) 	* cargar valor de 'cal3'
* <- identificador
 31:  LD     1,0(6) 	* op: cargar operando izquierdo en ac1
 32:  ADD    0,1,0 	* op +
* <- operador (+)
 33:  ST     0,0(6) 	* op: push operando izquierdo en temporal
* -> identificador (cal4)
 34:  LD     0,4(5) 	* cargar valor de 'cal4'
* <- identificador
 35:  LD     1,0(6) 	* op: cargar operando izquierdo en ac1
 36:  ADD    0,1,0 	* op +
* <- operador (+)
 37:  ST     0,0(6) 	* op: push operando izquierdo en temporal
* -> identificador (cal5)
 38:  LD     0,5(5) 	* cargar valor de 'cal5'
* <- identificador
 39:  LD     1,0(6) 	* op: cargar operando izquierdo en ac1
 40:  ADD    0,1,0 	* op +
* <- operador (+)
 41:  ST     0,0(6) 	* op: push operando izquierdo en temporal
* -> constante (5.0)
 42:  LDC    0,5.0(0) 	* cargar constante 5.0
* <- constante
 43:  LD     1,0(6) 	* op: cargar operando izquierdo en ac1
 44:  ST     0,0(6) 	* div: resguardar divisor
 45:  LDC    0,0.0(0) 	* div: constante 0.0
 46:  ADD    1,1,0 	* div: asegurar dividendo float
 47:  LD     0,0(6) 	* div: restaurar divisor
 48:  DIV    0,1,0 	* op /
* <- operador (/)
 49:  LDC    1,0.0(0) 	* asegurar representacion float
 50:  ADD    0,0,1 	* promover resultado a float para 'promedio'
 51:  ST     0,6(5) 	* asignar: guardar valor en 'promedio'
* <- asignacion a 'promedio'
* -> cout (escritura)
* -> identificador (matricula)
 52:  LD     0,0(5) 	* cargar valor de 'matricula'
* <- identificador
 53:  OUT    0,0,0 	* cout: escribir valor de ac
* <- cout
* -> cout (escritura)
* -> identificador (promedio)
 54:  LD     0,6(5) 	* cargar valor de 'promedio'
* <- identificador
 55:  OUT    0,0,0 	* cout: escribir valor de ac
* <- cout
* Fin de la ejecucion.
 56:  HALT   0,0,0 
