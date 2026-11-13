* Compilacion de Coffee Compiler Studio para Tiny Machine (.tm)
* Archivo objeto: C:\Users\hecto\Documents\Cofffe\Cofffee-Compilator-Studio\ejercicios_finales\G1_Ej5_Repetitivo_LluviasArgentina.tm
* Preludio estandar:
  0:  LD     6,0(0) 	* cargar mp con la direccion maxima desde localidad 0
  1:  ST     0,0(0) 	* limpiar localidad 0
* Fin del preludio estandar.
* Variable 'mes' (int) asignada en dMem[gp+0] (offset 0 B)
* Variable 'mes_menor_sur' (int) asignada en dMem[gp+1] (offset 4 B)
* Variable 'region_mayor' (int) asignada en dMem[gp+2] (offset 8 B)
* Variable 'lluvia_norte' (float) asignada en dMem[gp+3] (offset 12 B)
* Variable 'lluvia_centro' (float) asignada en dMem[gp+4] (offset 16 B)
* Variable 'lluvia_sur' (float) asignada en dMem[gp+5] (offset 20 B)
* Variable 'suma_norte' (float) asignada en dMem[gp+6] (offset 24 B)
* Variable 'suma_centro' (float) asignada en dMem[gp+7] (offset 28 B)
* Variable 'suma_sur' (float) asignada en dMem[gp+8] (offset 32 B)
* Variable 'prom_centro' (float) asignada en dMem[gp+9] (offset 36 B)
* Variable 'menor_sur' (float) asignada en dMem[gp+10] (offset 40 B)
* Variable 'mayor_anual' (float) asignada en dMem[gp+11] (offset 44 B)
* -> asignacion a 'suma_norte'
* -> constante (0.0)
  2:  LDC    0,0.0(0) 	* cargar constante 0.0
* <- constante
  3:  LDC    1,0.0(0) 	* asegurar representacion float
  4:  ADD    0,0,1 	* promover resultado a float para 'suma_norte'
  5:  ST     0,6(5) 	* asignar: guardar valor en 'suma_norte'
* <- asignacion a 'suma_norte'
* -> asignacion a 'suma_centro'
* -> constante (0.0)
  6:  LDC    0,0.0(0) 	* cargar constante 0.0
* <- constante
  7:  LDC    1,0.0(0) 	* asegurar representacion float
  8:  ADD    0,0,1 	* promover resultado a float para 'suma_centro'
  9:  ST     0,7(5) 	* asignar: guardar valor en 'suma_centro'
* <- asignacion a 'suma_centro'
* -> asignacion a 'suma_sur'
* -> constante (0.0)
 10:  LDC    0,0.0(0) 	* cargar constante 0.0
* <- constante
 11:  LDC    1,0.0(0) 	* asegurar representacion float
 12:  ADD    0,0,1 	* promover resultado a float para 'suma_sur'
 13:  ST     0,8(5) 	* asignar: guardar valor en 'suma_sur'
* <- asignacion a 'suma_sur'
* -> asignacion a 'menor_sur'
* -> constante (999999.0)
 14:  LDC    0,999999.0(0) 	* cargar constante 999999.0
* <- constante
 15:  LDC    1,0.0(0) 	* asegurar representacion float
 16:  ADD    0,0,1 	* promover resultado a float para 'menor_sur'
 17:  ST     0,10(5) 	* asignar: guardar valor en 'menor_sur'
* <- asignacion a 'menor_sur'
* -> asignacion a 'mes_menor_sur'
* -> constante (1)
 18:  LDC    0,1(0) 	* cargar constante 1
* <- constante
 19:  ST     0,1(5) 	* asignar: guardar valor en 'mes_menor_sur'
* <- asignacion a 'mes_menor_sur'
* -> asignacion a 'mes'
* -> constante (1)
 20:  LDC    0,1(0) 	* cargar constante 1
* <- constante
 21:  ST     0,0(5) 	* asignar: guardar valor en 'mes'
* <- asignacion a 'mes'
* -> do-until
* do: inicio del cuerpo del ciclo
* -> cin (lectura)
 22:  IN     0,0,0 	* leer valor para 'lluvia_norte' (float)
 23:  LDC    1,0.0(0) 	* constante 0.0 para promover a float
 24:  ADD    0,0,1 	* convertir 'lluvia_norte' a float
 25:  ST     0,3(5) 	* cin: almacenar valor en 'lluvia_norte'
* <- cin
* -> cin (lectura)
 26:  IN     0,0,0 	* leer valor para 'lluvia_centro' (float)
 27:  LDC    1,0.0(0) 	* constante 0.0 para promover a float
 28:  ADD    0,0,1 	* convertir 'lluvia_centro' a float
 29:  ST     0,4(5) 	* cin: almacenar valor en 'lluvia_centro'
