* Compilacion de Coffee Compiler Studio para Tiny Machine (.tm)
* Archivo objeto: C:/Users/hecto/Documents/Cofffe/Cofffee-Compilator-Studio/ejercicios_finales/G2_Ej5_Repetitivo_BodegaVinos.tm
* Preludio estandar:
  0:  LD     6,0(0) 	* cargar mp con la direccion maxima desde localidad 0
  1:  ST     0,0(0) 	* limpiar localidad 0
* Fin del preludio estandar.
* Variable 'n_anios' (int) asignada en dMem[gp+0] (offset 0 B)
* Variable 'anio' (int) asignada en dMem[gp+1] (offset 4 B)
* Variable 'anio_max_tipo2' (int) asignada en dMem[gp+2] (offset 8 B)
* Variable 'anio_sin_tipo3' (int) asignada en dMem[gp+3] (offset 12 B)
* Variable 'v1' (float) asignada en dMem[gp+4] (offset 16 B)
* Variable 'v2' (float) asignada en dMem[gp+5] (offset 20 B)
* Variable 'v3' (float) asignada en dMem[gp+6] (offset 24 B)
* Variable 'v4' (float) asignada en dMem[gp+7] (offset 28 B)
* Variable 'v5' (float) asignada en dMem[gp+8] (offset 32 B)
* Variable 'tot1' (float) asignada en dMem[gp+9] (offset 36 B)
* Variable 'tot2' (float) asignada en dMem[gp+10] (offset 40 B)
* Variable 'tot3' (float) asignada en dMem[gp+11] (offset 44 B)
* Variable 'tot4' (float) asignada en dMem[gp+12] (offset 48 B)
* Variable 'tot5' (float) asignada en dMem[gp+13] (offset 52 B)
* Variable 'total_anio' (float) asignada en dMem[gp+14] (offset 56 B)
* Variable 'max_tipo2' (float) asignada en dMem[gp+15] (offset 60 B)
* -> asignacion a 'tot1'
* -> constante (0.0)
  2:  LDC    0,0.0(0) 	* cargar constante 0.0
* <- constante
  3:  LDC    1,0.0(0) 	* asegurar representacion float
  4:  ADD    0,0,1 	* promover resultado a float para 'tot1'
  5:  ST     0,9(5) 	* asignar: guardar valor en 'tot1'
* <- asignacion a 'tot1'
* -> asignacion a 'tot2'
* -> constante (0.0)
  6:  LDC    0,0.0(0) 	* cargar constante 0.0
* <- constante
  7:  LDC    1,0.0(0) 	* asegurar representacion float
  8:  ADD    0,0,1 	* promover resultado a float para 'tot2'
  9:  ST     0,10(5) 	* asignar: guardar valor en 'tot2'
* <- asignacion a 'tot2'
* -> asignacion a 'tot3'
* -> constante (0.0)
 10:  LDC    0,0.0(0) 	* cargar constante 0.0
* <- constante
 11:  LDC    1,0.0(0) 	* asegurar representacion float
 12:  ADD    0,0,1 	* promover resultado a float para 'tot3'
 13:  ST     0,11(5) 	* asignar: guardar valor en 'tot3'
* <- asignacion a 'tot3'
* -> asignacion a 'tot4'
* -> constante (0.0)
 14:  LDC    0,0.0(0) 	* cargar constante 0.0
* <- constante
 15:  LDC    1,0.0(0) 	* asegurar representacion float
 16:  ADD    0,0,1 	* promover resultado a float para 'tot4'
 17:  ST     0,12(5) 	* asignar: guardar valor en 'tot4'
* <- asignacion a 'tot4'
* -> asignacion a 'tot5'
* -> constante (0.0)
 18:  LDC    0,0.0(0) 	* cargar constante 0.0
* <- constante
 19:  LDC    1,0.0(0) 	* asegurar representacion float
 20:  ADD    0,0,1 	* promover resultado a float para 'tot5'
 21:  ST     0,13(5) 	* asignar: guardar valor en 'tot5'
* <- asignacion a 'tot5'
* -> asignacion a 'max_tipo2'
* -> operador (-)
* -> constante (0)
 22:  LDC    0,0(0) 	* cargar constante 0
