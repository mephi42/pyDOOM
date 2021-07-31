import ctypes
import numpy as np
import sdl2
import sdl2.ext

import _pyDOOM

XLATEKEY = {
    sdl2.SDLK_LEFT: _pyDOOM.KEY_LEFTARROW,
    sdl2.SDLK_RIGHT: _pyDOOM.KEY_RIGHTARROW,
    sdl2.SDLK_DOWN: _pyDOOM.KEY_DOWNARROW,
    sdl2.SDLK_UP: _pyDOOM.KEY_UPARROW,
    sdl2.SDLK_ESCAPE: _pyDOOM.KEY_ESCAPE,
    sdl2.SDLK_RETURN: _pyDOOM.KEY_ENTER,
    sdl2.SDLK_TAB: _pyDOOM.KEY_TAB,
    sdl2.SDLK_F1: _pyDOOM.KEY_F1,
    sdl2.SDLK_F2: _pyDOOM.KEY_F2,
    sdl2.SDLK_F3: _pyDOOM.KEY_F3,
    sdl2.SDLK_F4: _pyDOOM.KEY_F4,
    sdl2.SDLK_F5: _pyDOOM.KEY_F5,
    sdl2.SDLK_F6: _pyDOOM.KEY_F6,
    sdl2.SDLK_F7: _pyDOOM.KEY_F7,
    sdl2.SDLK_F8: _pyDOOM.KEY_F8,
    sdl2.SDLK_F9: _pyDOOM.KEY_F9,
    sdl2.SDLK_F10: _pyDOOM.KEY_F10,
    sdl2.SDLK_F11: _pyDOOM.KEY_F11,
    sdl2.SDLK_F12: _pyDOOM.KEY_F12,
    sdl2.SDLK_BACKSPACE: _pyDOOM.KEY_BACKSPACE,
    sdl2.SDLK_DELETE: _pyDOOM.KEY_BACKSPACE,
    sdl2.SDLK_PAUSE: _pyDOOM.KEY_PAUSE,
    sdl2.SDLK_EQUALS: _pyDOOM.KEY_EQUALS,
    sdl2.SDLK_KP_EQUALS: _pyDOOM.KEY_EQUALS,
    sdl2.SDLK_MINUS: _pyDOOM.KEY_MINUS,
    sdl2.SDLK_KP_MINUS: _pyDOOM.KEY_MINUS,
    sdl2.SDLK_LSHIFT: _pyDOOM.KEY_RSHIFT,
    sdl2.SDLK_RSHIFT: _pyDOOM.KEY_RSHIFT,
    sdl2.SDLK_LCTRL: _pyDOOM.KEY_RCTRL,
    sdl2.SDLK_RCTRL: _pyDOOM.KEY_RCTRL,
    sdl2.SDLK_LALT: _pyDOOM.KEY_RALT,
    sdl2.SDLK_RALT: _pyDOOM.KEY_RALT,
    sdl2.SDLK_LGUI: _pyDOOM.KEY_RALT,
    sdl2.SDLK_RGUI: _pyDOOM.KEY_RALT,
}


def xlatekey(keysym):
    result = XLATEKEY.get(keysym.sym)
    if result is not None:
        return result
    if sdl2.SDLK_SPACE <= keysym.sym <= sdl2.SDLK_BACKQUOTE:
        return keysym.sym - sdl2.SDLK_SPACE + ord(" ")
    if sdl2.SDLK_a <= keysym.sym <= sdl2.SDLK_z:
        return keysym.sym - sdl2.SDLK_a + ord("a")
    return keysym.sym


def get_screen():
    screen, palette, gamma = _pyDOOM.get_screen()
    screen = np.array(screen, dtype=np.uint8).T
    palette = np.array(palette, dtype=np.uint8)
    gamma = np.array(gamma, dtype=np.uint8)
    return gamma[palette[screen]][:, :, ::-1]


BUTTON_MASKS = {
    sdl2.SDL_BUTTON_LEFT: 1,
    sdl2.SDL_BUTTON_MIDDLE: 2,
    sdl2.SDL_BUTTON_RIGHT: 4,
}


def play(args):
    sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO)
    try:
        factor = 4
        window = sdl2.SDL_CreateWindow(
            b"pyDOOM",
            sdl2.SDL_WINDOWPOS_CENTERED,
            sdl2.SDL_WINDOWPOS_CENTERED,
            _pyDOOM.SCREENWIDTH * factor,
            _pyDOOM.SCREENHEIGHT * factor,
            sdl2.SDL_WINDOW_SHOWN,
        )
        sdl2.SDL_SetWindowGrab(window, sdl2.SDL_TRUE)
        sdl2.SDL_ShowCursor(sdl2.SDL_DISABLE)
        try:
            event = sdl2.SDL_Event()
            with _pyDOOM.init(args):
                proceed = True
                mouse_state = 0
                mouse_x = 0
                mouse_y = 0
                while proceed:
                    _pyDOOM.step()
                    surface = sdl2.SDL_GetWindowSurface(window)
                    surface_array = sdl2.ext.pixels3d(surface.contents)
                    np.copyto(
                        surface_array[:, :, :3],
                        np.repeat(np.repeat(get_screen(), factor, 0), factor, 1),
                    )
                    sdl2.SDL_UpdateWindowSurface(window)
                    while sdl2.SDL_PollEvent(ctypes.byref(event)) != 0:
                        if event.type == sdl2.SDL_KEYDOWN:
                            _pyDOOM.post(
                                _pyDOOM.ev_keydown, xlatekey(event.key.keysym), 0, 0
                            )
                        elif event.type == sdl2.SDL_KEYUP:
                            _pyDOOM.post(
                                _pyDOOM.ev_keyup, xlatekey(event.key.keysym), 0, 0
                            )
                        elif event.type == sdl2.SDL_MOUSEBUTTONDOWN:
                            mouse_state |= BUTTON_MASKS[event.button.button]
                            _pyDOOM.post(_pyDOOM.ev_mouse, mouse_state, 0, 0)
                        elif event.type == sdl2.SDL_MOUSEBUTTONUP:
                            mouse_state &= ~BUTTON_MASKS[event.button.button]
                            _pyDOOM.post(_pyDOOM.ev_mouse, mouse_state, 0, 0)
                        elif event.type == sdl2.SDL_MOUSEMOTION:
                            data2 = (mouse_x - event.motion.x) << 2
                            data3 = (mouse_y - event.motion.y) << 2
                            if data2 != 0 or data3 != 0:
                                mouse_x = event.motion.x
                                mouse_y = event.motion.y
                                if (
                                    event.motion.x != surface_array.shape[0] // 2
                                    and event.motion.y != surface_array.shape[1] // 2
                                ):
                                    _pyDOOM.post(
                                        _pyDOOM.ev_mouse, mouse_state, data2, data3
                                    )
                        elif event.type == sdl2.SDL_QUIT:
                            proceed = False
                            break
                    sdl2.SDL_WarpMouseInWindow(
                        window, surface_array.shape[0] // 2, surface_array.shape[1] // 2
                    )
        finally:
            sdl2.SDL_DestroyWindow(window)
    finally:
        sdl2.SDL_Quit()
