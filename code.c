/****************************************************/
/* Archivo: code.c                                  */
/* Implementacion de las utilidades de emision TM   */
/* Coffee Compiler Studio - Compiladores II UAA     */
/****************************************************/

#include <stdio.h>
#include <math.h>
#include "code.h"

extern FILE * code;
extern int TraceCode;

/* Numero de localidad TM para la instruccion actual */
static int emitLoc = 0 ;

/* Localidad TM mas alta emitida hasta el momento
 * Para uso en conjuncion con emitSkip, emitBackup y emitRestore
 */
static int highEmitLoc = 0;

void emitComment( const char * c )
{
    if (TraceCode) fprintf(code, "* %s\n", c);
}

void emitRO( const char *op, int r, int s, int t, const char *c )
{
    fprintf(code, "%3d:  %5s  %d,%d,%d ", emitLoc++, op, r, s, t);
    if (TraceCode) fprintf(code, "\t* %s", c);
    fprintf(code, "\n");
    if (highEmitLoc < emitLoc) highEmitLoc = emitLoc;
}

void emitRM( const char * op, int r, double d, int s, const char *c )
{
    if (fabs(d - (int)d) < 1e-9)
        fprintf(code, "%3d:  %5s  %d,%d(%d) ", emitLoc++, op, r, (int)d, s);
    else
        fprintf(code, "%3d:  %5s  %d,%.6g(%d) ", emitLoc++, op, r, d, s);
    if (TraceCode) fprintf(code, "\t* %s", c);
    fprintf(code, "\n");
    if (highEmitLoc < emitLoc) highEmitLoc = emitLoc;
}

int emitSkip( int howMany )
{
    int i = emitLoc;
    emitLoc += howMany ;
    if (highEmitLoc < emitLoc) highEmitLoc = emitLoc ;
    return i;
}

void emitBackup( int loc )
{
    if (loc > highEmitLoc) emitComment("BUG in emitBackup");
    emitLoc = loc ;
}

void emitRestore( void )
{
    emitLoc = highEmitLoc;
}

void emitRM_Abs( const char *op, int r, int a, const char * c )
{
    fprintf(code, "%3d:  %5s  %d,%d(%d) ",
            emitLoc, op, r, a - (emitLoc + 1), pc);
    ++emitLoc ;
    if (TraceCode) fprintf(code, "\t* %s", c);
    fprintf(code, "\n");
    if (highEmitLoc < emitLoc) highEmitLoc = emitLoc ;
}
