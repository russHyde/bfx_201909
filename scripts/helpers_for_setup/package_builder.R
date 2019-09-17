###############################################################################

library(desc)
library(devtools)

###############################################################################

get_output_path <- function(input_dir, output_dir) {
  library(desc)

  if(! dir.exists(input_dir)){
    stop(paste("Input directory:", input_dir, "should exist"))
  }
  if(! dir.exists(output_dir)){
    stop(paste("Output directory:", output_dir, "should exist"))
  }

  description_file <- file.path(input_dir, "DESCRIPTION")
  if(! file.exists(description_file)){
    stop(paste("File:", description_file, "should exist"))
  }

  # The description for the current package
  desc <- desc::description$new(source_dir)

  pkg_name <- desc$get("Package")
  pkg_version <- desc$get("Version")

  output_path <- file.path(
    output_dir,
    paste0(pkg_name, "_", pkg_version, ".tar.gz")
  )

  output_path
}

###############################################################################

has_been_updated <- function(input_dir, output_path) {
  # Check whether any files nested inside `input_dir` are more recent than
  # output_path
  stopifnot(dir.exists(input_dir))
  stopifnot(file.exists(output_path))

  sub_files <- dir(input_dir, full.names = TRUE, recursive = TRUE)

  most_recent_date <- max(file.mtime(sub_files))

  return(
    most_recent_date > file.mtime(output_path)
  )
}

###############################################################################
# SCRIPT
#
###############################################################################

args <- commandArgs(trailingOnly = TRUE)

source_dir <- args[1]

output_dir <- args[2]

output_path <- get_output_path(source_dir, output_dir)

should_build <- !file.exists(output_path) ||
  has_been_updated(source_dir, output_path)

if (should_build) {
  message(paste("Building package:", source_dir))
  devtools::build(pkg = source_dir, path = output_dir, vignettes = FALSE)
}

###############################################################################
