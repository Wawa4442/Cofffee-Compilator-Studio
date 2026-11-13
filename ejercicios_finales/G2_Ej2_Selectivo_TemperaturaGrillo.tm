* Compilacion de Coffee Compiler Studio para Tiny Machine (.tm)
* Archivo objeto: C:\Users\hecto\Documents\Cofffe\Cofffee-Compilator-Studio\ejercicios_finales\G2_Ej2_Selectivo_TemperaturaGrillo.tm
* Preludio estandar:
  0:  LD     6,0(0) 	* cargar mp con la direccion maxima desde localidad 0
  1:  ST     0,0(0) 	* limpiar localidad 0
* Fin del preludio estandar.
* Variable 'h' (float) asignada en dMem[gp+0] (offset 0 B)
* Variable 'temperatura' (float) asignada en dMem[gp+1] (offset 4 B)
* -> cin (lectura)
  2:  IN     0,0,0 	* leer valor para 'h' (float)
  3:  LDC    1,0.0(0) 	* constante 0.0 para promover a float
  4:  ADD    0,0,1 	* convertir 'h' a float
  5:  ST     0,0(5) 	* cin: almacenar valor en 'h'
* <- cin
* -> if
* -> operador (>)
* -> identificador (h)
  6:  LD     0,0(5) 	* cargar valor de 'h'
* <- identificador
  7:  ST     0,0(6) 	* op: push operando izquierdo en temporal
* -> constante (0.0)
  8:  LDC    0,0.0(0) 	* cargar constante 0.0
* <- constante
  9:  LD     1,0(6) 	* op: cargar operando izquierdo en ac1
 10:  SUB    0,1,0 	* op > (comparar ac1 - ac)
 11:  JGT    0,2(7) 	* saltar a caso verdadero si >
 12:  LDC    0,0(0) 	* caso falso (ac = 0)
 13:  LDA    7,1(7) 	* saltar caso verdadero
 14:  LDC    0,1(0) 	* caso verdadero (ac = 1)
* <- operador (>)
 15:  JEQ    0,17(7) 	* if: jmp a else si condicion es falsa
* if: el salto hacia else/fin va aqui
* -> asignacion a 'temperatura'
* -> operador (+)
* -> operador (/)
* -> identificador (h)
 16:  LD     0,0(5) 	* cargar valor de 'h'
* <- identificador
 17:  ST     0,0(6) 	* op: push operando izquierdo en temporal
* -> constante (4.0)
 18:  LDC    0,4.0(0) 	* cargar constante 4.0
* <- constante
 19:  LD     1,0(6) 	* op: cargar operando izquierdo en ac1
 20:  ST     0,0(6) 	* div: resguardar divisor
 21:  LDC    0,0.0(0) 	* div: constante 0.0
 22:  ADD    1,1,0 	* div: asegurar dividendo float
 23:  LD     0,0(6) 	* div: restaurar divisor
 24:  DIV    0,1,0 	* op /
* <- operador (/)
 25:  ST     0,0(6) 	* op: push operando izquierdo en temporal
* -> constante (40.0)
 26:  LDC    0,40.0(0) 	* cargar constante 40.0
* <- constante
 27:  LD     1,0(6) 	* op: cargar operando izquierdo en ac1
 28:  ADD    0,1,0 	* op +
* <- operador (+)
 29:  LDC    1,0.0(0) 	* asegurar representacion float
 30:  ADD    0,0,1 	* promover resultado a float para 'temperatura'
 31:  ST     0,1(5) 	* asignar: guardar valor en 'temperatura'
* <- asignacion a 'temperatura'
 32:  LDA    7,4(7) 	* if: jmp al final
* if: el salto hacia el final va aqui
* if: rama else
* -> asignacion a 'temperatura'
* -> constante (0.0)
 33:  LDC    0,0.0(0) 	* cargar constante 0.0
* <- constante
 34:  LDC    1,0.0(0) 	* asegurar representacion float
 35:  ADD    0,0,1 	* promover resultado a float para 'temperatura'
 36:  ST     0,1(5) 	* asignar: guardar valor en 'temperatura'
* <- asignacion a 'temperatura'
* <- if
* -> cout (escritura)
* -> identificador (temperatura)
 37:  LD     0,1(5) 	* cargar valor de 'temperatura'
* <- identificador
 38:  OUT    0,0,0 	* cout: escribir valor de ac
* <- cout
* Fin de la ejecucion.
 39:  HALT   0,0,0 
