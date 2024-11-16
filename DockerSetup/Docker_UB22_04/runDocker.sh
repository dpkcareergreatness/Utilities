#!/bin/bash

# =============================================================
# build env settings
BUILDDIR_INNO="innogpu"
BUILDDIR_NOHW="nohw_linux"
BUILDDIR_FPGA="fpga_linux"

ENVFILE_NOHW="./env-setup-nohw.txt"
ENVFILE_INNO="./env-setup-inno.txt"
ENVFILE_FPGA="./env-setup-fpga.txt"

DOCKER_IMAGE="dockertag:auto_tester"
# =============================================================

BUILDDIR=""
ENVFILE=""
SOURCE=""
OUTPUT=""

USAGE="$0 --[nohw | inno| fpga] --src=<Path to DDK src code>"

for arg in $*; do
    case "$arg" in
        --fpga) {
                    ENVFILE=$ENVFILE_FPGA
                    BUILDDIR=$BUILDDIR_FPGA
                    OUTPUT=$PWD/output-fpga
                };;
        --nohw) {
                    ENVFILE=$ENVFILE_NOHW
                    BUILDDIR=$BUILDDIR_NOHW
                    OUTPUT=$PWD/output-nohw
                };;
        --inno) {
                    ENVFILE=$ENVFILE_INNO
                    BUILDDIR=$BUILDDIR_INNO
                    OUTPUT=$PWD/output-inno
                };;
        --src=*)  {
                    SOURCE=$(echo "$arg" | awk -F= '{print $2}')
                };;
        *     )
                echo "Invalid command: $arg"
                echo $USAGE
                exit 1;;
    esac
done

if  [ -z $BUILDDIR ] ||
    [ -z $ENVFILE ] ||
    [ -z $DOCKER_IMAGE ] ||
    [ -z $SOURCE ];
then
    echo $USAGE
    exit 1
fi

# =============================================================

echo Using source directory $SOURCE
echo Using output directory $OUTPUT

echo Using build directory $BUILDDIR
echo Using env-file $ENVFILE
echo Using Docker Image $DOCKER_IMAGE

docker run \
--rm \
-i -t \
-v $SOURCE:/ddk \
-v $OUTPUT:/output \
--env-file ${ENVFILE} \
-w ${BUILDDIR} \
$DOCKER_IMAGE
