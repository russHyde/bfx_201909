GTF_FILENAME="Homo_sapiens.GRCh38.87.gtf.gz"
GTF_PREFIX="ftp.ensembl.org/pub"
GTF_URL="${GTF_PREFIX}/release-87/gtf/homo_sapiens/${GTF_FILENAME}"

wget "https://${GTF_URL}" -P "data/ext"
