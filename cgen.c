/****************************************************/
/* Archivo: cgen.c                                  */
/* Implementacion del Generador de Codigo para TM   */
/* Coffee Compiler Studio - Compiladores II UAA     */
/****************************************************/

#include <stdio.h>
#include <string.h>
#include "code.h"
#include "cgen.h"

extern int st_lookup( const char * name );
extern int TraceCode;
extern FILE * code;

/* tmpOffset es el desplazamiento de memoria para los temporales.
 * Se decrementa cada vez que un temporal se almacena, y se
 * incrementa cuando se carga de nuevo.
 */
static int tmpOffset = 0;

/* Prototipo para el generador de codigo interno recursivo */
static void cGen( TreeNode * tree );

/* Procedimiento genStmt genera codigo en un nodo de sentencia */
static void genStmt( TreeNode * tree )
{
    TreeNode * p1, * p2, * p3;
    int savedLoc1, savedLoc2, currentLoc;
    int loc;

    switch (tree->kind.stmt) {

        case IfK :
            if (TraceCode) emitComment("-> if") ;
            p1 = tree->child[0] ;
            p2 = tree->child[1] ;
            p3 = tree->child[2] ;
            /* generar codigo para expresion de prueba */
            cGen(p1);
            savedLoc1 = emitSkip(1) ;
            emitComment("if: jump to else belongs here");
            /* recursion en la parte then */
            cGen(p2);
            if (p3 != NULL) {
                savedLoc2 = emitSkip(1) ;
                emitComment("if: jump to end belongs here");
                currentLoc = emitSkip(0) ;
                emitBackup(savedLoc1) ;
                emitRM_Abs("JEQ", ac, currentLoc, "if: jmp to else");
                emitRestore() ;
                /* recursion en la parte else */
                cGen(p3);
                currentLoc = emitSkip(0) ;
                emitBackup(savedLoc2) ;
                emitRM_Abs("LDA", pc, currentLoc, "jmp to end") ;
                emitRestore() ;
            } else {
                currentLoc = emitSkip(0) ;
                emitBackup(savedLoc1) ;
                emitRM_Abs("JEQ", ac, currentLoc, "if: jmp to end");
                emitRestore() ;
            }
            if (TraceCode)  emitComment("<- if") ;
            break;

        case WhileK :
            if (TraceCode) emitComment("-> while") ;
            p1 = tree->child[0] ;
            p2 = tree->child[1] ;
            savedLoc1 = emitSkip(0) ;
            emitComment("while: inicio evaluacion de condicion");
            cGen(p1);
            savedLoc2 = emitSkip(1) ;
            cGen(p2);
            emitRM_Abs("LDA", pc, savedLoc1, "while: regresar al inicio");
            currentLoc = emitSkip(0) ;
            emitBackup(savedLoc2) ;
            emitRM_Abs("JEQ", ac, currentLoc, "while: salir si falso");
            emitRestore() ;
            if (TraceCode) emitComment("<- while") ;
            break;

        case DoUntilK :
            if (TraceCode) emitComment("-> do-until") ;
            p1 = tree->child[0] ;
            p2 = tree->child[1] ;
            savedLoc1 = emitSkip(0);
            emitComment("do-until: salto al inicio pertenece aqui");
            /* generar codigo para el cuerpo */
            cGen(p1);
            /* generar codigo para la prueba */
            cGen(p2);
            emitRM_Abs("JEQ", ac, savedLoc1, "do-until: jmp back to body");
            if (TraceCode) emitComment("<- do-until") ;
            break;

        case ReadK :
            emitRO("IN", ac, 0, 0, "leer valor cin");
            loc = st_lookup(tree->attr.name);
            emitRM("ST", ac, loc, gp, "cin: almacenar valor");
            break;

        case WriteK :
            /* generar codigo para expresion a escribir */
            cGen(tree->child[0]);
            /* ahora dar salida */
            emitRO("OUT", ac, 0, 0, "cout: escribir ac");
            break;

        case AssignK :
            if (TraceCode) emitComment("-> asignacion") ;
            /* generar codigo para rhs */
            cGen(tree->child[0]);
            /* ahora almacenar valor */
            loc = st_lookup(tree->attr.name);
            emitRM("ST", ac, loc, gp, "asignacion: almacenar valor");
            if (TraceCode) emitComment("<- asignacion") ;
            break;

        case UnaryK :
            loc = st_lookup(tree->attr.name);
            emitRM("LD", ac, loc, gp, "cargar variable para op unario");
            emitRM("LDC", ac1, 1, 0, "cargar 1");
            if (strcmp(tree->attr.op, "++") == 0)
                emitRO("ADD", ac, ac, ac1, "incrementar ++");
            else
                emitRO("SUB", ac, ac, ac1, "decrementar --");
            emitRM("ST", ac, loc, gp, "guardar variable");
            break;

        default:
            break;
    }
}

