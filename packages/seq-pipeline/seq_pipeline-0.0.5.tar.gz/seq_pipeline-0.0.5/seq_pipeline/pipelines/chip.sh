# --- VARIABLES ---
# > input_type = paired_fastq
BASE_PATH="{ path base_exists }"
CPU_CORES="{ integer > 0 }"
BOWTIE2_INDEX_PATH="{ path base_exists }"
BAM_WITH_DUPLICATES="{ choice keep|remove }"
BIGWIG_BIN_SIZE="{ integer > 0 }"
MACS2_CONTROL_PATH="{ optional path file_exists }"
MACS2_PVALUE="{ regex [0-9]+e-[0-9]+ }"
MACS2_GENOME_SIZE="{ regex mm|hs|cc|dm|[0-9]+ }"


# --- MODULES ---
echo "# initializing environment and loading modules $(date '+%Y/%m/%d %H:%M:%S UTC%:::z')" >&2
module reset
module load python/3.9 java/13.0
module load fastqc/0.11 bowtie2/2.4 samtools/1.12
virtualenv --no-download "$SLURM_TMPDIR/env.python.3"
source "$SLURM_TMPDIR/env.python.3/bin/activate" &&
pip install --no-index --quiet --upgrade pip &&
pip install --no-index --quiet numpy scipy matplotlib pandas deepTools==3.5.0 MACS2==2.2.7.1
chmod +x "$SLURM_TMPDIR/env.python.3/bin/"* 2> /dev/null


# --- FUNCTIONS ---
function reads-count {
    case "$1" in
        fastq) echo "$(zcat "$2" | wc -l) / 4" | bc ;;
        fastqx2) echo "$(zcat "$2" | wc -l) / 4 * 2" | bc ;;
        bam) samtools idxstats "$2" | awk -F '\t' '{s+=$3}END{print s}' ;;
        *) echo "error: invalid format: $1" >&2 ; return 1 ;;
    esac
}
function reads-diff {
    local INITIAL="$(reads-count "$1" "$2")"
    local FINAL="$(reads-count "$3" "$4")"
    local PERCENT="$(echo "scale=2 ; $FINAL / $INITIAL * 100" | bc)"
    echo "reads: initial=$INITIAL final=$FINAL ($PERCENT%)"
}


# --- 1 QC AND TRIMMING ---
echo "# qc and trimming: start $(date '+%Y/%m/%d %H:%M:%S UTC%:::z')" >&2
TRIM_READS_SCRIPT_PATH="$BASE_PATH.tmp.trim_reads.py"
cat << EOM | tr -d "[:space:]" | base64 -d | gzip -dc > "$TRIM_READS_SCRIPT_PATH"
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
EOM
python "$TRIM_READS_SCRIPT_PATH" -i "$BASE_PATH.r1.fastq.gz" "$BASE_PATH.r2.fastq.gz" -a "AGATCGGAAGAG" -p "$CPU_CORES"
rm "$TRIM_READS_SCRIPT_PATH"
fastqc --quiet -t "$CPU_CORES" "$BASE_PATH.r1.fastq.gz" "$BASE_PATH.r2.fastq.gz" "$BASE_PATH.trimmed.r1.fastq.gz" "$BASE_PATH.trimmed.r2.fastq.gz"
rm "$BASE_PATH.r1_fastqc.zip" "$BASE_PATH.r2_fastqc.zip" "$BASE_PATH.trimmed.r1_fastqc.zip" "$BASE_PATH.trimmed.r2_fastqc.zip"
[ -d "$BASE_PATH.qc" ] || mkdir "$BASE_PATH.qc"
mv "$BASE_PATH.r1_fastqc.html" "$BASE_PATH.qc/$(basename "$BASE_PATH").r1.qc.html"
mv "$BASE_PATH.r2_fastqc.html" "$BASE_PATH.qc/$(basename "$BASE_PATH").r2.qc.html"
mv "$BASE_PATH.trimmed.r1_fastqc.html" "$BASE_PATH.qc/$(basename "$BASE_PATH").trimmed.r1.qc.html"
mv "$BASE_PATH.trimmed.r2_fastqc.html" "$BASE_PATH.qc/$(basename "$BASE_PATH").trimmed.r2.qc.html"


