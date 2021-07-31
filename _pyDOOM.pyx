from libc.stdlib cimport free, malloc


cdef extern from "Python.h":
    char* PyUnicode_AsUTF8(object unicode)


cdef extern from "m_argv.h":
    int myargc
    char **myargv


cdef extern from "d_main.h":
    void D_DoomMain()


cpdef long main(args):
    global myargc
    global myargv
    myargc = len(args)
    myargv = <char **>malloc((myargc + 1) * sizeof(char *))
    if not myargv:
        raise MemoryError()
    for i in range(myargc):
        myargv[i] = <char *>PyUnicode_AsUTF8(args[i])
    myargv[myargc] = NULL
    try:
        D_DoomMain()
    finally:
        myargc = 0
        free(myargv)
        myargv = NULL