/* Procedimiento genExp genera codigo en un nodo de expresion */
static void genExp( TreeNode * tree )
{
    int loc;
    TreeNode * p1, * p2;

    switch (tree->kind.exp) {

        case ConstK :
            if (TraceCode) emitComment("-> constante") ;
            emitRM("LDC", ac, tree->attr.val, 0, "cargar constante");
            if (TraceCode) emitComment("<- constante") ;
            break;

        case IdK :
            if (TraceCode) emitComment("-> identificador") ;
            loc = st_lookup(tree->attr.name);
            emitRM("LD", ac, loc, gp, "cargar valor de id");
            if (TraceCode) emitComment("<- identificador") ;
            break;

        case OpK :
            if (TraceCode) emitComment("-> operador") ;
            p1 = tree->child[0];
            p2 = tree->child[1];
            /* generar codigo para ac = argumento izquierdo */
            cGen(p1);
            /* generar codigo para hacer push del operando izquierdo */
            emitRM("ST", ac, tmpOffset--, mp, "op: push left");
            /* generar codigo para ac = operando derecho */
            cGen(p2);
            /* ahora cargar operando izquierdo */
            emitRM("LD", ac1, ++tmpOffset, mp, "op: load left");

            if (strcmp(tree->attr.op, "+") == 0)
                emitRO("ADD", ac, ac1, ac, "op +");
            else if (strcmp(tree->attr.op, "-") == 0)
                emitRO("SUB", ac, ac1, ac, "op -");
            else if (strcmp(tree->attr.op, "*") == 0)
                emitRO("MUL", ac, ac1, ac, "op *");
            else if (strcmp(tree->attr.op, "/") == 0)
                emitRO("DIV", ac, ac1, ac, "op /");
            else if (strcmp(tree->attr.op, "<") == 0) {
                emitRO("SUB", ac, ac1, ac, "op <") ;
                emitRM("JLT", ac, 2, pc, "br if true") ;
                emitRM("LDC", ac, 0, ac, "false case") ;
                emitRM("LDA", pc, 1, pc, "unconditional jmp") ;
                emitRM("LDC", ac, 1, ac, "true case") ;
            }
            else if (strcmp(tree->attr.op, "<=") == 0) {
                emitRO("SUB", ac, ac1, ac, "op <=") ;
                emitRM("JLE", ac, 2, pc, "br if true") ;
                emitRM("LDC", ac, 0, ac, "false case") ;
                emitRM("LDA", pc, 1, pc, "unconditional jmp") ;
                emitRM("LDC", ac, 1, ac, "true case") ;
            }
            else if (strcmp(tree->attr.op, ">") == 0) {
                emitRO("SUB", ac, ac1, ac, "op >") ;
                emitRM("JGT", ac, 2, pc, "br if true") ;
                emitRM("LDC", ac, 0, ac, "false case") ;
                emitRM("LDA", pc, 1, pc, "unconditional jmp") ;
                emitRM("LDC", ac, 1, ac, "true case") ;
            }
            else if (strcmp(tree->attr.op, ">=") == 0) {
                emitRO("SUB", ac, ac1, ac, "op >=") ;
                emitRM("JGE", ac, 2, pc, "br if true") ;
                emitRM("LDC", ac, 0, ac, "false case") ;
                emitRM("LDA", pc, 1, pc, "unconditional jmp") ;
                emitRM("LDC", ac, 1, ac, "true case") ;
            }
            else if (strcmp(tree->attr.op, "==") == 0) {
                emitRO("SUB", ac, ac1, ac, "op ==") ;
                emitRM("JEQ", ac, 2, pc, "br if true");
                emitRM("LDC", ac, 0, ac, "false case") ;
                emitRM("LDA", pc, 1, pc, "unconditional jmp") ;
                emitRM("LDC", ac, 1, ac, "true case") ;
            }
            else if (strcmp(tree->attr.op, "!=") == 0) {
                emitRO("SUB", ac, ac1, ac, "op !=") ;
                emitRM("JNE", ac, 2, pc, "br if true");
                emitRM("LDC", ac, 0, ac, "false case") ;
                emitRM("LDA", pc, 1, pc, "unconditional jmp") ;
                emitRM("LDC", ac, 1, ac, "true case") ;
            }
            if (TraceCode)  emitComment("<- operador") ;
            break;

        default:
            break;
    }
}

/* Procedimiento cGen genera codigo recursivamente recorriendo el arbol */
static void cGen( TreeNode * tree )
{
    if (tree != NULL) {
        switch (tree->nodekind) {
            case StmtK:
                genStmt(tree);
                break;
            case ExpK:
                genExp(tree);
                break;
            default:
                break;
        }
        cGen(tree->sibling);
    }
}

/* Funcion principal del generador de codigo */
void codeGen(TreeNode * syntaxTree, char * codefile)
{
    emitComment("Compilacion TINY / Coffee Compiler Studio para Codigo TM");
    emitComment("Preludio estandar:");
    emitRM("LD", mp, 0, ac, "cargar maxaddress desde localidad 0");
    emitRM("ST", ac, 0, ac, "limpiar localidad 0");
    emitComment("Fin de preludio estandar.");

    /* generar codigo para el programa */
    cGen(syntaxTree);

    /* terminar */
    emitComment("Fin de la ejecucion.");
    emitRO("HALT", 0, 0, 0, "");
}
