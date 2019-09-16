# Usage:
# - Rscript ./path/to/rsem_to_dgelist.R \
#       --rsem <RSEM FILE> \
#       --gene-details <GENE_DETAILS TSV FILE>
#       --sample-details <SAMPLE DETAILS TSV FILE>
#       --out <OUTPUT .RData file>
#
# The row names in <RSEM FILE> should match the `gene_id` column in the <GENE
# DETAILS FILE>
#
# The column names in <RSEM FILE> should match the `sample_id` column in the
# <SAMPLE DETAILS FILE>
#
# The features in the output will be the intersection of the <RSEM FILE>
# rownames and the <GENE DETAILS...> `gene_id` column
#
# The samples in the output will be the intersection of the <RSEM FILE> column
# names and the <SAMPLE DETAILS> `sample_id` column
#
###############################################################################

suppressPackageStartupMessages({
  library(argparse)
  library(magrittr)
  library(stringr)
  library(Biobase)
  library(edgeR)
})

###############################################################################

format_names <- function(x) {
  x %>%
    stringr::str_replace_all(c("^\\W+" = "", "\\W+" = "_")) %>%
    tolower()
}

import_rsem <- function(path) {
  # read
  table <- as.matrix(read.csv(path, sep = "\t", row.names = 1))

  # format
  # - rownames should be ensembl IDs
  # - colnames are modified on import
  # - the values contained should be floored, so they can be used in edgeR /
  # voom etc
  colnames(table) <- format_names(colnames(table))
  table <- floor(table)

  table
}

import_genes <- function(path) {
  # import as tibble and convert to data.frame (pushing gene IDs into rownames)
  if(is.null(path)) {
    return(NULL)
  }

  genes <- readr::read_tsv(path)

  stopifnot("gene_id" %in% colnames(genes))
  if (any(duplicated(genes$gene_id))) {
    stop("duplicate gene IDs detected")
  }

  genes_df <- as.data.frame(
    genes, row.names = genes$gene_id, stringsAsFactors = FALSE
  )

  genes_df
}

import_samples <- function(path) {
  NULL
}

construct_dgelist <- function(counts, genes, samples) {
  reordered_genes <- if (is.null(genes)) {
    NULL
  } else {
    merge(
      data.frame(gene_id = row.names(counts), stringsAsFactors = FALSE),
      genes,
      all.x = TRUE
    ) %>%
    set_rownames(
      .$gene_id
    )
  }

  edgeR::DGEList(counts = counts, genes = reordered_genes)
}

###############################################################################

main <- function(rsem_path, genes_path, samples_path, out_path) {
  counts <- import_rsem(rsem_path)
  genes <- import_genes(genes_path)
  samples <- import_samples(samples_path)

  dge <- construct_dgelist(counts, genes, samples)

  saveRDS(dge, out_path)
}

###############################################################################

define_parser <- function() {
  parser <- ArgumentParser()
  parser$add_argument("--rsem", dest = "rsem_path")
  parser$add_argument("--genes", dest = "genes_path")
  parser$add_argument("--samples", dest = "samples_path")
  parser$add_argument("--out", dest = "out_path")
  parser
}

###############################################################################

parser <- define_parser()
args <- parser$parse_args()
do.call(main, args)

###############################################################################
