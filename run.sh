#!/bin/bash

read -e -p 'Expression table: ' EXPRESSION_TABLE
read -p 'Activation or Suppression score (a/s): ' ASCENDING

if [[ ! -f ${EXPRESSION_TABLE} ]]
then
    echo "Could not find EXPRESSION_TABLE."
    exit
fi

echo "
Pathway DB Choices
k: kegg
r: reactome
s: hmdb/smpdb
h: hallmark
x: xcell
xc: xcell_complete_signatures
a: all
u: user
"
read -p 'Pathway db: ' DB_CHOICE
if [[ ${DB_CHOICE} == 'r' ]] || [[ ${DB_CHOICE} == 'R' ]]; then
    DATABASE='reactome'
    USER_PATHWAY_F=0
elif [[ ${DB_CHOICE} == 'k' ]] || [[ ${DB_CHOICE} == 'K' ]]; then
    DATABASE='kegg'
    USER_PATHWAY_F=0
elif [[ ${DB_CHOICE} == 's' ]] || [[ ${DB_CHOICE} == 'S' ]]; then
    DATABASE='hmdb_smpdb'
    USER_PATHWAY_F=0
elif [[ ${DB_CHOICE} == 'h' ]] || [[ ${DB_CHOICE} == 'H' ]]; then
    DATABASE='hallmark'
    USER_PATHWAY_F=0
elif [[ ${DB_CHOICE} == 'x' ]] || [[ ${DB_CHOICE} == 'X' ]]; then
    DATABASE='xcell'
    USER_PATHWAY_F=0
elif [[ ${DB_CHOICE} == 'xc' ]] || [[ ${DB_CHOICE} == 'XC' ]]; then
    DATABASE='xcell_complete_signatures'
    USER_PATHWAY_F=0
elif [[ ${DB_CHOICE} == 'w' ]] || [[ ${DB_CHOICE} == 'W' ]]; then
    DATABASE='wikipathways'
    USER_PATHWAY_F=0
elif [[ ${DB_CHOICE} == 'a' ]] || [[ ${DB_CHOICE} == 'A' ]]; then
    DATABASE='all'
    USER_PATHWAY_F=0
elif [[ ${DB_CHOICE} == 'u' ]] || [[ ${DB_CHOICE} == 'U' ]]; then
    DATABASE='user'
    echo "
    User pathway file must be a CSV in the format of:
    pathway_name,source,gene,gene,gene
    "
    read -e -p 'Path to custom pathway file: ' USER_PATHWAY_F
else
    DATABASE='KEGG'
    USER_PATHWAY_F=0
    echo 'Database choice not recognized. Defaulting to KEGG.'
fi

read -p 'Rank method for equal values (max/min/first): ' RANK_METHOD


BASE_DIR="."
python ${BASE_DIR}/main.py ${EXPRESSION_TABLE} ${ASCENDING} ${DATABASE} ${RANK_METHOD} ${USER_PATHWAY_F} ${BASE_DIR}
