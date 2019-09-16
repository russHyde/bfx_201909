###############################################################################
# Dependencies:

suppressPackageStartupMessages({
  library(argparse)
  library(magrittr)
  library(readr)
  library(tidyr)
})

helper_path <- file.path("scripts", "lib", "helpers.R")
stopifnot(file.exists(helper_path))
source(helper_path)

###############################################################################

parse_sample_data <- function(rsem) {
  samples <- colnames(rsem)

  # In the formatted RSEM derived from GSE103528, the cell-line, treatment and
  # batch are encoded as "_"-separated parts of the column names.

  data.frame(
    sample_id = samples,
    stringsAsFactors = FALSE
  ) %>%
    tidyr::separate(
      sample_id, c("cell", "treatment", "batch"), sep = "_", remove = FALSE
    ) %>%
    magrittr::set_rownames(.$sample_id)
}

###############################################################################

main <- function(rsem_path, out_path) {
  # extract sample IDs from first line of the RSEM file
  # extract cell-line, treatment, batch from the sample IDs
  # return a data.frame, indexed by sample ID

  rsem <- import_rsem(rsem_path)
  sample_df <- parse_sample_data(rsem)

  readr::write_tsv(sample_df, path = out_path)
}

###############################################################################

define_parser <- function() {
  parser <- ArgumentParser()
  parser$add_argument("--rsem", dest = "rsem_path")
  parser$add_argument("--out", dest = "out_path")
  parser
}

###############################################################################

parser <- define_parser()
args <- parser$parse_args()
do.call(main, args)

###############################################################################
