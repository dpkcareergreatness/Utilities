#!/bin/bash
sync
echo "emergency reboot"
echo 1 > /proc/sys/kernel/sysrq
echo b > /proc/sysrq-trigger