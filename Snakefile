# We aren't using snakemake's remote providers to download the data here:
# - Building DAG of jobs is painfully slow when using FTPRemoteProvider() in
# smk 5.4, 5.5, 5.6 see snakemake issues #1275
# - Couldn't work out how to download an http query and then copy it to a
# location
# - Therefore, we wrote a script to download the files using bash

rule all:
    input:
        "data/ext/GSE103528_RSEM.gene.results.txt.gz"


rule get_gse103528:
    message:
        """
        --- Downloading {input} to {output}
        """

    output:
        "data/ext/GSE103528_RSEM.gene.results.txt.gz"

    shell:
        """
            bash ./scripts/data_download.sh
        """
