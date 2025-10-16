#ifndef _FAIL_
#define _FAIL_

/*  Written by Hugh Fisher. Distributed under MIT/X11 license */

#ifdef __cplusplus
extern "C" {
#endif

/* Report error and exit the program. To be implemented by main program */
void Fail(const char * format, ...);

/* Common test, report error if ptr is NULL */
void FailNull(void * ptr, const char * format, ...);

#ifdef __cplusplus
}
#endif

#endif
