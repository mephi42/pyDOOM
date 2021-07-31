cmake_minimum_required(VERSION 3.3)
project(_pyDOOM)
find_package(PythonExtensions REQUIRED)
find_package(Cython REQUIRED)
set(SRCDIR ${CMAKE_CURRENT_SOURCE_DIR}/linuxdoom-1.10)
set(SRCS
        ${SRCDIR}/doomdef.c
        ${SRCDIR}/doomstat.c
        ${SRCDIR}/dstrings.c
        ${SRCDIR}/i_system.c
        ${SRCDIR}/i_sound.c
        ${SRCDIR}/i_video.c
        ${SRCDIR}/i_net.c
        ${SRCDIR}/tables.c
        ${SRCDIR}/f_finale.c
        ${SRCDIR}/f_wipe.c
        ${SRCDIR}/d_main.c
        ${SRCDIR}/d_net.c
        ${SRCDIR}/d_items.c
        ${SRCDIR}/g_game.c
        ${SRCDIR}/m_menu.c
        ${SRCDIR}/m_misc.c
        ${SRCDIR}/m_argv.c
        ${SRCDIR}/m_bbox.c
        ${SRCDIR}/m_fixed.c
        ${SRCDIR}/m_swap.c
        ${SRCDIR}/m_cheat.c
        ${SRCDIR}/m_random.c
        ${SRCDIR}/am_map.c
        ${SRCDIR}/p_ceilng.c
        ${SRCDIR}/p_doors.c
        ${SRCDIR}/p_enemy.c
        ${SRCDIR}/p_floor.c
        ${SRCDIR}/p_inter.c
        ${SRCDIR}/p_lights.c
        ${SRCDIR}/p_map.c
        ${SRCDIR}/p_maputl.c
        ${SRCDIR}/p_plats.c
        ${SRCDIR}/p_pspr.c
        ${SRCDIR}/p_setup.c
        ${SRCDIR}/p_sight.c
        ${SRCDIR}/p_spec.c
        ${SRCDIR}/p_switch.c
        ${SRCDIR}/p_mobj.c
        ${SRCDIR}/p_telept.c
        ${SRCDIR}/p_tick.c
        ${SRCDIR}/p_saveg.c
        ${SRCDIR}/p_user.c
        ${SRCDIR}/r_bsp.c
        ${SRCDIR}/r_data.c
        ${SRCDIR}/r_draw.c
        ${SRCDIR}/r_main.c
        ${SRCDIR}/r_plane.c
        ${SRCDIR}/r_segs.c
        ${SRCDIR}/r_sky.c
        ${SRCDIR}/r_things.c
        ${SRCDIR}/w_wad.c
        ${SRCDIR}/wi_stuff.c
        ${SRCDIR}/v_video.c
        ${SRCDIR}/st_lib.c
        ${SRCDIR}/st_stuff.c
        ${SRCDIR}/hu_stuff.c
        ${SRCDIR}/hu_lib.c
        ${SRCDIR}/s_sound.c
        ${SRCDIR}/z_zone.c
        ${SRCDIR}/info.c
        ${SRCDIR}/sounds.c
)
add_cython_target(_pyDOOM C)
set_source_files_properties(${_pyDOOM} PROPERTIES
        INCLUDE_DIRECTORIES ${SRCDIR}
)
add_library(_pyDOOM MODULE ${SRCS} ${_pyDOOM})
target_compile_options(_pyDOOM PRIVATE
        -Wall
        -Werror
        -Wno-maybe-uninitialized
        -Wno-unused-result
)
target_compile_definitions(_pyDOOM PRIVATE NORMALUNIX LINUX)
target_link_libraries(_pyDOOM Xext X11 nsl m)
python_extension_module(_pyDOOM)
install(TARGETS _pyDOOM LIBRARY DESTINATION _pyDOOM)
