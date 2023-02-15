#!/usr/bin/python3
from sys import argv

if 'm' in argv or 'mobile' in argv:
    import weekplanner.mobile
else:
    import weekplanner.cli.app
