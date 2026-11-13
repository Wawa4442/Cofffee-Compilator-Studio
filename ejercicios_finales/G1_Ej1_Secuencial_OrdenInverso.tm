* Compilacion de Coffee Compiler Studio para Tiny Machine (.tm)
* Archivo objeto: C:/Users/hecto/Documents/Cofffe/Cofffee-Compilator-Studio/ejercicios_finales/G1_Ej1_Secuencial_OrdenInverso.tm
* Preludio estandar:
  0:  LD     6,0(0) 	* cargar mp con la direccion maxima desde localidad 0
  1:  ST     0,0(0) 	* limpiar localidad 0
* Fin del preludio estandar.
* Variable 'A' (int) asignada en dMem[gp+0] (offset 0 B)
* Variable 'B' (int) asignada en dMem[gp+1] (offset 4 B)
* Variable 'C' (int) asignada en dMem[gp+2] (offset 8 B)
* Variable 'D' (int) asignada en dMem[gp+3] (offset 12 B)
* -> cin (lectura)
  2:  IN     0,0,0 	* leer valor para 'A' (int)
  3:  ST     0,0(5) 	* cin: almacenar valor en 'A'
* <- cin
* -> cin (lectura)
  4:  IN     0,0,0 	* leer valor para 'B' (int)
  5:  ST     0,1(5) 	* cin: almacenar valor en 'B'
* <- cin
* -> cin (lectura)
  6:  IN     0,0,0 	* leer valor para 'C' (int)
  7:  ST     0,2(5) 	* cin: almacenar valor en 'C'
* <- cin
* -> cin (lectura)
  8:  IN     0,0,0 	* leer valor para 'D' (int)
  9:  ST     0,3(5) 	* cin: almacenar valor en 'D'
* <- cin
* -> cout (escritura)
* -> identificador (D)
 10:  LD     0,3(5) 	* cargar valor de 'D'
* <- identificador
 11:  OUT    0,0,0 	* cout: escribir valor de ac
* <- cout
* -> cout (escritura)
* -> identificador (C)
 12:  LD     0,2(5) 	* cargar valor de 'C'
* <- identificador
 13:  OUT    0,0,0 	* cout: escribir valor de ac
* <- cout
* -> cout (escritura)
* -> identificador (B)
 14:  LD     0,1(5) 	* cargar valor de 'B'
* <- identificador
 15:  OUT    0,0,0 	* cout: escribir valor de ac
* <- cout
* -> cout (escritura)
* -> identificador (A)
 16:  LD     0,0(5) 	* cargar valor de 'A'
* <- identificador
 17:  OUT    0,0,0 	* cout: escribir valor de ac
* <- cout
* Fin de la ejecucion.
 18:  HALT   0,0,0 
