#!/bin/bash
dpkg-reconfigure locales
echo "Intall en_US.UTF-8 package"
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
export LANGUAGE=en_US.UTF-8
