# maeveScripts


Dependencies

It uses a BBMap script for demultiplexing (`filterbyname.sh`)


Meta-Map Format

The third step is to read in the mapping file for each sequencing
run.

 - a prefix called the seqID which represents the sequencing
   run and is the name of the subfolder in which the sequence
   files are contained
 - a paired or single end flag ("PE" or "SE")
 - the name of the forward reads or the common suffix among
   all forward reads in the
 - the name of the reverse reads or the common suffix among
   all the reverse reads
 - the name of the index file if there is one
 - a demultiplexing boolean flag ("T" or "F")
 - the file path of a list of barcode sequences and sample names      
 - a boolean if you want the scripts to check sequence header formatting
   matches between files (required for demultiplexing)
 - a boolean if you want the scripts to remove the last two chars of
   all sequence headers ( makes older sequencing files compatible with
   demuxing script)
