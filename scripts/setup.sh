#!/bin/bash
set -e
set -u
set -o pipefail

###############################################################################

echo  -e "\nJOB: ${PWD}" >&2
echo  -e "${0}: Running the work-package setup-script." >&2

###############################################################################

die_and_moan()
{
  echo -e "$1" >&2
  exit 1
}

##############################################################################
# Each of the following files / directories should be defined before running
# this script.
# - They will typically be initialised using `cookiecutter`

export CONFIG_DIR="./.sidekick/setup"
export SCRIPT_DIR="./scripts"
export LIB_DIR="./lib"
export BIN_DIR="./bin"

export JOB_VARS_FILE="${CONFIG_DIR}/job_specific_vars.sh"
export CHECK_DIRS_FILE="${CONFIG_DIR}/check_these_dirs.yaml"
export MAKE_DIRS_FILE="${CONFIG_DIR}/make_these_subdirs.txt"
export MAKE_LINKS_FILE="${CONFIG_DIR}/make_these_links.txt"
export MAKE_FILE_COPIES_FILE="${CONFIG_DIR}/copy_these_files.txt"
export MAKE_DIR_COPIES_FILE="${CONFIG_DIR}/copy_these_dirs.txt"
export REPO_CLONING_CONFIG="${CONFIG_DIR}/clone_these_repos.yaml"
export TOUCH_FILES_FILE="${CONFIG_DIR}/touch_these_files.txt"
export SUBJOBS_FILE="${CONFIG_DIR}/subjob_names.txt"

export SETUP_HELPERS_DIR="${SCRIPT_DIR}/helpers_for_setup"
export BUDDY_PY="${BIN_DIR}/buddy"

###############################################################################
# - Setup / check variable definitions
#   - The file `./.sidekick/setup/job_specific_vars.sh` should exist and
#   contain the definitions of all job-specific variables;
#   - All setup-related files require that `JOBNAME`, `ENVNAME` and
#   `IS_R_REQUIRED` are defined;
#   - If `IS_R_PKG_REQUIRED` is 1, `PKGNAME` should be defined;
#   - If `IS_JUPYTER_R_REQUIRED` is 1, `R_KERNEL` should be defined;
#   - `PKGNAME` is checked within `setup_libs.sh`;
#   - `ENVNAME` should be defined in `job_specific_vars.sh` and is checked by
#   `check_env.sh`

if [[ ! -f "${JOB_VARS_FILE}" ]];
then
  die_and_moan \
  "${0}: File '${JOB_VARS_FILE}' should be defined"
fi

source "${JOB_VARS_FILE}"

if [[ -z "${JOBNAME}" ]];
then
  die_and_moan \
  "${0}: Variable 'JOBNAME' should be defined in '${JOB_VARS_FILE}'"
fi

if [[ -z "${ENVNAME}" ]];
then
  die_and_moan \
  "${0}: Variable 'ENVNAME' (giving the name of the 'conda' environment for \
  \n ... the current job) should be defined in '${JOB_VARS_FILE}'"
fi

if [[ -z "${IS_R_REQUIRED}" ]] && \
   [[ ${IS_R_REQUIRED} -ne 0 ]] && \
   [[ ${IS_R_REQUIRED} -ne 1 ]];
then
  die_and_moan \
  "${0}: Binary variable 'IS_R_REQUIRED' should be defined in '${JOB_VARS_FILE}'"
fi

###############################################################################
# - Job should only be ran on Linux or Mac
#
if [[ "${OSTYPE}" != "linux-gnu" ]] && [[ "${OSTYPE}" != darwin* ]];
then
  die_and_moan \
  "${0}: 'OSTYPE' should be 'linux-gnu' or darwin*"
fi

###############################################################################
# - Ensure that <ENVNAME> is the name of the current env

if [[ -z "${CONDA_PREFIX}" ]] || \
   [[ -z "${CONDA_DEFAULT_ENV}" ]]; then
  die_and_moan \
  "${0}: 'CONDA_PREFIX' or 'CONDA_DEFAULT_ENV' are undefined \
  \n -- perhaps you haven't activated the work-package's 'conda' env?"
  fi

if [[ "${ENVNAME}" != "${CONDA_DEFAULT_ENV}" ]]; then
  die_and_moan \
  "${0}: 'conda' env '${ENVNAME}' is not activated"
  fi

###############################################################################
# - If the `buddy` python package has not previously been installed, install it
#
# TODO: ensure files in BUDDY_PY are newer than ${CONDA_PREFIX}/lib/buddy
#
if $(conda list | grep -qe "^buddy\\b"); then
  echo "${0}: 'buddy' has already been installed" >&2
else
  if [[ ! -d "${BUDDY_PY}" ]]
  then
    die_and_moan \
    "${0}: '${BUDDY_PY}' is not a directory: \
    \n ... Cannot install the project-setup helper scripts"
  fi

  pip install -e "${BUDDY_PY}"
fi

###############################################################################
# - Ensure that python / Rscript are ran from $CONDA_PREFIX/bin/

python "${BUDDY_PY}/buddy/validate_env_contents.py" \
  "${CONDA_PREFIX}" \
  "${IS_R_REQUIRED}"

###############################################################################
# - If the user plans to use R within jupyter, ensure an R kernel is available

JUPYTER_KERNEL_SCRIPT="${SETUP_HELPERS_DIR}/setup_jupyter_r_kernel.sh"
if [[ ! -f "${JUPYTER_KERNEL_SCRIPT}" ]];
then
  die_and_moan \
  "${0}: '${JUPYTER_KERNEL_SCRIPT}' should exist"
fi

if [[ ${IS_JUPYTER_R_REQUIRED} -ne 0 ]];
then
  bash "${JUPYTER_KERNEL_SCRIPT}"
fi

###############################################################################
# - Check that
#   - all internal directories/files are present (and make them if not);
#   - all necessary external directories are present;
#   - all links to / copies of external datafiles/scripts are set up.
# - This includes any R function scripts that are hard-copied into this job
#

DIRS_SCRIPT="${SETUP_HELPERS_DIR}/setup_dirs.sh"
if [[ ! -f "${DIRS_SCRIPT}" ]];
then
  die_and_moan \
  "${0}: '${DIRS_SCRIPT}' should exist"
fi

bash "${DIRS_SCRIPT}"

###############################################################################
# - Construct the R package for this job
#
PKGS_SCRIPT="${SETUP_HELPERS_DIR}/setup_libs.sh"
if [[ ! -f "${PKGS_SCRIPT}" ]];
then
  die_and_moan \
  "${0}: '${PKGS_SCRIPT}' should exist"
fi

bash "${PKGS_SCRIPT}"

###############################################################################
# - Setup all subjobs for this job
# - It is not an error if the `setup_subjobs.sh` script is missing
SUBJOB_SCRIPT="${SETUP_HELPERS_DIR}/setup_subjobs.sh"
if [[ ! -f "${SUBJOB_SCRIPT}" ]];
then
  echo "${0}: No subjob-definition script is available for '${PWD}'" >&2
else
  bash "${SUBJOB_SCRIPT}"
fi

###############################################################################