* <- constante
 23:  ST     0,0(6) 	* op: push operando izquierdo en temporal
* -> constante (1.0)
 24:  LDC    0,1.0(0) 	* cargar constante 1.0
* <- constante
 25:  LD     1,0(6) 	* op: cargar operando izquierdo en ac1
 26:  SUB    0,1,0 	* op -
* <- operador (-)
 27:  LDC    1,0.0(0) 	* asegurar representacion float
 28:  ADD    0,0,1 	* promover resultado a float para 'max_tipo2'
 29:  ST     0,15(5) 	* asignar: guardar valor en 'max_tipo2'
* <- asignacion a 'max_tipo2'
* -> asignacion a 'anio_max_tipo2'
* -> constante (0)
 30:  LDC    0,0(0) 	* cargar constante 0
* <- constante
 31:  ST     0,2(5) 	* asignar: guardar valor en 'anio_max_tipo2'
* <- asignacion a 'anio_max_tipo2'
* -> asignacion a 'anio_sin_tipo3'
* -> constante (0)
 32:  LDC    0,0(0) 	* cargar constante 0
* <- constante
 33:  ST     0,3(5) 	* asignar: guardar valor en 'anio_sin_tipo3'
* <- asignacion a 'anio_sin_tipo3'
* -> cin (lectura)
 34:  IN     0,0,0 	* leer valor para 'n_anios' (int)
 35:  ST     0,0(5) 	* cin: almacenar valor en 'n_anios'
* <- cin
* -> asignacion a 'anio'
* -> constante (1)
 36:  LDC    0,1(0) 	* cargar constante 1
* <- constante
 37:  ST     0,1(5) 	* asignar: guardar valor en 'anio'
* <- asignacion a 'anio'
* -> do-until
* do: inicio del cuerpo del ciclo
* -> cin (lectura)
 38:  IN     0,0,0 	* leer valor para 'v1' (float)
 39:  LDC    1,0.0(0) 	* constante 0.0 para promover a float
 40:  ADD    0,0,1 	* convertir 'v1' a float
 41:  ST     0,4(5) 	* cin: almacenar valor en 'v1'
* <- cin
* -> cin (lectura)
 42:  IN     0,0,0 	* leer valor para 'v2' (float)
 43:  LDC    1,0.0(0) 	* constante 0.0 para promover a float
 44:  ADD    0,0,1 	* convertir 'v2' a float
 45:  ST     0,5(5) 	* cin: almacenar valor en 'v2'
* <- cin
* -> cin (lectura)
 46:  IN     0,0,0 	* leer valor para 'v3' (float)
 47:  LDC    1,0.0(0) 	* constante 0.0 para promover a float
 48:  ADD    0,0,1 	* convertir 'v3' a float
 49:  ST     0,6(5) 	* cin: almacenar valor en 'v3'
* <- cin
* -> cin (lectura)
 50:  IN     0,0,0 	* leer valor para 'v4' (float)
 51:  LDC    1,0.0(0) 	* constante 0.0 para promover a float
 52:  ADD    0,0,1 	* convertir 'v4' a float
 53:  ST     0,7(5) 	* cin: almacenar valor en 'v4'
* <- cin
* -> cin (lectura)
 54:  IN     0,0,0 	* leer valor para 'v5' (float)
 55:  LDC    1,0.0(0) 	* constante 0.0 para promover a float
 56:  ADD    0,0,1 	* convertir 'v5' a float
 57:  ST     0,8(5) 	* cin: almacenar valor en 'v5'
* <- cin
* -> asignacion a 'tot1'
* -> operador (+)
* -> identificador (tot1)
 58:  LD     0,9(5) 	* cargar valor de 'tot1'
* <- identificador
 59:  ST     0,0(6) 	* op: push operando izquierdo en temporal
* -> identificador (v1)
 60:  LD     0,4(5) 	* cargar valor de 'v1'
* <- identificador
 61:  LD     1,0(6) 	* op: cargar operando izquierdo en ac1
 62:  ADD    0,1,0 	* op +
* <- operador (+)
 63:  LDC    1,0.0(0) 	* asegurar representacion float
 64:  ADD    0,0,1 	* promover resultado a float para 'tot1'
 65:  ST     0,9(5) 	* asignar: guardar valor en 'tot1'