* <- cin
* -> cin (lectura)
 30:  IN     0,0,0 	* leer valor para 'lluvia_sur' (float)
 31:  LDC    1,0.0(0) 	* constante 0.0 para promover a float
 32:  ADD    0,0,1 	* convertir 'lluvia_sur' a float
 33:  ST     0,5(5) 	* cin: almacenar valor en 'lluvia_sur'
* <- cin
* -> asignacion a 'suma_norte'
* -> operador (+)
* -> identificador (suma_norte)
 34:  LD     0,6(5) 	* cargar valor de 'suma_norte'
* <- identificador
 35:  ST     0,0(6) 	* op: push operando izquierdo en temporal
* -> identificador (lluvia_norte)
 36:  LD     0,3(5) 	* cargar valor de 'lluvia_norte'
* <- identificador
 37:  LD     1,0(6) 	* op: cargar operando izquierdo en ac1
 38:  ADD    0,1,0 	* op +
* <- operador (+)
 39:  LDC    1,0.0(0) 	* asegurar representacion float
 40:  ADD    0,0,1 	* promover resultado a float para 'suma_norte'
 41:  ST     0,6(5) 	* asignar: guardar valor en 'suma_norte'
* <- asignacion a 'suma_norte'
* -> asignacion a 'suma_centro'
* -> operador (+)
* -> identificador (suma_centro)
 42:  LD     0,7(5) 	* cargar valor de 'suma_centro'
* <- identificador
 43:  ST     0,0(6) 	* op: push operando izquierdo en temporal
* -> identificador (lluvia_centro)
 44:  LD     0,4(5) 	* cargar valor de 'lluvia_centro'
* <- identificador
 45:  LD     1,0(6) 	* op: cargar operando izquierdo en ac1
 46:  ADD    0,1,0 	* op +
* <- operador (+)
 47:  LDC    1,0.0(0) 	* asegurar representacion float
 48:  ADD    0,0,1 	* promover resultado a float para 'suma_centro'
 49:  ST     0,7(5) 	* asignar: guardar valor en 'suma_centro'
* <- asignacion a 'suma_centro'
* -> asignacion a 'suma_sur'
* -> operador (+)
* -> identificador (suma_sur)
 50:  LD     0,8(5) 	* cargar valor de 'suma_sur'
* <- identificador
 51:  ST     0,0(6) 	* op: push operando izquierdo en temporal
* -> identificador (lluvia_sur)
 52:  LD     0,5(5) 	* cargar valor de 'lluvia_sur'
* <- identificador
 53:  LD     1,0(6) 	* op: cargar operando izquierdo en ac1
 54:  ADD    0,1,0 	* op +
* <- operador (+)
 55:  LDC    1,0.0(0) 	* asegurar representacion float
 56:  ADD    0,0,1 	* promover resultado a float para 'suma_sur'
 57:  ST     0,8(5) 	* asignar: guardar valor en 'suma_sur'
* <- asignacion a 'suma_sur'
* -> if
* -> operador (<)
* -> identificador (lluvia_sur)
 58:  LD     0,5(5) 	* cargar valor de 'lluvia_sur'
* <- identificador
 59:  ST     0,0(6) 	* op: push operando izquierdo en temporal
* -> identificador (menor_sur)
 60:  LD     0,10(5) 	* cargar valor de 'menor_sur'
* <- identificador
 61:  LD     1,0(6) 	* op: cargar operando izquierdo en ac1
 62:  SUB    0,1,0 	* op < (comparar ac1 - ac)
 63:  JLT    0,2(7) 	* saltar a caso verdadero si <
 64:  LDC    0,0(0) 	* caso falso (ac = 0)
 65:  LDA    7,1(7) 	* saltar caso verdadero
 66:  LDC    0,1(0) 	* caso verdadero (ac = 1)
* <- operador (<)
 67:  JEQ    0,6(7) 	* if: jmp al final si condicion es falsa
* if: el salto hacia else/fin va aqui
* -> asignacion a 'menor_sur'
* -> identificador (lluvia_sur)
 68:  LD     0,5(5) 	* cargar valor de 'lluvia_sur'
* <- identificador
 69:  LDC    1,0.0(0) 	* asegurar representacion float
 70:  ADD    0,0,1 	* promover resultado a float para 'menor_sur'
 71:  ST     0,10(5) 	* asignar: guardar valor en 'menor_sur'
* <- asignacion a 'menor_sur'
* -> asignacion a 'mes_menor_sur'
* -> identificador (mes)
 72:  LD     0,0(5) 	* cargar valor de 'mes'
* <- identificador
 73:  ST     0,1(5) 	* asignar: guardar valor en 'mes_menor_sur'
