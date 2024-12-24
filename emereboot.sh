#!/bin/bash
sync
echo "emergency reboot"
#Enable Magic sysreq
echo 1 > /proc/sys/kernel/sysrq
#Reboot the system using the sysreq command
echo b > /proc/sysrq-trigger
