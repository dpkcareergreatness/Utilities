# Docker setup
This provides basic docker environment setup for ubuntu.

## Prerequisite

Install docker

https://www.docker.com/

## Setting up docker env

1. First build the docker image. For this edit the Dockerfile with the required packages
2. Then run build.sh
3. Now edit the run.sh to change your volumes mounted (-v), startup directory (-w)
4. It will now run the script and change the current directory to the one mentioned by -w
