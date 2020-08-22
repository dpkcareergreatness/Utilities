#!/bin/sh 
docker run \
-i -t \
-v /dir:/dir \
-v /opt/poky/2.4.3/:/opt/poky/2.4.3 \
--env-file env-setup.txt \
-w ~/root \
example:vm1
