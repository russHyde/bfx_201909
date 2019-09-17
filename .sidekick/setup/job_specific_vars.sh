#!/bin/bash -e

###############################################################################
# User-specified variables for use in the `bfx_201909`
# project

###############################################################################
# `JOBNAME` and `IS_R_REQUIRED` must be defined for each new project
#
# `IS_R_REQUIRED=1` if R is to be used in addition to pythono within the current
# project
# `IS_R_PKG_REQUIRED=1` is required if an R package is to be made
# `IS_JUPYTER_R_REQUIRED=1` is required if an R kernel is to be made

export JOBNAME="bfx_201909"
export IS_R_REQUIRED=1
export IS_R_PKG_REQUIRED=1
export IS_JUPYTER_R_REQUIRED=0

###############################################################################
# PKGNAME is the name of the job-specific R package
# - Note that the R-package <PKGNAME> will only be built/installed if the user
#   adds some files to the subdirectories ./lib/local_rfuncs/R or
#   ./lib/global_rfuncs
# - The R_INCLUDES_FILE defines which external R packages are 'include'd by the
#   job-specific package

if [[ ! -z "${IS_R_PKG_REQUIRED}" ]] && [[ ${IS_R_PKG_REQUIRED} -ne 0 ]];
then
  export PKGNAME="bfx.201909"
  export R_INCLUDES_FILE="${PWD}/lib/conf/include_into_rpackage.txt"
fi

# ENVNAME is the name of the job-specific conda environment
export ENVNAME="bfx_201909"

###############################################################################
if [[ ! -z "${IS_JUPYTER_R_REQUIRED}" ]] && [[ ${IS_JUPYTER_R_REQUIRED} -ne 0 ]];
then
  export R_KERNEL="conda-env-${ENVNAME}-r"
fi
