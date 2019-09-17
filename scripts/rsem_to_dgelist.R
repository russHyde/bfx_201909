# Usage:
# - Rscript ./path/to/rsem_to_dgelist.R \
#       --rsem <RSEM FILE> \
#       --genes <GENE_DETAILS TSV FILE>
#       --samples <SAMPLE DETAILS TSV FILE>
#       --out <OUTPUT .rds file>
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
# Dependencies:

suppressPackageStartupMessages({
  library(argparse)
  library(magrittr)
  library(readr)

  library(Biobase)
  library(edgeR)
})

###############################################################################

helper_path <- file.path("scripts", "lib", "helpers.R")
source(helper_path)

###############################################################################

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
  samples <- readr::read_tsv(path)

  as.data.frame(
    samples, row.names = samples$sample_id, stringsAsFactors = FALSE
  )
}

construct_dgelist <- function(counts, genes, samples) {
  reordered_genes <- if (is.null(genes)) {
    NULL
  } else {
    rownames(genes) <- genes$gene_id
    genes[match(rownames(counts), genes$gene_id), ]
  }

  reordered_samples <- if (is.null(samples)) {
    NULL
  } else {
    rownames(samples) <- samples$sample_id
    samples[match(colnames(counts), samples$sample_id), ]
  }

  edgeR::DGEList(
    counts = counts,
    genes = reordered_genes,
    samples = reordered_samples
  )
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
