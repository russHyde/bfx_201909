###############################################################################
# 18/1/2017
# Makefile for generating R-function package for a general workjob
#
###############################################################################

# The user must specify a pkgname, or directly modify this file in a specific
#   job.
#
# This file should be placed in <JOB_NAME>/lib along with a copy of
#   default.setup.DESCRIPTION.R. This file should be renamed Makefile and the
#   latter should be renamed setup.DESCRIPTION.R
#
# The makefile constructs an R package <job.name>
#   that can be installed / imported into R and contains all the user-defined
#   functions for this project
#   - Typically job.name would be "do.some.work" if the job is called
#   "do_some_work"
#
# When called in ./lib for the current project,
#   it copies files into .lib/<job.name>/R/*.R from either
#   ./lib/global_rfuncs/*.R (which contains user-defined R functions used by
#                       several projects)
#   or ./lib/local_rfuncs/*.R (which contains any user-defined R functions that
#                       are specific to this project)
#
# It copies local test files into ./lib/<job.name>/tests/testthat/ from
#   ./lib/local_rfuncs/tests/testthat/test*.R and from
#   ./lib/global_rfuncs/tests/testthat/test*.R
#   and also copies in ./lib/local_rfuncs/tests/testthat.R (the
#   local-package-specific test runner)
#
# The contents of ./lib/<job.name>/ are packaged up into
#   ./lib/<job.name>.tar.gz which can then be install.packages()'d
#   - The latter is the preferred method for installing, since it is can be
#   used on windows, cygwin, linux and OSX
#
# Also, make should be called from within the directory ./lib

###############################################################################
SHELL=/bin/bash -o pipefail

# User must define pkgname at the commandline
pkgname:=

# Check that pkgname is set
ifndef pkgname
$(error pkgname for job-specific R package is not set)
endif

# Filename of
r_includes:=conf/include_into_rpackage.txt

# Check that r_includes is set
# - that $r_includes is a file is checked by the ${pkgname}/DESCRIPTION recipe
ifndef r_includes
$(error r_includes is not set)
endif

###############################################################################
# Source versions of the global and local r-function scripts and r-test files
#  that are to be incorporated into the R-package for the current project.
#
# Any files that are found in */tests/testthat are included, since the tests
# folder may include data and *.R scripts

rfiles:=${wildcard global_rfuncs/R/*.R} \
        ${wildcard local_rfuncs/R/*.R}

rtestfiles:=${wildcard global_rfuncs/tests/testthat/*} \
            ${wildcard local_rfuncs/tests/testthat/*}

# File locations of the r-function and r-test scripts that are used in the
#   work package

pkg_rfiles=${addprefix ${pkgname}/R/, \
             ${notdir ${rfiles}} \
             }

pkg_rtestfiles=${addprefix ${pkgname}/tests/testthat/, \
                 ${notdir ${rtestfiles}} \
                 }


###############################################################################
all: built_packages/${pkgname}_0.0.0.9000.tar.gz

# Set up default package structure
#   and add default tests/ and tests/testthat.R to it

# Set up the DESCRIPTION file for the current job's work package
# Have modified setup.DESCRIPTION.R to also add the tests/testthat subdirs
# TODO: add authorship etc
${pkgname}/DESCRIPTION \
${pkgname}/tests/testthat.R: \
		setup.DESCRIPTION.R \
		${r_includes}
	if [[ -f "${pkgname}/DESCRIPTION" ]]; then rm -R "${pkgname}"; fi
	Rscript setup.DESCRIPTION.R \
		${pkgname} \
		${r_includes}

# Copy my own written functions into the job's R package
${pkgname}/%: \
		global_rfuncs/% \
		${pkgname}/DESCRIPTION \
		${pkgname}/tests/testthat.R
	cp $< $@

${pkgname}/%: \
		local_rfuncs/% \
		${pkgname}/DESCRIPTION \
		${pkgname}/tests/testthat.R
	cp $< $@

# Build the archive for the current job's R package
built_packages/${pkgname}_0.0.0.9000.tar.gz: \
		${pkgname}/DESCRIPTION \
		${pkgname}/tests/testthat.R \
		${pkg_rfiles} \
		${pkg_rtestfiles}
	Rscript -e 'library(devtools); library(methods);' \
                -e 'setwd("${pkgname}");' \
                -e 'document();' \
                -e 'dir.create("../built_packages", showWarnings = FALSE);' \
                -e 'devtools::build(path = "../built_packages")'

###############################################################################
