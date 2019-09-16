suppressPackageStartupMessages({
  library(magrittr)
  library(readr)
  library(rtracklayer)
  library(argparse)
})

###############################################################################

# copied from snakemake r script: `get_ensembl_gene_details.smk.R` in
# `rnaseq_workflow`

parse_gtf <- function(gtf_path){
  stopifnot(file.exists(gtf_path))
  gtf <- rtracklayer::import(gtf_path)
}

get_genes_from_gtf <- function(gtf){
  gtf[which(gtf$type == "gene"), ]
}

get_gene_df_from_gtf <- function(gtf_path, reqd_columns){
  gene_df <- gtf_path %>%
    parse_gtf() %>%
    get_genes_from_gtf() %>%
    as.data.frame()

  gene_df[, reqd_columns]
}

###############################################################################

main <- function(gtf_path, out_path) {
  gtf_columns <- paste(
    "gene", c("id", "version", "name", "source", "biotype"), sep = "_"
  )

  results <- get_gene_df_from_gtf(gtf_path, gtf_columns)

  readr::write_tsv(results, path = out_path)
}

###############################################################################

define_parser <- function() {
  parser <- argparse::ArgumentParser()
  parser$add_argument("--gtf", dest = "gtf_path")
  parser$add_argument("-o", "--out", dest = "out_path")
  parser
}

###############################################################################

parser <- define_parser()
args <- parser$parse_args()

main(gtf_path = args$gtf_path, out_path = args$out_path)

###############################################################################
