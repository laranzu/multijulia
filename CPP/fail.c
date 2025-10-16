
/*  Written by Hugh Fisher. Distributed under MIT/X11 license */


#include <stdio.h>
#include <stdarg.h>
#include <stdlib.h>

#include "fail.h"

// This function is meant to be implemented by front end

void MinimalFail(const char * format, ...)
{
    va_list ap;

    va_start(ap, format);
    vfprintf(stderr, format, ap);
    va_end(ap);

    exit(-1);
}

void FailNull(void * ptr, const char * format, ...)
{
    va_list ap;
    char    msg[256];
    
    if (ptr == NULL) {
        va_start(ap, format);
        vsnprintf(msg, sizeof(msg), format, ap);
        va_end(ap);
        Fail("NULL pointer: %s", msg);
    }
}



