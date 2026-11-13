* Compilacion de Coffee Compiler Studio para Tiny Machine (.tm)
* Archivo objeto: C:\Users\hecto\Documents\Cofffe\Cofffee-Compilator-Studio\ejercicios_finales\G2_Ej3_Selectivo_ImpuestoArticulo.tm
* Preludio estandar:
  0:  LD     6,0(0) 	* cargar mp con la direccion maxima desde localidad 0
  1:  ST     0,0(0) 	* limpiar localidad 0
* Fin del preludio estandar.
* Variable 'costo_basico' (float) asignada en dMem[gp+0] (offset 0 B)
* Variable 'impuesto' (float) asignada en dMem[gp+1] (offset 4 B)
* Variable 'precio_total' (float) asignada en dMem[gp+2] (offset 8 B)
* -> cin (lectura)
  2:  IN     0,0,0 	* leer valor para 'costo_basico' (float)
  3:  LDC    1,0.0(0) 	* constante 0.0 para promover a float
  4:  ADD    0,0,1 	* convertir 'costo_basico' a float
  5:  ST     0,0(5) 	* cin: almacenar valor en 'costo_basico'
* <- cin
* -> if
* -> operador (<=)
* -> identificador (costo_basico)
  6:  LD     0,0(5) 	* cargar valor de 'costo_basico'
* <- identificador
  7:  ST     0,0(6) 	* op: push operando izquierdo en temporal
* -> constante (20.0)
  8:  LDC    0,20.0(0) 	* cargar constante 20.0
* <- constante
  9:  LD     1,0(6) 	* op: cargar operando izquierdo en ac1
 10:  SUB    0,1,0 	* op <= (comparar ac1 - ac)
 11:  JLE    0,2(7) 	* saltar a caso verdadero si <=
 12:  LDC    0,0(0) 	* caso falso (ac = 0)
 13:  LDA    7,1(7) 	* saltar caso verdadero
 14:  LDC    0,1(0) 	* caso verdadero (ac = 1)
* <- operador (<=)
 15:  JEQ    0,5(7) 	* if: jmp a else si condicion es falsa
* if: el salto hacia else/fin va aqui
* -> asignacion a 'impuesto'
* -> constante (0.0)
 16:  LDC    0,0.0(0) 	* cargar constante 0.0
* <- constante
 17:  LDC    1,0.0(0) 	* asegurar representacion float
 18:  ADD    0,0,1 	* promover resultado a float para 'impuesto'
 19:  ST     0,1(5) 	* asignar: guardar valor en 'impuesto'
* <- asignacion a 'impuesto'
 20:  LDA    7,74(7) 	* if: jmp al final
* if: el salto hacia el final va aqui
* if: rama else
* -> if
* -> operador (<=)
* -> identificador (costo_basico)
 21:  LD     0,0(5) 	* cargar valor de 'costo_basico'
* <- identificador
 22:  ST     0,0(6) 	* op: push operando izquierdo en temporal
* -> constante (40.0)
 23:  LDC    0,40.0(0) 	* cargar constante 40.0
* <- constante
 24:  LD     1,0(6) 	* op: cargar operando izquierdo en ac1
 25:  SUB    0,1,0 	* op <= (comparar ac1 - ac)
 26:  JLE    0,2(7) 	* saltar a caso verdadero si <=
 27:  LDC    0,0(0) 	* caso falso (ac = 0)
 28:  LDA    7,1(7) 	* saltar caso verdadero
 29:  LDC    0,1(0) 	* caso verdadero (ac = 1)
* <- operador (<=)
 30:  JEQ    0,13(7) 	* if: jmp a else si condicion es falsa
* if: el salto hacia else/fin va aqui
* -> asignacion a 'impuesto'
* -> operador (*)
* -> operador (-)
* -> identificador (costo_basico)
 31:  LD     0,0(5) 	* cargar valor de 'costo_basico'
* <- identificador
 32:  ST     0,0(6) 	* op: push operando izquierdo en temporal
* -> constante (20.0)
 33:  LDC    0,20.0(0) 	* cargar constante 20.0
* <- constante
 34:  LD     1,0(6) 	* op: cargar operando izquierdo en ac1
 35:  SUB    0,1,0 	* op -
* <- operador (-)
 36:  ST     0,0(6) 	* op: push operando izquierdo en temporal
* -> constante (0.30)
 37:  LDC    0,0.3(0) 	* cargar constante 0.30
* <- constante
 38:  LD     1,0(6) 	* op: cargar operando izquierdo en ac1
 39:  MUL    0,1,0 	* op *
* <- operador (*)
 40:  LDC    1,0.0(0) 	* asegurar representacion float
 41:  ADD    0,0,1 	* promover resultado a float para 'impuesto'
 42:  ST     0,1(5) 	* asignar: guardar valor en 'impuesto'
* <- asignacion a 'impuesto'
 43:  LDA    7,51(7) 	* if: jmp al final
* if: el salto hacia el final va aqui
* if: rama else
* -> if
* -> operador (<=)
* -> identificador (costo_basico)
 44:  LD     0,0(5) 	* cargar valor de 'costo_basico'
* <- identificador
 45:  ST     0,0(6) 	* op: push operando izquierdo en temporal
* -> constante (500.0)
 46:  LDC    0,500.0(0) 	* cargar constante 500.0
