#!/bin/bash
set -e
set -u
set -o pipefail

# If the current project uses R within jupyter:
# - Ensure an R kernel can be accessed by `jupyter nbconvert` and within
# `jupyter` by adding `R_KERNEL` to the `kernelspec` list
#
if [[ ${IS_JUPYTER_R_REQUIRED} -ne 0 ]];
then
  if [[ -z "${R_KERNEL}" ]];
  then
    die_and_moan \
    "${0}: 'R_KERNEL' name should be defined in '${JOB_VARS_FILE}'"
  fi
  # check if the current kernel name is present in the list of available
  #  r-kernels for jupyter:
  # The final ` || : ` step prevents an empty grep-return-value from killing
  # the script; we do this since CHECK_KERNELS is subsequently double checked
  # for exact matching against the name of R_KERNEL
  CHECK_KERNELS=$( jupyter kernelspec list |\
                   cut -d" " -f3 |\
                   grep -e "${R_KERNEL}" - ) || :
  if [[ "${CHECK_KERNELS}" == "${R_KERNEL}" ]];
  then
    echo "${0}: Kernel '${R_KERNEL}' is already available" >&2
  else
    echo "${0}: Adding Kernel '${R_KERNEL}'" >&2
    Rscript \
      -e "kern_name = commandArgs(trailingOnly = TRUE)[1];" \
      -e "library(IRkernel);" \
      -e "IRkernel::installspec(name = kern_name, displayname = kern_name);" \
       "${R_KERNEL}"
  fi
fi
