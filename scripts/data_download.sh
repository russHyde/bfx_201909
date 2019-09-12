GSE_FILENAME="GSE103528_RSEM.gene.results.txt.gz"
GSE_PREFIX="ftp.ncbi.nlm.nih.gov/geo/series"
GSE_URL="${GSE_PREFIX}/GSE103nnn/GSE103528/suppl/${GSE_FILENAME}"

wget "https://${GSE_URL}" -P "data/ext/"