* <- constante
 47:  LD     1,0(6) 	* op: cargar operando izquierdo en ac1
 48:  SUB    0,1,0 	* op <= (comparar ac1 - ac)
 49:  JLE    0,2(7) 	* saltar a caso verdadero si <=
 50:  LDC    0,0(0) 	* caso falso (ac = 0)
 51:  LDA    7,1(7) 	* saltar caso verdadero
 52:  LDC    0,1(0) 	* caso verdadero (ac = 1)
* <- operador (<=)
 53:  JEQ    0,21(7) 	* if: jmp a else si condicion es falsa
* if: el salto hacia else/fin va aqui
* -> asignacion a 'impuesto'
* -> operador (+)
* -> operador (*)
* -> constante (20.0)
 54:  LDC    0,20.0(0) 	* cargar constante 20.0
* <- constante
 55:  ST     0,0(6) 	* op: push operando izquierdo en temporal
* -> constante (0.30)
 56:  LDC    0,0.3(0) 	* cargar constante 0.30
* <- constante
 57:  LD     1,0(6) 	* op: cargar operando izquierdo en ac1
 58:  MUL    0,1,0 	* op *
* <- operador (*)
 59:  ST     0,0(6) 	* op: push operando izquierdo en temporal
* -> operador (*)
* -> operador (-)
* -> identificador (costo_basico)
 60:  LD     0,0(5) 	* cargar valor de 'costo_basico'
* <- identificador
 61:  ST     0,-1(6) 	* op: push operando izquierdo en temporal
* -> constante (40.0)
 62:  LDC    0,40.0(0) 	* cargar constante 40.0
* <- constante
 63:  LD     1,-1(6) 	* op: cargar operando izquierdo en ac1
 64:  SUB    0,1,0 	* op -
* <- operador (-)
 65:  ST     0,-1(6) 	* op: push operando izquierdo en temporal
* -> constante (0.40)
 66:  LDC    0,0.4(0) 	* cargar constante 0.40
* <- constante
 67:  LD     1,-1(6) 	* op: cargar operando izquierdo en ac1
 68:  MUL    0,1,0 	* op *
* <- operador (*)
 69:  LD     1,0(6) 	* op: cargar operando izquierdo en ac1
 70:  ADD    0,1,0 	* op +
* <- operador (+)
 71:  LDC    1,0.0(0) 	* asegurar representacion float
 72:  ADD    0,0,1 	* promover resultado a float para 'impuesto'
 73:  ST     0,1(5) 	* asignar: guardar valor en 'impuesto'
* <- asignacion a 'impuesto'
 74:  LDA    7,20(7) 	* if: jmp al final
* if: el salto hacia el final va aqui
* if: rama else
* -> asignacion a 'impuesto'
* -> operador (+)
* -> operador (*)
* -> constante (20.0)
 75:  LDC    0,20.0(0) 	* cargar constante 20.0
* <- constante
 76:  ST     0,0(6) 	* op: push operando izquierdo en temporal
* -> constante (0.30)
 77:  LDC    0,0.3(0) 	* cargar constante 0.30
* <- constante
 78:  LD     1,0(6) 	* op: cargar operando izquierdo en ac1
 79:  MUL    0,1,0 	* op *
* <- operador (*)
 80:  ST     0,0(6) 	* op: push operando izquierdo en temporal
* -> operador (*)
* -> operador (-)
* -> identificador (costo_basico)
 81:  LD     0,0(5) 	* cargar valor de 'costo_basico'
* <- identificador
 82:  ST     0,-1(6) 	* op: push operando izquierdo en temporal
* -> constante (40.0)
 83:  LDC    0,40.0(0) 	* cargar constante 40.0
* <- constante
 84:  LD     1,-1(6) 	* op: cargar operando izquierdo en ac1
 85:  SUB    0,1,0 	* op -
* <- operador (-)
 86:  ST     0,-1(6) 	* op: push operando izquierdo en temporal
* -> constante (0.50)
 87:  LDC    0,0.5(0) 	* cargar constante 0.50
* <- constante
 88:  LD     1,-1(6) 	* op: cargar operando izquierdo en ac1
 89:  MUL    0,1,0 	* op *
* <- operador (*)
 90:  LD     1,0(6) 	* op: cargar operando izquierdo en ac1
 91:  ADD    0,1,0 	* op +
* <- operador (+)
 92:  LDC    1,0.0(0) 	* asegurar representacion float
 93:  ADD    0,0,1 	* promover resultado a float para 'impuesto'
 94:  ST     0,1(5) 	* asignar: guardar valor en 'impuesto'
* <- asignacion a 'impuesto'
* <- if
* <- if
* <- if
* -> asignacion a 'precio_total'
* -> operador (+)
* -> identificador (costo_basico)
 95:  LD     0,0(5) 	* cargar valor de 'costo_basico'
* <- identificador
 96:  ST     0,0(6) 	* op: push operando izquierdo en temporal
* -> identificador (impuesto)
 97:  LD     0,1(5) 	* cargar valor de 'impuesto'
* <- identificador
 98:  LD     1,0(6) 	* op: cargar operando izquierdo en ac1
 99:  ADD    0,1,0 	* op +
* <- operador (+)
100:  LDC    1,0.0(0) 	* asegurar representacion float
101:  ADD    0,0,1 	* promover resultado a float para 'precio_total'
102:  ST     0,2(5) 	* asignar: guardar valor en 'precio_total'
* <- asignacion a 'precio_total'
* -> cout (escritura)
* -> identificador (precio_total)
103:  LD     0,2(5) 	* cargar valor de 'precio_total'
* <- identificador
104:  OUT    0,0,0 	* cout: escribir valor de ac
* <- cout
* Fin de la ejecucion.
105:  HALT   0,0,0 
