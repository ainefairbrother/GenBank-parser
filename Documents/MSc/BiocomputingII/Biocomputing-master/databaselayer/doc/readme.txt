Author: Aine Fairbrother-Browne
Email: afairb01@mail.bbk.ac.uk

GenBank file parser and database connection
Documentation for files parser.py and split_file.py.






Description of project

This tier of the project aims to parse a GenBank file and store some relevant information in an SQL database.

Setup: split_file.py

Some steps must be taken prior to use of the parser. Please see the 'Dependencies' section below for required imports. As well as these, it is important to note that the split_file.py script must be run before the parser is used. The file that the user passes into it must be a GenBank format file. The split_file.py script takes the raw GenBank file and splits it at the '//' entry separator, thus, a separate file for each gene locus is generated. Ensure that these files are stored in a directory with nothing else in it. Once this step has been completed, set the 'indir' variable in the parser.py script to the directory containing your split files.

Dependencies: parser.py, split_file.py

The following imports must be performed in order to run the code. Code to import them is included in both parser.py and split_file.py

split_file.py:
    import re

parser.py:
    import re
    import os
    import pandas as pd
    import mysql.connector
    from sqlalchemy import create_engine

Data extraction tier: parser.py
Functions

First core function: numerical_split
Allows string to digit conversion of the filenames derived from the split GenBank file. 
Parameters:
1. filename

Second core function: match_finder
Finds one match to the supplied regex in each separate file derived from the split GenBank file. 
Parameters:
1.	list - this is an empty list in which you want to store the
function output
2.	compiler - this is the regex compiler in the format:
compiler = re.compile(r" regex here ", re.MULTILINE|re.DOTALL)
3.	else_statement - this is the value that will be appended to the
list specified in parameter 1. if no value can be found by the regex in the GenBank file. DEFAULT = 'None'

Third core function: findall_matcher
Finds all matches to the supplied regex in each separate file derived from the split GenBank file. 
Parameters:
1.	list_ - this is an empty list in which you want to store the
function output
2.	pattern - this is the findall regex pattern in the form r"pattern"

Implementation: parser.py 

Here, the functions are used to extract useful parts of the GenBank file.
Regular expressions have been designed to extract key data the match_finder and findall_matcher functions store their captured data in the following lists:

List name
Description 
gene_ids            
Unique locus identifier                                       
genbank_accessions  
Unique genbank identifier                                     
gene_name
Name of the gene                                              
clean_dna_seq             
Nucleotide sequence of the gene                               
gene_products       
This list contains the 1st protein product of the gene        
chr_loc             
Chromosomal location of the locus                             
clean_protein_seq         
Amino acid sequence encoded by the coding sequence of the gene
exon_start          
Contains sub-lists of exon start positions for each locus     
exon_end            
Contains sub-lists of exon end positions for each locus     


Data processing: parser.py

Some of the data requires additional post-capture processing
DNA sequence:
cleaning of whitespaces and digits present in the GenBank file – begins with list dna_seq and the database-friendly data is stored in the list clean_dna_seq.
Protein sequence:
Cleaning of whitespaces
Coding sequence:
cds_grab is the initial list containing the raw strings
It then undergoes whitespace stripping, and the data is contained in cds_ws_strip.
The list then becomes the new list: cds_ws_strip. Extra characters are then stripped, resulting in the list clean_boundaries. 
Then the items (now in the form '123..456') are split at the ‘..’. 
After this, exons that span multiple genes are removed. 
The list is now called remove_spans. The start and end positions of the coding sequence are then stored in the lists exon_start and exon_end. 

Preparing the data for database import: parser.py
The tables of the database are fed the following data:-

    Table 1
    Coding_region:
       - gene_ids as 'Gene_ID'
       - exon start as 'Start_location'
       - exon end as 'End_location'
    Table 2
    Gene_info
       - gene_ids as 'Gene_ID'
       - chr_loc as 'Chromosome_location'
       - clean_dna_seq as DNA_sequence
       - clean_protein_seq as Protein_sequence
       - gene_products as Protein_product

Preparing exon_start and exon_end:
A zip object called zipped_id_start_end is created - it is a list of tuples. A list comprehension is utilised to go from lists of lists of the form exon_start, exon_end to a list of tuples with repeating gene_ids i.e. any one gene_ids entry will be contained in n rows where n is the number of start positions and corresponding end positions.

Removal of splice variants:
Splice variants are then identified and deleted. An enumerating for loop identifies the gene_ids associated with these, and removes any splice variant tuples from the zipped_id_start_end list and any rows containing splice variants from the Gene_info table. 

Preparing the data for table 1:
Using pandas (imported as pd), the zip object is converted to a Pandas DataFrame.

Preparing the data for table 2:
Using pandas (imported as pd), the five lists named under 'Table 2' above are
converted to a Pandas DataFrame object.

A connection to the database is generated using the sqlAlchemy function
create_engine.
mysql.connector is then used to login into the database and port the dataframes in. 
# GenBank-parser
