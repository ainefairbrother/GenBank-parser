# Aine Fairbrother-Browne, afairb01@mail.bbk.ac.uk
#! /usr/bin/env python3

#Before the parser can be run, the split_file.py code must be run in order to split
#the raw GenBank file into separate files in a directory (one for each locus)

#Dependencies:
import os
import re
import os
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine

indir = '/Users/ainefairbrother/PycharmProjects/BiocomputingII/genes'
#file path of the file where the split files are stored

# -----------------------------------Database access tier---------------------------------------------

password = '' #database password here
host_name = 'localhost' #name of host
database_name = 'biocomp_project' #this is the db into which your data will go

# ----------------------------------------------------------------------------------------------------
# -----------------------------------Data extraction tier---------------------------------------------

# -----------------------------------Numerical convert function---------------------------------------

# function to split the filenames so the directory iterator loop goes through the files in order from 1 to 241
# thus allowing all lists to be generated in the same order (from gene 1 to 241)

def numerical_convert(value):
    """
    numerical_convert returns the string-format argument as an integer.
    
    The argument is split it into its components.
    A list, split_value, then contains 3 items:
    1. empty string
    2. number in string format
    3. empty string
    It takes the second item from the list split_value, as this is the number
    This is then converted into an integer using the map() function to apply the int() function to it.
    
    """
    file_name_compiler = re.compile(r'(\d+)')
    split_value = file_name_compiler.split(value)
    split_value[1::2] = map(int, split_value[1::2])
    return(split_value)

# -- Test -- #
#a = "23.txt"
#print(numerical_convert(a))

# -----------------------------------Match finder functions-------------------------------------------

#these functions look through each file in the file defined by 'indir' for the regex provided

#this match_finder finds a single match in a locus file
def match_finder(list_, compiler, else_statement = None):
    """
    This function walks through a given directory taking the filenames, sorting by numerical name using
    the numerical_convert() function to convert string filenames into integers.
    It takes the following as parameters:
        list: the list to which the user wishes to append matches
        compiler: the regex compiler in the format re.compile(r"...()...") that the function uses to search for a match group.
        else_statement: this is a string that is appended to the list if no match group is found. It is set to None by default.
    If a match to the regex is found, match group 1 is appended to the list. If not, the else_statement is appended instead.
    Nothing visible is returned, but the list provided will be populated with matches.
    """
    for root, dirs, all_files in os.walk(indir):
        for infile in sorted(all_files, key=numerical_convert):
            open_file = open(os.path.join(root, infile), 'r')
            match = compiler.search(open_file.read())
            if match:
                list_.append(str(match.group(1)))
            else:
                list_.append(str(else_statement))
    return()

#this findall_matcher finds all the matches present in a locus file - for when more than one item is needed
def findall_matcher(list_, pattern):
    """
    This function walks through a given directory taking the filenames, sorting by numerical name using
    the numerical_convert() function to convert string filenames into integers.
    
    It takes the following as parameters:
        list: the list to which the user wishes to append matches
        pattern: the regex pattern to match in the format pattern=r"..."
    
    A list of all the matches found in one file is stored in find_all
    The directory is iterated over, and a list of lists is appended to the paramater 'list' defined by the user
    
    """
    for root, dirs, all_files in os.walk(indir):
        for infile in sorted(all_files, key=numerical_convert):
            open_file = open(os.path.join(root, infile), 'r')
            find_all = list(re.findall(pattern, open_file.read(), re.MULTILINE | re.DOTALL))
            list_.append(find_all)
    return()

# -----------------------------------Implementing data extraction-------------------------------------

#this section applies the defined functions to each piece of information we need to grab
#from the split GenBank file

genbank_accessions = []                                                     ## genbank accessions
accession_compiler = re.compile(r"^ACCESSION\s+(\w+).+\/\/", re.MULTILINE|re.DOTALL)
match_finder(genbank_accessions, accession_compiler, else_statement='none')

gene_ids = []    #don't use this other than to identify splice variants     ## gene IDs
id_compiler = re.compile(r"^LOCUS\s+(\w+).+\/\/", re.MULTILINE|re.DOTALL)
match_finder(gene_ids, id_compiler, else_statement='none')

gene_name = []  #call this gene_identifier                                  ## gene name
name_compiler = re.compile(r"^LOCUS\s.+\/gene\=\"(.+?)\".+\/\/", re.MULTILINE|re.DOTALL)
match_finder(gene_name, name_compiler, else_statement='none')

dna_seq = []
dnaseq_compiler = re.compile(r"^ORIGIN\s+(.+)\/\/", re.DOTALL|re.MULTILINE)
match_finder(dna_seq, dnaseq_compiler, else_statement='none')
clean_dna_seq = []                                                          ## DNA sequence
for x in dna_seq: #this removes all of the digits and whitespaces from the sequence
    sub1 = re.sub(r"\W", "", x)
    sub2 = re.sub(r"\d", "", sub1)
    clean_dna_seq.append(sub2)

