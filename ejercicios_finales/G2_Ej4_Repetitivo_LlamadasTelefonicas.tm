* Compilacion de Coffee Compiler Studio para Tiny Machine (.tm)
* Archivo objeto: C:\Users\hecto\Documents\Cofffe\Cofffee-Compilator-Studio\ejercicios_finales\G2_Ej4_Repetitivo_LlamadasTelefonicas.tm
* Preludio estandar:
  0:  LD     6,0(0) 	* cargar mp con la direccion maxima desde localidad 0
  1:  ST     0,0(0) 	* limpiar localidad 0
* Fin del preludio estandar.
* Variable 'tipo' (int) asignada en dMem[gp+0] (offset 0 B)
* Variable 'duracion' (int) asignada en dMem[gp+1] (offset 4 B)
* Variable 'cuenta_locales' (int) asignada en dMem[gp+2] (offset 8 B)
* Variable 'costo_llamada' (float) asignada en dMem[gp+3] (offset 12 B)
* Variable 'total_pagar' (float) asignada en dMem[gp+4] (offset 16 B)
* -> asignacion a 'cuenta_locales'
* -> constante (0)
  2:  LDC    0,0(0) 	* cargar constante 0
* <- constante
  3:  ST     0,2(5) 	* asignar: guardar valor en 'cuenta_locales'
* <- asignacion a 'cuenta_locales'
* -> asignacion a 'total_pagar'
* -> constante (0.0)
  4:  LDC    0,0.0(0) 	* cargar constante 0.0
* <- constante
  5:  LDC    1,0.0(0) 	* asegurar representacion float
  6:  ADD    0,0,1 	* promover resultado a float para 'total_pagar'
  7:  ST     0,4(5) 	* asignar: guardar valor en 'total_pagar'
* <- asignacion a 'total_pagar'
* -> cin (lectura)
  8:  IN     0,0,0 	* leer valor para 'tipo' (int)
  9:  ST     0,0(5) 	* cin: almacenar valor en 'tipo'
* <- cin
* -> while
* while: evaluar condicion
* -> operador (!=)
* -> identificador (tipo)
 10:  LD     0,0(5) 	* cargar valor de 'tipo'
* <- identificador
 11:  ST     0,0(6) 	* op: push operando izquierdo en temporal
* -> operador (-)
* -> constante (0)
 12:  LDC    0,0(0) 	* cargar constante 0
* <- constante
 13:  ST     0,-1(6) 	* op: push operando izquierdo en temporal
* -> constante (1)
 14:  LDC    0,1(0) 	* cargar constante 1
* <- constante
 15:  LD     1,-1(6) 	* op: cargar operando izquierdo en ac1
 16:  SUB    0,1,0 	* op -
* <- operador (-)
 17:  LD     1,0(6) 	* op: cargar operando izquierdo en ac1
 18:  SUB    0,1,0 	* op != (comparar ac1 - ac)
 19:  JNE    0,2(7) 	* saltar a caso verdadero si !=
 20:  LDC    0,0(0) 	* caso falso (ac = 0)
 21:  LDA    7,1(7) 	* saltar caso verdadero
 22:  LDC    0,1(0) 	* caso verdadero (ac = 1)
* <- operador (!=)
 23:  JEQ    0,136(7) 	* while: salir del ciclo si condicion es falsa
* while: salto hacia el final si es falso
* -> cin (lectura)
 24:  IN     0,0,0 	* leer valor para 'duracion' (int)
 25:  ST     0,1(5) 	* cin: almacenar valor en 'duracion'
* <- cin
* -> asignacion a 'costo_llamada'
* -> constante (0.0)
 26:  LDC    0,0.0(0) 	* cargar constante 0.0
* <- constante
 27:  LDC    1,0.0(0) 	* asegurar representacion float
 28:  ADD    0,0,1 	* promover resultado a float para 'costo_llamada'
 29:  ST     0,3(5) 	* asignar: guardar valor en 'costo_llamada'
* <- asignacion a 'costo_llamada'
* -> if
* -> operador (==)
* -> identificador (tipo)
 30:  LD     0,0(5) 	* cargar valor de 'tipo'
* <- identificador
 31:  ST     0,0(6) 	* op: push operando izquierdo en temporal
* -> constante (1)
 32:  LDC    0,1(0) 	* cargar constante 1