* <- asignacion a 'mes_menor_sur'
* <- if
* -> operador unario mes++
 74:  LD     0,0(5) 	* cargar 'mes'
 75:  LDC    1,1(0) 	* cargar constante 1
 76:  ADD    0,0,1 	* incrementar 'mes'
 77:  ST     0,0(5) 	* guardar nuevo valor en 'mes'
* <- operador unario mes++
* do: evaluar condicion de cierre (until)
* -> operador (>)
* -> identificador (mes)
 78:  LD     0,0(5) 	* cargar valor de 'mes'
* <- identificador
 79:  ST     0,0(6) 	* op: push operando izquierdo en temporal
* -> constante (12)
 80:  LDC    0,12(0) 	* cargar constante 12
* <- constante
 81:  LD     1,0(6) 	* op: cargar operando izquierdo en ac1
 82:  SUB    0,1,0 	* op > (comparar ac1 - ac)
 83:  JGT    0,2(7) 	* saltar a caso verdadero si >
 84:  LDC    0,0(0) 	* caso falso (ac = 0)
 85:  LDA    7,1(7) 	* saltar caso verdadero
 86:  LDC    0,1(0) 	* caso verdadero (ac = 1)
* <- operador (>)
 87:  JEQ    0,-66(7) 	* do-until: regresar al inicio si condicion es falsa
* <- do-until
* -> asignacion a 'prom_centro'
* -> operador (/)
* -> identificador (suma_centro)
 88:  LD     0,7(5) 	* cargar valor de 'suma_centro'
* <- identificador
 89:  ST     0,0(6) 	* op: push operando izquierdo en temporal
* -> constante (12.0)
 90:  LDC    0,12.0(0) 	* cargar constante 12.0
* <- constante
 91:  LD     1,0(6) 	* op: cargar operando izquierdo en ac1
 92:  ST     0,0(6) 	* div: resguardar divisor
 93:  LDC    0,0.0(0) 	* div: constante 0.0
 94:  ADD    1,1,0 	* div: asegurar dividendo float
 95:  LD     0,0(6) 	* div: restaurar divisor
 96:  DIV    0,1,0 	* op /
* <- operador (/)
 97:  LDC    1,0.0(0) 	* asegurar representacion float
 98:  ADD    0,0,1 	* promover resultado a float para 'prom_centro'
 99:  ST     0,9(5) 	* asignar: guardar valor en 'prom_centro'
