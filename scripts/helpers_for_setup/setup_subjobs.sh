#!/bin/bash
set -e
set -u
set -o pipefail

###############################################################################
# 2017-08-29
#
# Script for recursively calling ./scripts/setup.sh for each subjob of the
# current job.
#
# TODO: generalise this so that it can run for any job
#
###############################################################################

die_and_moan()
{
  echo -e "$1" >&2
  exit 1
}

###############################################################################
# User can specify that there are no subjobs of the current job by either
# - ensuring that SUBJOBS_FILE is missing or empty
# - ensuring that SUBJOBS_FILE only contains comments or blank lines
# Note that 'not having a subjob' is not a failure case

if [[ -z "${SUBJOBS_FILE}" ]] || [[ ! -f "${SUBJOBS_FILE}" ]];
then
  echo "${0}: No subjobs defined" >&2
  exit
fi

###############################################################################
# For every non-comment / non-blank line in the SUBJOBS_FILE, assume that a
# subjob in ./subjobs/<subjob_name> exists and run it's setup-script

while read -r LINE;
do
  # Ignore blanks and
  # .. ignore lines if they start with '#' (ie, comment lines)
  if [[ -z "${LINE}" ]] || [[ "${LINE:0:1}" == "#" ]];
  then
    continue
  fi

  # Define path to subjob and check that subjob is defined
  SUBJOB_PATH="./subjobs/${LINE}"
  if [[ ! -d "${SUBJOB_PATH}" ]];
  then
    die_and_moan \
    "${0}: Subjob ${SUBJOB_PATH} should be defined before calling \
     \n setup_subjobs.sh with ${LINE} in ${SUBJOBS_FILE}"
  fi

  if [[ ! -f "${SUBJOB_PATH}/scripts/setup.sh" ]];
  then
    die_and_moan \
    "${0}: Subjob ${SUBJOB_PATH} should have a scripts/setup.sh defined"
  fi

  # Change dir into the subjob,
  #   run the setup scripts for the subjob,
  #   then move back into the original directory.

  # Since (...)-wrapping the code runs it in a subshell, we don't need to cd
  #   back into the original directory.

  (cd "${SUBJOB_PATH}" && ./sidekick setup)

done < "${SUBJOBS_FILE}"

###############################################################################
