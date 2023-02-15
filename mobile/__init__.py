#!/usr/bin/python3
import os
os.environ['SDL_VIDEO_X11_WMCLASS'] = 'float'

print('main mobile')
import weekplanner.mobile.src.app
