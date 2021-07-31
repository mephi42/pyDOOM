import contextlib
from libc.stdlib cimport free, malloc


cdef extern from "Python.h":
    char *PyUnicode_AsUTF8(object unicode)


cdef extern from "m_argv.h":
    int myargc
    char **myargv


cdef extern from "d_main.h":
    void D_DoomInit()
    void D_DoomLoopStep()
    void D_PostEvent(event_t *ev)


cpdef enum evtype_t: ev_keydown, ev_keyup, ev_mouse, ev_joystick


cdef extern from "d_event.h":
    ctypedef struct event_t:
        evtype_t type
        int data1
        int data2
        int data3


# doomdef.h
KEY_RIGHTARROW = 0xae
KEY_LEFTARROW = 0xac
KEY_UPARROW = 0xad
KEY_DOWNARROW = 0xaf
KEY_ESCAPE = 27
KEY_ENTER = 13
KEY_TAB = 9
KEY_F1 = 0x80 + 0x3b
KEY_F2 = 0x80 + 0x3c
KEY_F3 = 0x80 + 0x3d
KEY_F4 = 0x80 + 0x3e
KEY_F5 = 0x80 + 0x3f
KEY_F6 = 0x80 + 0x40
KEY_F7 = 0x80 + 0x41
KEY_F8 = 0x80 + 0x42
KEY_F9 = 0x80 + 0x43
KEY_F10 = 0x80 + 0x44
KEY_F11 = 0x80 + 0x57
KEY_F12 = 0x80 + 0x58
KEY_BACKSPACE = 127
KEY_PAUSE = 0xff
KEY_EQUALS = 0x3d
KEY_MINUS = 0x2d
KEY_RSHIFT = 0x80 + 0x36
KEY_RCTRL = 0x80 + 0x1d
KEY_RALT = 0x80 + 0x38
KEY_LALT = KEY_RALT


cdef extern from "v_video.h":
    extern unsigned char *screens[5]
    extern unsigned char gammatable[5][256]
    extern long usegamma


cdef extern unsigned char *current_palette

SCREENWIDTH = 320
SCREENHEIGHT = 200


@contextlib.contextmanager
def init(args):
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
        D_DoomInit()
        yield
    finally:
        myargc = 0
        free(myargv)
        myargv = NULL


cpdef step():
    D_DoomLoopStep()


cpdef post(type, data1, data2, data3):
    ev: event_t
    ev.type = type
    ev.data1 = data1
    ev.data2 = data2
    ev.data3 = data3
    D_PostEvent(&ev)


cpdef get_screen():
    return (<unsigned char[:SCREENHEIGHT, :SCREENWIDTH]>screens[0],
            <unsigned char[:256, :3]>current_palette,
            <unsigned char[:256]>gammatable[usegamma])
