@echo off
REM Set the compatibility layer to RunAsInvoker to run the program with the same privileges as the parent process
set __COMPAT_LAYER=RunAsInvoker

REM Start the specified program
start %1

