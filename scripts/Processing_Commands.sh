#!/bin/bash

# Merge Sequences together with FLASH 
mkdir Flash_Files
~/Desktop/Scripts/FLASH-1.2.11/flash Undetermined_S0_L001_R1_001.fastq.gz Undetermined_S0_L001_R2_001.fastq.gz -O -o Flash_Files/Flash_Files -M 300

# Parse headers by barcode
mkdir Barcode_IDs
gunzip Undetermined_S0_L001_I1_001.fastq.gz
for i in `cat ./Barcode_sequences.txt`; do grep -B1 "$i" Undetermined_S0_L001_I1_001.fastq > "$i".ids.fastq; done
for i in ./*.ids.fastq; do grep -A0 "@M00776" "$i" >> "$i".headers.txt; done
rm *.ids.fastq
for i in ./*.headers.txt; do cat "$i" | sed 's/1:N:0:0//g' > Barcode_IDs/"$i".2.txt; done
rm *.headers.txt

# Create demultiplexed FastQ files
mkdir Dereplicated_Fastq_Files_1
cat Flash_Files/Flash_Files.extendedFrags.fastq | sed 's/@M00776/>@M00776/g' >> Flash_Files/Flash_Files.extendedFrags.2.fastq
rm Flash_Files/Flash_Files.extendedFrags.fastq
for i in Barcode_IDs/*.fastq.headers.txt.2.txt; do ~/Desktop/Scripts/seqtk/seqtk subseq Flash_Files/Flash_Files.extendedFrags.2.fastq "$i" > "$i".fastq; done
mv Barcode_IDs/*.fastq Dereplicated_Fastq_Files_1/

# Quality filter dereplicated FastQ files
mkdir Quality_Trimmed_Fastq_2
for i in Dereplicated_Fastq_Files_1/*.2.txt.fastq; do ~/.local/bin/cutadapt -q 10 -o "$i".trimmed_q10.fastq "$i"; done
mv Dereplicated_Fastq_Files_1/*q10.fastq Quality_Trimmed_Fastq_2/

# Remove primer/adapter sequence from trimmed FastQ files
mkdir Filtered_Trimmed_Fastq_Files_3
for i in Quality_Trimmed_Fastq_2/*q10.fastq; do ~/.local/bin/cutadapt -g ^ATCTYRYRGTGCCAGCMGCCGCGGTAA --untrimmed-output "$i".untrimmed.fastq -o "$i".adapter_trimmed.fastq "$i"; done
mv Quality_Trimmed_Fastq_2/*.adapter_trimmed.fastq Filtered_Trimmed_Fastq_Files_3/
mkdir Seqs_without_adapters
mv Quality_Trimmed_Fastq_2/*.untrimmed.fastq Seqs_without_adapters/

# Create quality score log files for filtered and trimmed FastQ files
mkdir Log_Files
for i in Filtered_Trimmed_Fastq_Files_3/*.adapter_trimmed.fastq; do usearch -fastq_stats "$i" -log "$i".stats.log; done
mv Filtered_Trimmed_Fastq_Files_3/*.log Log_Files/