* <- constante
 33:  LD     1,0(6) 	* op: cargar operando izquierdo en ac1
 34:  SUB    0,1,0 	* op == (comparar ac1 - ac)
 35:  JEQ    0,2(7) 	* saltar a caso verdadero si ==
 36:  LDC    0,0(0) 	* caso falso (ac = 0)
 37:  LDA    7,1(7) 	* saltar caso verdadero
 38:  LDC    0,1(0) 	* caso verdadero (ac = 1)
* <- operador (==)
 39:  JEQ    0,32(7) 	* if: jmp a else si condicion es falsa
* if: el salto hacia else/fin va aqui
* -> if
* -> operador (<=)
* -> identificador (duracion)
 40:  LD     0,1(5) 	* cargar valor de 'duracion'
* <- identificador
 41:  ST     0,0(6) 	* op: push operando izquierdo en temporal
* -> constante (3)
 42:  LDC    0,3(0) 	* cargar constante 3
* <- constante
 43:  LD     1,0(6) 	* op: cargar operando izquierdo en ac1
 44:  SUB    0,1,0 	* op <= (comparar ac1 - ac)
 45:  JLE    0,2(7) 	* saltar a caso verdadero si <=
 46:  LDC    0,0(0) 	* caso falso (ac = 0)
 47:  LDA    7,1(7) 	* saltar caso verdadero
 48:  LDC    0,1(0) 	* caso verdadero (ac = 1)
* <- operador (<=)
 49:  JEQ    0,5(7) 	* if: jmp a else si condicion es falsa
* if: el salto hacia else/fin va aqui
* -> asignacion a 'costo_llamada'
* -> constante (7.59)
 50:  LDC    0,7.59(0) 	* cargar constante 7.59
* <- constante
 51:  LDC    1,0.0(0) 	* asegurar representacion float
 52:  ADD    0,0,1 	* promover resultado a float para 'costo_llamada'
 53:  ST     0,3(5) 	* asignar: guardar valor en 'costo_llamada'
* <- asignacion a 'costo_llamada'
 54:  LDA    7,16(7) 	* if: jmp al final
* if: el salto hacia el final va aqui
* if: rama else
* -> asignacion a 'costo_llamada'
* -> operador (+)
* -> constante (7.59)
 55:  LDC    0,7.59(0) 	* cargar constante 7.59
* <- constante
 56:  ST     0,0(6) 	* op: push operando izquierdo en temporal
* -> operador (*)
* -> operador (-)
* -> identificador (duracion)
 57:  LD     0,1(5) 	* cargar valor de 'duracion'
* <- identificador
 58:  ST     0,-1(6) 	* op: push operando izquierdo en temporal
* -> constante (3)
 59:  LDC    0,3(0) 	* cargar constante 3
* <- constante
 60:  LD     1,-1(6) 	* op: cargar operando izquierdo en ac1
 61:  SUB    0,1,0 	* op -
* <- operador (-)
 62:  ST     0,-1(6) 	* op: push operando izquierdo en temporal
* -> constante (3.03)
 63:  LDC    0,3.03(0) 	* cargar constante 3.03
* <- constante
 64:  LD     1,-1(6) 	* op: cargar operando izquierdo en ac1
 65:  MUL    0,1,0 	* op *
* <- operador (*)
 66:  LD     1,0(6) 	* op: cargar operando izquierdo en ac1
 67:  ADD    0,1,0 	* op +
* <- operador (+)
 68:  LDC    1,0.0(0) 	* asegurar representacion float
 69:  ADD    0,0,1 	* promover resultado a float para 'costo_llamada'
 70:  ST     0,3(5) 	* asignar: guardar valor en 'costo_llamada'
* <- asignacion a 'costo_llamada'
* <- if
 71:  LDA    7,75(7) 	* if: jmp al final
* if: el salto hacia el final va aqui
* if: rama else
* -> if
* -> operador (==)
* -> identificador (tipo)
 72:  LD     0,0(5) 	* cargar valor de 'tipo'
* <- identificador
 73:  ST     0,0(6) 	* op: push operando izquierdo en temporal
* -> constante (2)
 74:  LDC    0,2(0) 	* cargar constante 2