* <- asignacion a 'tot1'
* -> asignacion a 'tot2'
* -> operador (+)
* -> identificador (tot2)
 66:  LD     0,10(5) 	* cargar valor de 'tot2'
* <- identificador
 67:  ST     0,0(6) 	* op: push operando izquierdo en temporal
* -> identificador (v2)
 68:  LD     0,5(5) 	* cargar valor de 'v2'
* <- identificador
 69:  LD     1,0(6) 	* op: cargar operando izquierdo en ac1
 70:  ADD    0,1,0 	* op +
* <- operador (+)
 71:  LDC    1,0.0(0) 	* asegurar representacion float
 72:  ADD    0,0,1 	* promover resultado a float para 'tot2'
 73:  ST     0,10(5) 	* asignar: guardar valor en 'tot2'
* <- asignacion a 'tot2'
* -> asignacion a 'tot3'
* -> operador (+)
* -> identificador (tot3)
 74:  LD     0,11(5) 	* cargar valor de 'tot3'
* <- identificador
 75:  ST     0,0(6) 	* op: push operando izquierdo en temporal
* -> identificador (v3)
 76:  LD     0,6(5) 	* cargar valor de 'v3'
* <- identificador
 77:  LD     1,0(6) 	* op: cargar operando izquierdo en ac1
 78:  ADD    0,1,0 	* op +
* <- operador (+)
 79:  LDC    1,0.0(0) 	* asegurar representacion float
 80:  ADD    0,0,1 	* promover resultado a float para 'tot3'
 81:  ST     0,11(5) 	* asignar: guardar valor en 'tot3'
* <- asignacion a 'tot3'
* -> asignacion a 'tot4'
* -> operador (+)
* -> identificador (tot4)
 82:  LD     0,12(5) 	* cargar valor de 'tot4'
* <- identificador
 83:  ST     0,0(6) 	* op: push operando izquierdo en temporal
* -> identificador (v4)
 84:  LD     0,7(5) 	* cargar valor de 'v4'
* <- identificador
 85:  LD     1,0(6) 	* op: cargar operando izquierdo en ac1
 86:  ADD    0,1,0 	* op +
* <- operador (+)
 87:  LDC    1,0.0(0) 	* asegurar representacion float
 88:  ADD    0,0,1 	* promover resultado a float para 'tot4'
 89:  ST     0,12(5) 	* asignar: guardar valor en 'tot4'
* <- asignacion a 'tot4'
* -> asignacion a 'tot5'
* -> operador (+)
* -> identificador (tot5)
 90:  LD     0,13(5) 	* cargar valor de 'tot5'
* <- identificador
 91:  ST     0,0(6) 	* op: push operando izquierdo en temporal
* -> identificador (v5)
 92:  LD     0,8(5) 	* cargar valor de 'v5'
* <- identificador
 93:  LD     1,0(6) 	* op: cargar operando izquierdo en ac1
 94:  ADD    0,1,0 	* op +
* <- operador (+)
 95:  LDC    1,0.0(0) 	* asegurar representacion float
 96:  ADD    0,0,1 	* promover resultado a float para 'tot5'
 97:  ST     0,13(5) 	* asignar: guardar valor en 'tot5'
* <- asignacion a 'tot5'
* -> asignacion a 'total_anio'
* -> operador (+)
* -> operador (+)
* -> operador (+)
* -> operador (+)
* -> identificador (v1)
 98:  LD     0,4(5) 	* cargar valor de 'v1'
* <- identificador
 99:  ST     0,0(6) 	* op: push operando izquierdo en temporal
