// Emacs style mode select   -*- C++ -*- 
//-----------------------------------------------------------------------------
//
// $Id:$
//
// Copyright (C) 1993-1996 by id Software, Inc.
//
// This source is available for distribution and/or modification
// only under the terms of the DOOM Source Code License as
// published by id Software. All rights reserved.
//
// The source is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// FITNESS FOR A PARTICULAR PURPOSE. See the DOOM Source Code License
// for more details.
//
// $Log:$
//
// DESCRIPTION:
//	DOOM graphics stubs.
//
//-----------------------------------------------------------------------------

#include "v_video.h"

void I_ShutdownGraphics(void)
{
}

void I_StartFrame (void)
{
}

void I_StartTic (void)
{
}

void I_UpdateNoBlit (void)
{
}

void I_FinishUpdate (void)
{
}

void I_ReadScreen (byte* scr)
{
    memcpy (scr, screens[0], SCREENWIDTH*SCREENHEIGHT);
}

byte* current_palette;

void I_SetPalette (byte* palette)
{
    current_palette = palette;
}

void I_InitGraphics(void)
{
}
