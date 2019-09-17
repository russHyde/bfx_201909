
###############################################################################

#' format_sample_names
#'
#' @importFrom   magrittr   %>%
#' @importFrom   stringr    str_replace_all
#'
#' @export

format_sample_names <- function(x) {
  x %>%
    stringr::str_replace_all(c("^\\W+" = "", "\\W+" = "_")) %>%
    tolower()
}

###############################################################################

#' import_rsem
#'
#' @export

import_rsem <- function(path) {
  # read
  table <- as.matrix(read.csv(path, sep = "\t", row.names = 1))

  # format
  # - rownames should be ensembl IDs
  # - colnames are modified on import
  # - the values contained should be floored, so they can be used in edgeR /
  # voom etc
  colnames(table) <- format_sample_names(colnames(table))
  table <- floor(table)

  table
}

###############################################################################
