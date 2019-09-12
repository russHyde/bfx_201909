# We aren't using snakemake's remote providers to download the data here:
# - Building DAG of jobs is painfully slow when using FTPRemoteProvider() in
# smk 5.4, 5.5, 5.6 see snakemake issues #1275
# - Couldn't work out how to download an http query and then copy it to a
# location
# - Therefore, we wrote a script to download the files using bash

local_rsem = "data/ext/GSE103528_RSEM.gene.results.txt.gz"
local_gtf = "data/ext/Homo_sapiens.GRCh38.87.gtf.gz"
gene_details = "data/ext/Homo_sapiens.GRCh38.87.gene_details.tsv"

rule all:
    input:
        gene_details,
        local_rsem,
        local_gtf

rule get_gse103528:
    message:
        """
        --- Downloading {input} to {output}
        """

    output:
        local_rsem

    shell:
        """
            bash ./scripts/data_download.sh
        """

rule get_gtf:
    message:
        """
        --- Downloading {input} to {output}
        """

    output:
        local_gtf

    shell:
        """
            bash ./scripts/transcriptome_download.sh
        """

rule gene_details:
    message:
        """
        --- Extract gene annotations from {input}
        """

    input:
        "data/ext/{prefix}.gtf.gz"

    output:
        "data/ext/{prefix}.gene_details.tsv"

    shell:
        "Rscript ./scripts/ensembl_details.R --gtf {input} --out {output}"
