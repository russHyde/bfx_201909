###############################################################################
# This script sets up the DESCRIPTION file for a basic devtools package
#
###############################################################################

library(devtools)
library(roxygen2) # only used to obtain current roxygen2 version

###############################################################################

check_package <- function(pkg_name) {
  print(paste("Checking package:", pkg_name))
  if (!require(pkg_name, character.only = TRUE)) {
    stop(
      paste("The following package is required, but not installed:", pkg_name)
    )
  }
}

###############################################################################
# These packages are required to build the job-specific R package

required_pkgs <- c("devtools", "testthat")

###############################################################################
# The user must provide the jobname prior to calling this, the constructed
#   package will be <jobname>.tar.gz
args <- commandArgs(trailingOnly = TRUE)

# args should contain [<jobname>, <filename>]
# - where jobname is a string (lacking '/' or whitespace)
# - and where filename is a file that exists and contains the names of all
#     R packages that are to be 'include'd by the job-specific package

if (length(args) == 0) {
  stop(paste0(
    "User should provide package-name and filename-of-imported-",
    "packages to setup.DESCRIPTION.R"
  ))
}

###############################################################################
# Extract the name of the package that is under construction (current_pkg) and
#   the name of the file that contains all the R-packages that are to be
#   imported during construction of this package from the command args
#
# Then check the validity of these arguments
#
current_pkg <- args[1]

file_of_imported_packages <- args[2]

if (grepl(pattern = "[[:space:]]", x = current_pkg) ||
  grepl(pattern = "\\/", x = current_pkg)
) {
  stop("The package name should contain no whitespace nor '/' characters")
}

if (!file.exists(file_of_imported_packages)) {
  stop("The filename-of-imported-packages should be an existing file")
}

###############################################################################
# - Obtain the list of packages that are to be imported
#
# - Check that each package that is required to be imported or is required to
# build the job-specific package is an installed R-package; die if any are not

import_pkgs <- scan(file_of_imported_packages, what = "character")

for (pkg in c(required_pkgs, import_pkgs)) {
  check_package(pkg)
}

###############################################################################
# Devtools description values for this package:

# - Building the package within R using devtools adds an Authors@R line to
# DESCRIPTION by default. This is obtained from options('devtools.desc.author')
# and seems to always be inserted.
# - To check the package using R CMD check, we require that both Author and
# Maintainer fields are specified in DESCRIPTION. These can be added
# automatically based on the Authors@R line of the DESCRIPTION by R CMD build,
# but I'd rather build the package using devtools (so that I can specify which
# directory the tarball gets put into, and prevent version numbers from being
# added to the name of the tarball).
# - The R docs say you shouldn't include both i) Authors@R, and ii) Author and
# Maintainer lines in your DESCRIPTION. This is false, you only need to ensure
# that Author/Maintainer/Authors@R fields are consistent.

options(
  devtools.desc.author =
    '"Russell Hyde <russell.hyde@glasgow.ac.uk> [aut, cre]"'
)

description <- list(
  "Author" = '"Russell Hyde" [aut, cre]',
  "Maintainer" = '"Russell Hyde" <russell.hyde@glasgow.ac.uk>',
  "Title" = paste0("R Package For The ", current_pkg, " Job"),
  "License" = "CC0",
  "RoxygenNote" = packageVersion("roxygen2")
)

###############################################################################
# Setup an initial package structure, with package name $current_pkg
#   if the directory structure doesn't already exist

if (!dir.exists(current_pkg)) {
  devtools::create(
    current_pkg,
    description = description
  )
}

###############################################################################
# Add all imported packages to the user-defined package
#   using devtools::use_package

for (ext_pkg in import_pkgs) {
  devtools::use_package(
    ext_pkg,
    type = "Imports",
    pkg = current_pkg
  )
}

###############################################################################
# Add testthat directories and functionality

devtools::use_testthat(current_pkg)

###############################################################################