* <- asignacion a 'prom_centro'
* -> cout (escritura)
* -> identificador (prom_centro)
100:  LD     0,9(5) 	* cargar valor de 'prom_centro'
* <- identificador
101:  OUT    0,0,0 	* cout: escribir valor de ac
* <- cout
* -> cout (escritura)
* -> identificador (mes_menor_sur)
102:  LD     0,1(5) 	* cargar valor de 'mes_menor_sur'
* <- identificador
103:  OUT    0,0,0 	* cout: escribir valor de ac
* <- cout
* -> cout (escritura)
* -> identificador (menor_sur)
104:  LD     0,10(5) 	* cargar valor de 'menor_sur'
* <- identificador
105:  OUT    0,0,0 	* cout: escribir valor de ac
* <- cout
* -> if
* -> operador (&&)
* -> operador (>)
* -> identificador (suma_norte)
106:  LD     0,6(5) 	* cargar valor de 'suma_norte'
* <- identificador
107:  ST     0,0(6) 	* op: push operando izquierdo en temporal
* -> identificador (suma_centro)
108:  LD     0,7(5) 	* cargar valor de 'suma_centro'
* <- identificador
109:  LD     1,0(6) 	* op: cargar operando izquierdo en ac1
110:  SUB    0,1,0 	* op > (comparar ac1 - ac)
111:  JGT    0,2(7) 	* saltar a caso verdadero si >
112:  LDC    0,0(0) 	* caso falso (ac = 0)
113:  LDA    7,1(7) 	* saltar caso verdadero
114:  LDC    0,1(0) 	* caso verdadero (ac = 1)
* <- operador (>)
115:  ST     0,0(6) 	* op: push operando izquierdo en temporal
* -> operador (>)
* -> identificador (suma_norte)
116:  LD     0,6(5) 	* cargar valor de 'suma_norte'
* <- identificador
117:  ST     0,-1(6) 	* op: push operando izquierdo en temporal
* -> identificador (suma_sur)
118:  LD     0,8(5) 	* cargar valor de 'suma_sur'
* <- identificador
119:  LD     1,-1(6) 	* op: cargar operando izquierdo en ac1
120:  SUB    0,1,0 	* op > (comparar ac1 - ac)
121:  JGT    0,2(7) 	* saltar a caso verdadero si >
122:  LDC    0,0(0) 	* caso falso (ac = 0)
123:  LDA    7,1(7) 	* saltar caso verdadero
124:  LDC    0,1(0) 	* caso verdadero (ac = 1)
* <- operador (>)
125:  LD     1,0(6) 	* op: cargar operando izquierdo en ac1
126:  JEQ    1,3(7) 	* AND: si izq es falso (0), saltar a falso
127:  JEQ    0,2(7) 	* AND: si der es falso (0), saltar a falso
128:  LDC    0,1(0) 	* AND: ambos verdaderos (ac = 1)
129:  LDA    7,1(7) 	* AND: saltar caso falso
130:  LDC    0,0(0) 	* AND: caso falso (ac = 0)
* <- operador (&&)
131:  JEQ    0,7(7) 	* if: jmp a else si condicion es falsa
* if: el salto hacia else/fin va aqui
* -> asignacion a 'region_mayor'
* -> constante (1)
132:  LDC    0,1(0) 	* cargar constante 1
* <- constante
133:  ST     0,2(5) 	* asignar: guardar valor en 'region_mayor'
* <- asignacion a 'region_mayor'
* -> asignacion a 'mayor_anual'
* -> identificador (suma_norte)
134:  LD     0,6(5) 	* cargar valor de 'suma_norte'
* <- identificador
135:  LDC    1,0.0(0) 	* asegurar representacion float
136:  ADD    0,0,1 	* promover resultado a float para 'mayor_anual'
137:  ST     0,11(5) 	* asignar: guardar valor en 'mayor_anual'
* <- asignacion a 'mayor_anual'
138:  LDA    7,23(7) 	* if: jmp al final
* if: el salto hacia el final va aqui
* if: rama else
* -> if
* -> operador (>)
* -> identificador (suma_centro)
139:  LD     0,7(5) 	* cargar valor de 'suma_centro'
* <- identificador
140:  ST     0,0(6) 	* op: push operando izquierdo en temporal
* -> identificador (suma_sur)
141:  LD     0,8(5) 	* cargar valor de 'suma_sur'
* <- identificador
142:  LD     1,0(6) 	* op: cargar operando izquierdo en ac1
143:  SUB    0,1,0 	* op > (comparar ac1 - ac)
144:  JGT    0,2(7) 	* saltar a caso verdadero si >
145:  LDC    0,0(0) 	* caso falso (ac = 0)
146:  LDA    7,1(7) 	* saltar caso verdadero
147:  LDC    0,1(0) 	* caso verdadero (ac = 1)
* <- operador (>)
148:  JEQ    0,7(7) 	* if: jmp a else si condicion es falsa
* if: el salto hacia else/fin va aqui
* -> asignacion a 'region_mayor'
* -> constante (2)
149:  LDC    0,2(0) 	* cargar constante 2
* <- constante
150:  ST     0,2(5) 	* asignar: guardar valor en 'region_mayor'
* <- asignacion a 'region_mayor'
* -> asignacion a 'mayor_anual'
* -> identificador (suma_centro)
151:  LD     0,7(5) 	* cargar valor de 'suma_centro'
* <- identificador
152:  LDC    1,0.0(0) 	* asegurar representacion float
153:  ADD    0,0,1 	* promover resultado a float para 'mayor_anual'
154:  ST     0,11(5) 	* asignar: guardar valor en 'mayor_anual'
* <- asignacion a 'mayor_anual'
155:  LDA    7,6(7) 	* if: jmp al final
* if: el salto hacia el final va aqui
* if: rama else
* -> asignacion a 'region_mayor'
* -> constante (3)
156:  LDC    0,3(0) 	* cargar constante 3
* <- constante
157:  ST     0,2(5) 	* asignar: guardar valor en 'region_mayor'
* <- asignacion a 'region_mayor'
* -> asignacion a 'mayor_anual'
* -> identificador (suma_sur)
158:  LD     0,8(5) 	* cargar valor de 'suma_sur'
* <- identificador
159:  LDC    1,0.0(0) 	* asegurar representacion float
160:  ADD    0,0,1 	* promover resultado a float para 'mayor_anual'
161:  ST     0,11(5) 	* asignar: guardar valor en 'mayor_anual'
* <- asignacion a 'mayor_anual'
* <- if
* <- if
* -> cout (escritura)
* -> identificador (region_mayor)
162:  LD     0,2(5) 	* cargar valor de 'region_mayor'
* <- identificador
163:  OUT    0,0,0 	* cout: escribir valor de ac
* <- cout
* -> cout (escritura)
* -> identificador (mayor_anual)
164:  LD     0,11(5) 	* cargar valor de 'mayor_anual'
* <- identificador
165:  OUT    0,0,0 	* cout: escribir valor de ac
* <- cout
* Fin de la ejecucion.
166:  HALT   0,0,0 