* <- constante
 75:  LD     1,0(6) 	* op: cargar operando izquierdo en ac1
 76:  SUB    0,1,0 	* op == (comparar ac1 - ac)
 77:  JEQ    0,2(7) 	* saltar a caso verdadero si ==
 78:  LDC    0,0(0) 	* caso falso (ac = 0)
 79:  LDA    7,1(7) 	* saltar caso verdadero
 80:  LDC    0,1(0) 	* caso verdadero (ac = 1)
* <- operador (==)
 81:  JEQ    0,32(7) 	* if: jmp a else si condicion es falsa
* if: el salto hacia else/fin va aqui
* -> if
* -> operador (<=)
* -> identificador (duracion)
 82:  LD     0,1(5) 	* cargar valor de 'duracion'
* <- identificador
 83:  ST     0,0(6) 	* op: push operando izquierdo en temporal
* -> constante (3)
 84:  LDC    0,3(0) 	* cargar constante 3
* <- constante
 85:  LD     1,0(6) 	* op: cargar operando izquierdo en ac1
 86:  SUB    0,1,0 	* op <= (comparar ac1 - ac)
 87:  JLE    0,2(7) 	* saltar a caso verdadero si <=
 88:  LDC    0,0(0) 	* caso falso (ac = 0)
 89:  LDA    7,1(7) 	* saltar caso verdadero
 90:  LDC    0,1(0) 	* caso verdadero (ac = 1)
* <- operador (<=)
 91:  JEQ    0,5(7) 	* if: jmp a else si condicion es falsa
* if: el salto hacia else/fin va aqui
* -> asignacion a 'costo_llamada'
* -> constante (1.20)
 92:  LDC    0,1.2(0) 	* cargar constante 1.20
* <- constante
 93:  LDC    1,0.0(0) 	* asegurar representacion float
 94:  ADD    0,0,1 	* promover resultado a float para 'costo_llamada'
 95:  ST     0,3(5) 	* asignar: guardar valor en 'costo_llamada'
* <- asignacion a 'costo_llamada'
 96:  LDA    7,16(7) 	* if: jmp al final
* if: el salto hacia el final va aqui
* if: rama else
* -> asignacion a 'costo_llamada'
* -> operador (+)
* -> constante (1.20)
 97:  LDC    0,1.2(0) 	* cargar constante 1.20
* <- constante
 98:  ST     0,0(6) 	* op: push operando izquierdo en temporal
* -> operador (*)
* -> operador (-)
* -> identificador (duracion)
 99:  LD     0,1(5) 	* cargar valor de 'duracion'
