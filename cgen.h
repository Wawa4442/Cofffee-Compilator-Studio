/****************************************************/
/* Archivo: cgen.h                                  */
/* Interfaz del Generador de Codigo para la         */
/* Tiny Machine - Coffee Compiler Studio            */
/****************************************************/

#ifndef _CGEN_H_
#define _CGEN_H_

#include <stdio.h>

/* Estructura de nodo AST equivalente a NodoAST del compilador */
typedef enum { StmtK, ExpK } NodeKind;
typedef enum { IfK, WhileK, DoUntilK, AssignK, UnaryK, ReadK, WriteK } StmtKind;
typedef enum { OpK, ConstK, IdK } ExpKind;

#define MAXCHILDREN 3

typedef struct treeNode {
    struct treeNode * child[MAXCHILDREN];
    struct treeNode * sibling;
    int lineno;
    NodeKind nodekind;
    union { StmtKind stmt; ExpKind exp; } kind;
    struct {
        const char * op;
        double val;
        const char * name;
    } attr;
} TreeNode;

/* Procedimiento codeGen genera codigo en un archivo
 * recorriendo el arbol sintactico. El segundo argumento
 * es el nombre del archivo de codigo objeto (.tm).
 */
void codeGen(TreeNode * syntaxTree, char * codefile);

#endif