gene_products = []                                                          ## 1st protein product
prod_compiler = re.compile(r"^LOCUS\s.+\/product\=\"(.+?)\".+\/\/", re.MULTILINE|re.DOTALL)
match_finder(gene_products, prod_compiler, else_statement='none')

chr_loc = []                                                                ## chromosomal location
chrloc_compiler = re.compile(r"^LOCUS\s.+\/map\=\"(.+?)\".+^\/\/", re.MULTILINE|re.DOTALL)
match_finder(chr_loc, chrloc_compiler, else_statement='15')

protein_seq = []
proseq_compiler = re.compile(r"^LOCUS\s.+\/translation\=\"(.+?)\".+\/\/", re.MULTILINE | re.DOTALL)
match_finder(protein_seq, proseq_compiler, else_statement='none')
clean_protein_seq = []                                                      ## protein sequence
for x in protein_seq: #this removes all of the whitespaces from the protein sequence
    sub = re.sub(r"\W", "", x)
    clean_protein_seq.append(sub)

cds_grab = [] #extracting the coding seq of the gene in order to get the exon ranges
pattern = r"^\s{5}CDS\s+(.+?)\/"
findall_matcher(cds_grab, pattern)

# -- Test -- #
# This simple enumeration test ensures that the correct gene id will be associated with the correct
# coding sequence once in the dataframe - allows me to compare the first 5 of each and ensure they match in the file
#for number, letter in enumerate(gene_ids[:5]):
    #print(number, letter)
#for number, letter in enumerate(cds_grab[:5]):
    #print(number, letter)

# the following code removes the \n and whitespace from the strings in cds_grab
# it leaves me with an overall list (cds_ws_strip), within which there are sub-lists
# the items in the sub-lists are all the coding seqs for 1 gene
cds_ws_strip = []
for list in cds_grab:
    subL = []
    for item in list:
        stripped_item = re.sub(r"\n\s{21}", "", item)
        subL.append(stripped_item)
    cds_ws_strip.append(subL)

# -- Test -- #
#for number, letter in enumerate(cds_ws_strip):
    #print(number, letter)
#for number, letter in enumerate(gene_ids):
    #print(number, letter)

#the following code strips off various superfluous characters from items in cds_ws_strip:
clean_boundaries = []
for list in cds_ws_strip:
    subL = []
    for item in list:
        sub0 = re.sub(r"join\(", "", item)
        sub1 = re.sub(r"\<", "", sub0)
        sub2 = re.sub(r"\>", "", sub1)
        sub3 = re.sub(r"\(", "", sub2)
        sub4 = re.sub(r"\)", "", sub3)
        sub5 = re.sub(r"complement", "", sub4)
        subL.append(sub5)
    clean_boundaries.append(subL)

# -- Test -- #
#for number, letter in enumerate(clean_boundaries):
    #print(number, letter)
#An example of the format of clean_boundaries:
#161 ['104..149,437..517', '926..996']

split_items = []
character = ','
for list in clean_boundaries: #this loop takes each sublist and splits each item at the comma if one is present
    subL = []
    for item in list:
        if character in item: #if the item contains a comma
            break_items = item.split(',') #splitting at comma and storing resulting items in break_items
            for component in break_items:
                subL.append(component) #appending each item in break_items to subL
        else:
            subL.append(item) #if there is no comma, the item is simply appended to subL unprocessed
    split_items.append(subL) #subL is added to the main list, split_items

# -- Test -- #
#for number, letter in enumerate(split_items):
    #print(number, letter)
#An example of the format of split_items:
#161 ['104..149', '437..517', '926..996']
#However, some entries have this format, meaning their exons span multiple genes
#221 ['U59692.1:2089..2187', 'U59693.1:710..809', 'U59693.1:1858..2093', 'U59693.1:2465..4329', '344..1028']

#the solution:
# the following code identifies any exons in the cds of loci which have labels from other loci - it then
# appends 'exons span multiple genes' to the end of each loci's list to indicate this, and chops off all but
# the last term, which is this phrase.
exon_across_genes_compiler = re.compile(r"[A-Z]{1,2}.+?\:")
remove_spans = []
phrase = 'exons span multiple genes'
for list in split_items:
    for item in list:
        match = exon_across_genes_compiler.search(item)
        if match:
            list.append(phrase) #if the alphanumerical regex is found, the phrase is appended to sublist
    if phrase in list: #after the phrases have been added, sublists containing the phrase are chopped so that they
        #contain nothing but the phrase
        l = len(list)
        chop = l - 1
        new_list = list[chop:]
        remove_spans.append(new_list)
    else:
        remove_spans.append(list) #if there is no phrase in the sublist, it is simply added to remove_spans

# -- Test -- #
#for number, letter in enumerate(remove_spans):
    #print(number, letter)
#Now, number 221 in the list looks like this:
#221 ['exons span multiple genes']

