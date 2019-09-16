# We aren't using snakemake's remote providers to download the data here:
# - Building DAG of jobs is painfully slow when using FTPRemoteProvider() in
# smk 5.4, 5.5, 5.6 see snakemake issues #1275
# - Couldn't work out how to download an http query and then copy it to a
# location
# - Therefore, we wrote a script to download the files using bash

###############################################################################

local_rsem = "data/ext/GSE103528_RSEM.gene.results.txt.gz"
ensembled_rsem = "data/ext/GSE103528_RSEM.gene.results.ensembl.tsv"
local_gtf = "data/ext/Homo_sapiens.GRCh38.87.gtf.gz"
gene_details = "data/ext/Homo_sapiens.GRCh38.87.gene_details.tsv"

dgelist = "data/job/GSE103528_RSEM.gene.results.ensembl.dgelist.rds"

###############################################################################

rule all:
    input:
        gene_details,
        ensembled_rsem,
        dgelist

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

rule reformat_gse103528:
    message:
        """
        --- Replace `ENSG00001234_<gene_symbol>` with `ENSG00001234` in the
            RSEM file
        """

    input:
        "data/ext/{prefix}.txt.gz"

    output:
        "data/ext/{prefix}.ensembl.tsv"

    shell:
        """
            cat {input} |\
            gunzip - |\
            perl -npe "s/(ENSG[0-9]{{11}})_(.*?)\\t/\$1\\t/" - \
            > {output}
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
        """
            Rscript ./scripts/ensembl_details.R --gtf {input} --out {output}
        """

rule make_dgelist:
    message:
        """
        --- Convert an RSEM dataset into an integer DGEList
        """

    input:
        tsv = "data/ext/{prefix}.ensembl.tsv",
        genes = "data/ext/Homo_sapiens.GRCh38.87.gene_details.tsv",
        script = "scripts/rsem_to_dgelist.R"

    output:
        "data/job/{prefix}.ensembl.dgelist.rds"

    shell:
        """
            Rscript {input.script} \
                --rsem {input.tsv} \
                --genes {input.genes} \
                --out {output}
        """
