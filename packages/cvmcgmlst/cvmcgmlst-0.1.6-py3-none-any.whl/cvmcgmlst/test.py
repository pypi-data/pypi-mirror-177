import os
import sys
import pandas as pd
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Blast import NCBIXML

# from Bio.Blast import NCBIWWW
from Bio.Blast.Applications import NcbiblastnCommandline
from Bio.Blast.Applications import NcbimakeblastdbCommandline


def makeblastdb(file):
    cline = NcbimakeblastdbCommandline(
        dbtype="nucl", title='cgMLSt',
        hash_index=True,
        parse_seqids=True,
        input_file=file)
    print(f"Making database...")
    stdout, stderr = cline()
    print(stdout)
    # print('Finish')


makeblastdb('/Users/cuiqingpo/Downloads/cgmlst_tq/tq/cgMLST.fa')