# --- 2 ALIGNEMENT ---
echo "# alignment: start $(date '+%Y/%m/%d %H:%M:%S UTC%:::z')" >&2
bowtie2 -p "$CPU_CORES" --fr --no-unal --no-mixed --no-discordant -x "$BOWTIE2_INDEX_PATH" -1 "$BASE_PATH.trimmed.r1.fastq.gz" -2 "$BASE_PATH.trimmed.r2.fastq.gz" |
samtools fixmate -@ "$CPU_CORES" -m /dev/stdin "$BASE_PATH.bam"


# --- 3 SORTING ---
echo "# sorting: start $(date '+%Y/%m/%d %H:%M:%S UTC%:::z')" >&2
mv "$BASE_PATH.bam" "$BASE_PATH.unsorted.bam"
samtools sort -@ "$CPU_CORES" -o "$BASE_PATH.bam" "$BASE_PATH.unsorted.bam"
samtools index -@ "$CPU_CORES" "$BASE_PATH.bam"
echo "aligned reads: $(reads-diff fastqx2 "$BASE_PATH.trimmed.r1.fastq.gz" bam "$BASE_PATH.bam")" >&2
rm "$BASE_PATH.unsorted.bam"


# --- 4 DUPLICATES ---
echo "# duplicates: start $(date '+%Y/%m/%d %H:%M:%S UTC%:::z')" >&2
mv "$BASE_PATH.bam" "$BASE_PATH.with_duplicates.bam"
mv "$BASE_PATH.bam.bai" "$BASE_PATH.with_duplicates.bam.bai"
samtools markdup -@ "$CPU_CORES" -r -s "$BASE_PATH.with_duplicates.bam" "$BASE_PATH.bam"
samtools index -@ "$CPU_CORES" "$BASE_PATH.bam"
echo "duplicates: $(reads-diff bam "$BASE_PATH.with_duplicates.bam" bam "$BASE_PATH.bam")" >&2
[ "$BAM_WITH_DUPLICATES" = remove ] && rm "$BASE_PATH.with_duplicates.bam" "$BASE_PATH.with_duplicates.bam.bai"


# --- 5 BIGWIG ---
echo "# bigwig: start $(date '+%Y/%m/%d %H:%M:%S UTC%:::z')" >&2
bamCoverage -b "$BASE_PATH.bam" -o "$BASE_PATH.cpm.bigwig" -bs "$BIGWIG_BIN_SIZE" -e 150 --normalizeUsing BPM -p "$CPU_CORES"


# --- 6 PEAK CALLING ---
echo "# peak calling: start $(date '+%Y/%m/%d %H:%M:%S UTC%:::z')" >&2
MACS2_OUTPUT_PATH="$BASE_PATH.$MACS2_PVALUE.peaks"
[ -d "$MACS2_OUTPUT_PATH" ] || mkdir "$MACS2_OUTPUT_PATH"
if [ "$MACS2_CONTROL_PATH" = "" ]; then
    macs2 callpeak -t "$BASE_PATH.bam" -n "$(basename "$BASE_PATH")" --outdir "$MACS2_OUTPUT_PATH" -f BAMPE -p "$MACS2_PVALUE" -g "$MACS2_GENOME_SIZE" --call-summits --min-length 100 --max-gap 50
else
    macs2 callpeak -t "$BASE_PATH.bam" -n "$(basename "$BASE_PATH")" --outdir "$MACS2_OUTPUT_PATH" -f BAMPE -c "$MACS2_CONTROL_PATH" -p "$MACS2_PVALUE" -g "$MACS2_GENOME_SIZE" --call-summits --min-length 100 --max-gap 50
fi
REFORMAT_MACS2_SCRIPT_PATH="$BASE_PATH.tmp.reformat_macs2.py"
cat << EOM | tr -d "[:space:]" | base64 -d | gzip -dc > "$REFORMAT_MACS2_SCRIPT_PATH"
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
EOM
python "$REFORMAT_MACS2_SCRIPT_PATH" "$MACS2_OUTPUT_PATH"
rm "$REFORMAT_MACS2_SCRIPT_PATH"


# --- DONE ---
echo "# done $(date '+%Y/%m/%d %H:%M:%S UTC%:::z')" >&2