* <- identificador
100:  ST     0,-1(6) 	* op: push operando izquierdo en temporal
* -> constante (3)
101:  LDC    0,3(0) 	* cargar constante 3
* <- constante
102:  LD     1,-1(6) 	* op: cargar operando izquierdo en ac1
103:  SUB    0,1,0 	* op -
* <- operador (-)
104:  ST     0,-1(6) 	* op: push operando izquierdo en temporal
* -> constante (0.48)
105:  LDC    0,0.48(0) 	* cargar constante 0.48
* <- constante
106:  LD     1,-1(6) 	* op: cargar operando izquierdo en ac1
107:  MUL    0,1,0 	* op *
* <- operador (*)
108:  LD     1,0(6) 	* op: cargar operando izquierdo en ac1
109:  ADD    0,1,0 	* op +
* <- operador (+)
110:  LDC    1,0.0(0) 	* asegurar representacion float
111:  ADD    0,0,1 	* promover resultado a float para 'costo_llamada'
112:  ST     0,3(5) 	* asignar: guardar valor en 'costo_llamada'
* <- asignacion a 'costo_llamada'
* <- if
113:  LDA    7,33(7) 	* if: jmp al final
* if: el salto hacia el final va aqui
* if: rama else
* -> if
* -> operador (==)
* -> identificador (tipo)
114:  LD     0,0(5) 	* cargar valor de 'tipo'
* <- identificador
115:  ST     0,0(6) 	* op: push operando izquierdo en temporal
* -> constante (3)
116:  LDC    0,3(0) 	* cargar constante 3
* <- constante
117:  LD     1,0(6) 	* op: cargar operando izquierdo en ac1
118:  SUB    0,1,0 	* op == (comparar ac1 - ac)
119:  JEQ    0,2(7) 	* saltar a caso verdadero si ==
120:  LDC    0,0(0) 	* caso falso (ac = 0)
121:  LDA    7,1(7) 	* saltar caso verdadero
122:  LDC    0,1(0) 	* caso verdadero (ac = 1)
* <- operador (==)
123:  JEQ    0,23(7) 	* if: jmp al final si condicion es falsa
* if: el salto hacia else/fin va aqui
* -> operador unario cuenta_locales++
124:  LD     0,2(5) 	* cargar 'cuenta_locales'
125:  LDC    1,1(0) 	* cargar constante 1
126:  ADD    0,0,1 	* incrementar 'cuenta_locales'
127:  ST     0,2(5) 	* guardar nuevo valor en 'cuenta_locales'
* <- operador unario cuenta_locales++
* -> if
* -> operador (>)
* -> identificador (cuenta_locales)
128:  LD     0,2(5) 	* cargar valor de 'cuenta_locales'
* <- identificador
129:  ST     0,0(6) 	* op: push operando izquierdo en temporal
* -> constante (50)
130:  LDC    0,50(0) 	* cargar constante 50
* <- constante
131:  LD     1,0(6) 	* op: cargar operando izquierdo en ac1
132:  SUB    0,1,0 	* op > (comparar ac1 - ac)
133:  JGT    0,2(7) 	* saltar a caso verdadero si >
134:  LDC    0,0(0) 	* caso falso (ac = 0)
135:  LDA    7,1(7) 	* saltar caso verdadero
136:  LDC    0,1(0) 	* caso verdadero (ac = 1)
* <- operador (>)
137:  JEQ    0,5(7) 	* if: jmp a else si condicion es falsa
* if: el salto hacia else/fin va aqui
* -> asignacion a 'costo_llamada'
* -> constante (0.60)
138:  LDC    0,0.6(0) 	* cargar constante 0.60
* <- constante
139:  LDC    1,0.0(0) 	* asegurar representacion float
140:  ADD    0,0,1 	* promover resultado a float para 'costo_llamada'
141:  ST     0,3(5) 	* asignar: guardar valor en 'costo_llamada'
* <- asignacion a 'costo_llamada'
142:  LDA    7,4(7) 	* if: jmp al final
* if: el salto hacia el final va aqui
* if: rama else
* -> asignacion a 'costo_llamada'
* -> constante (0.0)
143:  LDC    0,0.0(0) 	* cargar constante 0.0
* <- constante
144:  LDC    1,0.0(0) 	* asegurar representacion float
145:  ADD    0,0,1 	* promover resultado a float para 'costo_llamada'
146:  ST     0,3(5) 	* asignar: guardar valor en 'costo_llamada'
* <- asignacion a 'costo_llamada'
* <- if
* <- if
* <- if
* <- if
* -> cout (escritura)
* -> identificador (costo_llamada)
147:  LD     0,3(5) 	* cargar valor de 'costo_llamada'
* <- identificador
148:  OUT    0,0,0 	* cout: escribir valor de ac
* <- cout
* -> asignacion a 'total_pagar'
* -> operador (+)
* -> identificador (total_pagar)
149:  LD     0,4(5) 	* cargar valor de 'total_pagar'
* <- identificador
150:  ST     0,0(6) 	* op: push operando izquierdo en temporal
* -> identificador (costo_llamada)
151:  LD     0,3(5) 	* cargar valor de 'costo_llamada'
* <- identificador
152:  LD     1,0(6) 	* op: cargar operando izquierdo en ac1
153:  ADD    0,1,0 	* op +
* <- operador (+)
154:  LDC    1,0.0(0) 	* asegurar representacion float
155:  ADD    0,0,1 	* promover resultado a float para 'total_pagar'
156:  ST     0,4(5) 	* asignar: guardar valor en 'total_pagar'
* <- asignacion a 'total_pagar'
* -> cin (lectura)
157:  IN     0,0,0 	* leer valor para 'tipo' (int)
158:  ST     0,0(5) 	* cin: almacenar valor en 'tipo'
* <- cin
159:  LDA    7,-150(7) 	* while: regresar al inicio del ciclo
* <- while
* -> cout (escritura)
* -> identificador (total_pagar)
160:  LD     0,4(5) 	* cargar valor de 'total_pagar'
* <- identificador
161:  OUT    0,0,0 	* cout: escribir valor de ac
* <- cout
* Fin de la ejecucion.
162:  HALT   0,0,0 
