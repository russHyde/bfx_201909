# We aren't using snakemake's remote providers to download the data here:
# - Building DAG of jobs is painfully slow when using FTPRemoteProvider() in
# smk 5.4, 5.5, 5.6 see snakemake issues #1275
# - Couldn't work out how to download an http query and then copy it to a
# location
# - Therefore, we wrote a script to download the files using bash

from snakemake.remote.HTTP import RemoteProvider as HTTPRemoteProvider

http = HTTPRemoteProvider()

###############################################################################

local_rsem = "data/ext/GSE103528_RSEM.gene.results.txt.gz"
ensembled_rsem = "data/ext/GSE103528_RSEM.gene.results.ensembl.tsv"
local_gtf = "data/ext/Homo_sapiens.GRCh38.87.gtf.gz"
gene_details = "data/ext/Homo_sapiens.GRCh38.87.gene_details.tsv"

sample_details = "data/job/GSE103528.samples.tsv"
dgelist = "data/job/GSE103528.dgelist.rds"

html_report = "doc/stats_and_bfx.html"

###############################################################################

figures = {
    "Relationships_among_some_of_univariate_probability_distributions.jpg" : \
        "upload.wikimedia.org/wikipedia/commons/6/69/Relationships_among_some_of_univariate_probability_distributions.jpg",
    "gkv007fig1.jpg" : \
        "www.ncbi.nlm.nih.gov/pmc/articles/PMC4402510/bin/gkv007fig1.jpg"
}

def get_figure_url(wildcards):
    return http.remote(figures[wildcards["suffix"]], keep_local=True)

###############################################################################

rule all:
    input:
        gene_details,
        ensembled_rsem,
        sample_details,
        dgelist,
        html_report

rule download_figure:
    input:
        get_figure_url

    output:
        "figures/{suffix}"

    shell:
        """
            mv {input} {output}
        """

rule get_gse103528:
    message:
        """
        --- Downloading {input} to {output}
        """

    output:
        local_rsem

    shell:
        """
            bash ./scripts/GSE103528/data_download.sh
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

rule sample_details:
    message:
        """
        --- Extract sample/treatment data from {input}
        """

    input:
        tsv = "data/ext/{gse_id}_RSEM.gene.results.ensembl.tsv",
        script = "scripts/{gse_id}/rsem_to_samples.R"

    output:
        "data/job/{gse_id}.samples.tsv"

    shell:
        """
            Rscript {input.script} --rsem {input.tsv} --out {output}
        """

rule make_dgelist:
    message:
        """
        --- Convert an RSEM dataset into an integer DGEList
        """

    input:
        tsv = "data/ext/{gse_id}_RSEM.gene.results.ensembl.tsv",
        genes = "data/ext/Homo_sapiens.GRCh38.87.gene_details.tsv",
        samples = "data/job/{gse_id}.samples.tsv",
        script = "scripts/rsem_to_dgelist.R"

    output:
        "data/job/{gse_id}.dgelist.rds"

    shell:
        """
            Rscript {input.script} \
                --rsem {input.tsv} \
                --genes {input.genes} \
                --samples {input.samples} \
                --out {output}
        """

rule compile_rmarkdown:
    message:
        """
        --- Compile the Rmarkdown report to a xaringan presentation

            input: {input}
            output: {output}
        """

    input:
        report = "doc/stats_and_bfx.Rmd",
        dgelist = "data/job/GSE103528.dgelist.rds",
        probdists = "figures/Relationships_among_some_of_univariate_probability_distributions.jpg",
        limma_figure = "figures/gkv007fig1.jpg"

    output:
        "doc/stats_and_bfx.html"

    script:
        "{input.report}"

