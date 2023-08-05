# cvmmlst


cvmcgmlst is a tool developed based on the [cvmmlst](https://github.com/hbucqp/cvmmlst) for core genome MLST analysis .

```
usage: cvmcgmlst -i <genome assemble directory> -o <output_directory>

Author: Qingpo Cui(SZQ Lab, China Agricultural University)

optional arguments:
  -h, --help      show this help message and exit
  -i I            <input_path>: the PATH to the directory of assembled genome files. Could not use with -f
  -f F            <input_file>: the PATH of assembled genome file. Could not use with -i
  -db DB          <database_path>: path of cgMLST database
  -o O            <output_directory>: output PATH
  -minid MINID    <minimum threshold of identity>, default=95
  -mincov MINCOV  <minimum threshold of coverage>, default=90
  -create_db      <initialize the reference database>
  -t T            <number of threads>: default=8
  -v, --version   Display version
```


## Installation
### Using pip
pip3 install cvmcgmlst

### Using conda
comming soon...

## Dependency
- BLAST+ >2.7.0

**you should add BLAST in your PATH**


## Blast installation
### Windows


Following this tutorial:
[Add blast into your windows PATH](http://82.157.185.121:22300/shares/BevQrP0j8EXn76p7CwfheA)

### Linux/Mac
The easyest way to install blast is:

```
conda install -c bioconda blast
```



## Usage


### Making your own database

Users could create their own core genome database. All you need is a FASTA file of nucleotide sequences. The sequence IDs should have the format >locus_allelenumber, where **locus** is the loci name, **allelenumber** is the number of this allele. 
The curated core genome fasta file should like this:
```
>GBAA_RS00015_1
TTGGAAAACATCTCTGATTTATGGAACAGCGCCTTAAAAGAACTCGAAAAAAAGGTCAGT
AAACCAAGTTATGAAACATGGTTAAAATCAACAACCGCACATAATTTAAAGAAAGATGTA
TTAACAATTACGGCTCCAAATGAATTCGCCCGTGATTGGTTAGAATCTCATTATTCAGAG
CTAATTTCGGAAACACTTTATGATTTAACGGGGGCAAAATTAGCTATTCGCTTTATTATT
CCCCAAAGTCAAGCTGAAGAGGAGATTGATCTTCCTCCTGCTAAACCAAATGCAGCACAA
GATGATTCTAATCATTTACCACAGAGTATGCTAAACCCAAAATATACGTTTGATACATTT
GTTATTGGCTCTGGTAACCGTTTTGCTCACGCTGCTTCATTGGCCGTAGCCGAAGCGCCA
GCTAAAGCATATAATCCCCTCTTTATTTATGGGGGAGTTGGACTTGGAAAAACCCATTTA
ATGCATGCAATTGGCCATTATGTAATTGAACATAACCCAAATGCCAAAGTTGTATATTTA
TCATCAGAAAAATTTACAAATGAATTCATTAATTCTATTCGTGATAATAAAGCGGTCGAT
TTTCGTAATAAATACCGCAATGTAGATGTTTTATTGATAGATGATATTCAATTTTTAGCG
GGAAAAGAACAAACTCAAGAAGAGTTTTTCCATACATTCAATGCATTACACGAAGAAAGT
AAACAAATTGTAATTTCCAGTGATCGGCCACCAAAAGAAATTCCAACTTTAGAAGATCGT
CTTCGTTCTCGCTTTGAATGGGGACTCATTACGGATATTACGCCACCAGATTTAGAAACA
CGAATTGCGATTTTACGTAAAAAGGCAAAGGCTGAAGGACTTGATATACCAAATGAGGTC
ATGCTTTATATCGCAAATCAAATCGATTCAAATATTCGTGAACTAGAAGGTGCACTCATC
CGCGTTGTAGCTTATTCATCTTTAATTAACAAGGATATTAATGCTGATTTAGCAGCTGAA
GCACTTAAAGATATTATTCCAAATTCTAAACCAAAAATTATCTCCATTTATGATATTCAA
AAAGCTGTTGGAGATGTTTATCAAGTAAAATTAGAAGATTTCAAGGCGAAAAAGCGCACA
AAGTCAGTTGCCTTTCCTCGCCAAATTGCAATGTATTTGTCACGCGAACTGACAGATTCC
TCCTTACCTAAAATAGGTGAAGAATTTGGTGGACGTGATCATACAACCGTTATCCATGCC
CATGAAAAAATTTCTAAGCTACTTAAGACGGATACGCAATTACAAAAACAAGTTGAAGAA
ATTAACGATATTTTAAAGTAG
```

The first time when running cvmcgmlst, you should use -create_db parameter to initialize your database. **After your own database was created, you could run cvmcgmlst without using -create_db parameter**.

You could also create reference database using makeblastdb command.

```
makeblastdb -hash_index -in reference.fa -dbtype nucl -title cgMLST -parse_seqids
``` 

### Example
```
# Single Genome Mode
cvmcgmlst -f /PATH_TO_ASSEBLED_GENOME/sample.fa -create_db -db /PATH_TO_DATABASE/reference.fa -o PATH_TO_OUTPUT

# Batch Mode
cvmcgmlst -i /PATH_TO_ASSEBLED_GENOME_DIR -create_db -db /PATH_TO_DATABASE/reference.fa -o PATH_TO_OUTPUT
```