# --- separating the start and end positions of the exons into an exon start list and an exon end list --- #

# the following code grabs all the exon start positions for a particular and puts them into a sub-list
# the sub-list is then appended to the main list:
exon_start = []
exon_end = []

start_compiler = re.compile(r"^(\d+)\.")
end_compiler = re.compile(r"^\d+\.\.(\d+)")
for list in remove_spans:
    subL = []
    for item in list:
        match = start_compiler.search(item)
        if match:
            subL.append(str(match.group(1)))
    exon_start.append(subL)
for list in remove_spans:
    subL = []
    for item in list:
        match = end_compiler.search(item)
        if match:
            subL.append(str(match.group(1)))
    exon_end.append(subL)

#this code makes duplicate ID values - so that each exon start and end is associated with it's ID in a separate row
# in prep for the db
#this is the data that will fill the coding region table
zipped_id_start_end = [(id, v1, v2) for id, val1, val2 in zip(gene_ids, exon_start, exon_end)
                       for v1, v2 in zip(val1, val2)]
#zipped_id_start_end is comprised of tuples of the form:
# ('AB022430', '3606', '3666')

#removing splice variants by identifying indexes that match this regex
#splice variants are removed after start, end and id have been linked for each locus
#this allows rows of the zipped product to be removed together as opposed to removing items separately from the
#gene_ids list, exon_start list and exon_end list
#the following code identifies gene_ids that contain an 'S' after positions 7, 8 or 9
splice_variant_compiler = re.compile(r"^.{7}S|.{8}S|.{9}S") #regex to identify gene_ids of splice variants
splice_variant_indexes = []
for i, j in enumerate(gene_ids):
    match = splice_variant_compiler.search(j)
    if match:
        splice_variant_indexes.append(i) #appends the index of the splice variant to splice_variant_indexes

#the following code uses the splice_variant_index list to delete specific indexes from zipped_id_start_end
for index in sorted(splice_variant_indexes, reverse=True):
    del zipped_id_start_end[index]
# -- Test -- #
# is HSSMAD3S08 gone from the zipped_id_start_end list?
#print(zipped_id_start_end) - a simple text search of the result shows that the HSSMAD3S08 row has been removed

# --------------------------------------------------------------------------------------------------
# -----------------------------------Database connection tier---------------------------------------

# Using Pandas to generate dataframes from my lists

#gene_ids                          will be 'Gene_ID' in DB
#gene_name                         will be 'Gene_name' in DB
#chr_loc                           will be 'Chromosome_location' in DB
#clean_dna_seq                     will be 'DNA_sequence' in DB
#clean_protein_seq                 will be 'Protein_sequence' in DB
#gene_products                     will be 'Protein_product' in DB
#exon_start                        will be 'Start_location' in DB
#exon_end                          will be 'End_location' in DB

# Generating pandas dataframes
coding_region_df = pd.DataFrame(zipped_id_start_end, columns=['Gene_ID', 'Start_location', 'End_location'])
gene_info_df = pd.DataFrame({'Gene_ID': gene_ids, 'Gene_name': gene_name,'Chromosome_location':chr_loc, 'DNA_sequence':clean_dna_seq,
                        'Protein_sequence':clean_protein_seq, 'Protein_product':gene_products}, index=gene_ids)

#removing splice variants from the gene_info_df dataframe:
gene_info_df = gene_info_df.drop(gene_info_df.index[splice_variant_indexes]) #gene_info_db with no splice variants

# creating the engine to allow connection to the db
engine = create_engine('mysql+mysqlconnector://root:password@host_name/database_name', echo=False)

# Porting to the database:
coding_region_df.to_sql(name='Coding_region', con=engine, if_exists = 'append', index=False)
gene_info_df.to_sql(name='Gene_info', con=engine, if_exists = 'append', index=False)

# --------------------------------------------------------------------------------------------------
# -----------------------------------Length Tests --------------------------------------------------

#This testing tier tests list lengths throughout the parser development process
#It ensures that lists remain the same length throughout the development process, alerting me to changes
#in length by printing 'test failed' if any bugs or coding errors disrupt list length, which would ultimately
#disrupt data alignment (i.e. LOCUS 1 id with LOCUS 1 dna_seq etc.) in the database

def len_test(list_):
    """Takes in a list as a parameter, evaluates list length and prints 'test failed' 
    if the list does not match the required length of 241, or passed if it does."""
    correct_length = 241
    if len(list_) == correct_length:
        return(print('test passed'))
    else:
        return(print('test failed'))

len_test(genbank_accessions)
len_test(gene_ids)
len_test(gene_name)
len_test(dna_seq)
len_test(gene_products)
len_test(protein_seq)
len_test(exon_start)
len_test(exon_end)
len_test(cds_grab)
len_test(clean_boundaries)
len_test(clean_dna_seq)
len_test(clean_protein_seq)
len_test(cds_ws_strip)
len_test(remove_spans)

# --------------------------------------------------------------------------------------------------