* -> identificador (v2)
100:  LD     0,5(5) 	* cargar valor de 'v2'
* <- identificador
101:  LD     1,0(6) 	* op: cargar operando izquierdo en ac1
102:  ADD    0,1,0 	* op +
* <- operador (+)
103:  ST     0,0(6) 	* op: push operando izquierdo en temporal
* -> identificador (v3)
104:  LD     0,6(5) 	* cargar valor de 'v3'
* <- identificador
105:  LD     1,0(6) 	* op: cargar operando izquierdo en ac1
106:  ADD    0,1,0 	* op +
* <- operador (+)
107:  ST     0,0(6) 	* op: push operando izquierdo en temporal
* -> identificador (v4)
108:  LD     0,7(5) 	* cargar valor de 'v4'
* <- identificador
109:  LD     1,0(6) 	* op: cargar operando izquierdo en ac1
110:  ADD    0,1,0 	* op +
* <- operador (+)
111:  ST     0,0(6) 	* op: push operando izquierdo en temporal
* -> identificador (v5)
112:  LD     0,8(5) 	* cargar valor de 'v5'
* <- identificador
113:  LD     1,0(6) 	* op: cargar operando izquierdo en ac1
114:  ADD    0,1,0 	* op +
* <- operador (+)
115:  LDC    1,0.0(0) 	* asegurar representacion float
116:  ADD    0,0,1 	* promover resultado a float para 'total_anio'
117:  ST     0,14(5) 	* asignar: guardar valor en 'total_anio'
* <- asignacion a 'total_anio'
* -> cout (escritura)
* -> identificador (total_anio)
118:  LD     0,14(5) 	* cargar valor de 'total_anio'
* <- identificador
119:  OUT    0,0,0 	* cout: escribir valor de ac
* <- cout
* -> if
* -> operador (>)
* -> identificador (v2)
120:  LD     0,5(5) 	* cargar valor de 'v2'
* <- identificador
121:  ST     0,0(6) 	* op: push operando izquierdo en temporal
* -> identificador (max_tipo2)
122:  LD     0,15(5) 	* cargar valor de 'max_tipo2'
* <- identificador
123:  LD     1,0(6) 	* op: cargar operando izquierdo en ac1
124:  SUB    0,1,0 	* op > (comparar ac1 - ac)
125:  JGT    0,2(7) 	* saltar a caso verdadero si >
126:  LDC    0,0(0) 	* caso falso (ac = 0)
127:  LDA    7,1(7) 	* saltar caso verdadero
128:  LDC    0,1(0) 	* caso verdadero (ac = 1)
* <- operador (>)
129:  JEQ    0,6(7) 	* if: jmp al final si condicion es falsa
* if: el salto hacia else/fin va aqui
* -> asignacion a 'max_tipo2'
* -> identificador (v2)
130:  LD     0,5(5) 	* cargar valor de 'v2'
* <- identificador
131:  LDC    1,0.0(0) 	* asegurar representacion float
132:  ADD    0,0,1 	* promover resultado a float para 'max_tipo2'
133:  ST     0,15(5) 	* asignar: guardar valor en 'max_tipo2'
* <- asignacion a 'max_tipo2'
* -> asignacion a 'anio_max_tipo2'
* -> identificador (anio)
134:  LD     0,1(5) 	* cargar valor de 'anio'
* <- identificador
135:  ST     0,2(5) 	* asignar: guardar valor en 'anio_max_tipo2'
* <- asignacion a 'anio_max_tipo2'
* <- if
* -> if
* -> operador (==)
* -> identificador (v3)
136:  LD     0,6(5) 	* cargar valor de 'v3'
* <- identificador
137:  ST     0,0(6) 	* op: push operando izquierdo en temporal
* -> constante (0.0)
138:  LDC    0,0.0(0) 	* cargar constante 0.0
* <- constante
139:  LD     1,0(6) 	* op: cargar operando izquierdo en ac1
140:  SUB    0,1,0 	* op == (comparar ac1 - ac)
141:  JEQ    0,2(7) 	* saltar a caso verdadero si ==
142:  LDC    0,0(0) 	* caso falso (ac = 0)
143:  LDA    7,1(7) 	* saltar caso verdadero
144:  LDC    0,1(0) 	* caso verdadero (ac = 1)
* <- operador (==)
145:  JEQ    0,2(7) 	* if: jmp al final si condicion es falsa
* if: el salto hacia else/fin va aqui
* -> asignacion a 'anio_sin_tipo3'
* -> identificador (anio)
146:  LD     0,1(5) 	* cargar valor de 'anio'
* <- identificador
147:  ST     0,3(5) 	* asignar: guardar valor en 'anio_sin_tipo3'
* <- asignacion a 'anio_sin_tipo3'
* <- if
* -> operador unario anio++
148:  LD     0,1(5) 	* cargar 'anio'
149:  LDC    1,1(0) 	* cargar constante 1
150:  ADD    0,0,1 	* incrementar 'anio'
151:  ST     0,1(5) 	* guardar nuevo valor en 'anio'
* <- operador unario anio++
* do: evaluar condicion de cierre (until)
* -> operador (>)
* -> identificador (anio)
152:  LD     0,1(5) 	* cargar valor de 'anio'
* <- identificador
153:  ST     0,0(6) 	* op: push operando izquierdo en temporal
* -> identificador (n_anios)
154:  LD     0,0(5) 	* cargar valor de 'n_anios'
* <- identificador
155:  LD     1,0(6) 	* op: cargar operando izquierdo en ac1
156:  SUB    0,1,0 	* op > (comparar ac1 - ac)
157:  JGT    0,2(7) 	* saltar a caso verdadero si >
158:  LDC    0,0(0) 	* caso falso (ac = 0)
159:  LDA    7,1(7) 	* saltar caso verdadero
160:  LDC    0,1(0) 	* caso verdadero (ac = 1)
* <- operador (>)
161:  JEQ    0,-124(7) 	* do-until: regresar al inicio si condicion es falsa
* <- do-until
* -> cout (escritura)
* -> identificador (tot1)
162:  LD     0,9(5) 	* cargar valor de 'tot1'
* <- identificador
163:  OUT    0,0,0 	* cout: escribir valor de ac
* <- cout
* -> cout (escritura)
* -> identificador (tot2)
164:  LD     0,10(5) 	* cargar valor de 'tot2'
* <- identificador
165:  OUT    0,0,0 	* cout: escribir valor de ac
* <- cout
* -> cout (escritura)
* -> identificador (tot3)
166:  LD     0,11(5) 	* cargar valor de 'tot3'
* <- identificador
167:  OUT    0,0,0 	* cout: escribir valor de ac
* <- cout
* -> cout (escritura)
* -> identificador (tot4)
168:  LD     0,12(5) 	* cargar valor de 'tot4'
* <- identificador
169:  OUT    0,0,0 	* cout: escribir valor de ac
* <- cout
* -> cout (escritura)
* -> identificador (tot5)
170:  LD     0,13(5) 	* cargar valor de 'tot5'
* <- identificador
171:  OUT    0,0,0 	* cout: escribir valor de ac
* <- cout
* -> cout (escritura)
* -> identificador (anio_max_tipo2)
172:  LD     0,2(5) 	* cargar valor de 'anio_max_tipo2'
* <- identificador
173:  OUT    0,0,0 	* cout: escribir valor de ac
* <- cout
* -> cout (escritura)
* -> identificador (max_tipo2)
174:  LD     0,15(5) 	* cargar valor de 'max_tipo2'
* <- identificador
175:  OUT    0,0,0 	* cout: escribir valor de ac
* <- cout
* -> if
* -> operador (>)
* -> identificador (anio_sin_tipo3)
176:  LD     0,3(5) 	* cargar valor de 'anio_sin_tipo3'
* <- identificador
177:  ST     0,0(6) 	* op: push operando izquierdo en temporal
* -> constante (0)
178:  LDC    0,0(0) 	* cargar constante 0
* <- constante
179:  LD     1,0(6) 	* op: cargar operando izquierdo en ac1
180:  SUB    0,1,0 	* op > (comparar ac1 - ac)
181:  JGT    0,2(7) 	* saltar a caso verdadero si >
182:  LDC    0,0(0) 	* caso falso (ac = 0)
183:  LDA    7,1(7) 	* saltar caso verdadero
184:  LDC    0,1(0) 	* caso verdadero (ac = 1)
* <- operador (>)
185:  JEQ    0,2(7) 	* if: jmp al final si condicion es falsa
* if: el salto hacia else/fin va aqui
* -> cout (escritura)
* -> identificador (anio_sin_tipo3)
186:  LD     0,3(5) 	* cargar valor de 'anio_sin_tipo3'
* <- identificador
187:  OUT    0,0,0 	* cout: escribir valor de ac
* <- cout
* <- if
* Fin de la ejecucion.
188:  HALT   0,0,0 
