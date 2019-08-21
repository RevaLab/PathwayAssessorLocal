import csv
import os
import pickle
import sys

import pandas as pd
import pathway_assessor as pa


def clean_filename(f):
    return os.path.splitext(os.path.basename(f))[0]


def output_dir_path(base_dir, expression_table_f, pathway_db_choice, ascending, rank_method):
    filename = clean_filename(expression_table_f)
    if ascending:
        direction = 'sup'
    else:
        direction = 'act'
    return '{}/output/{}_{}_{}_{}r'.format(base_dir, filename, pathway_db_choice, direction, rank_method)


def write_score_table(output_dir_path, score_type, df):
    output_path = '{}/{}.tsv'.format(output_dir_path, score_type)
    df.to_csv(output_path, sep='\t')


def user_pathways_dict(user_pw_db_f):
    with open(user_pw_db_f, mode='r') as infile:
        reader = csv.reader(infile)
        user_pathways_d = {rows[0]: rows[2:] for rows in reader}

    return user_pathways_d


if __name__ == '__main__':
    expression_table_f = sys.argv[1]
    ascending = sys.argv[2].lower() == 's'
    pathway_db_choice = sys.argv[3]
    rank_method = sys.argv[4]

    base_dir = sys.argv[-1]

    if pathway_db_choice == 'user':
        user_pw_db_f = sys.argv[5]
        user_pw_name = clean_filename(user_pw_db_f)
        output_dir = output_dir_path(base_dir, expression_table_f, user_pw_name, ascending, rank_method)
    else:
        user_pw_db_f = None
        output_dir = output_dir_path(base_dir, expression_table_f, pathway_db_choice, ascending, rank_method)

    os.makedirs(output_dir, exist_ok=True)

    expression_df = pd.read_csv(expression_table_f, sep='\t', index_col=0)

    if pathway_db_choice == 'xcell' \
            or pathway_db_choice == 'xcell_complete_signatures' \
            or pathway_db_choice == 'all' \
            or pathway_db_choice == 'wikipathways' \
            or pathway_db_choice == 'immune_all':
        user_pathways = pickle.load(open('databases/{}.pkl'.format(pathway_db_choice), 'rb'))
        scores = pa.all(expression_table=expression_df,
                        pathways=user_pathways,
                        ascending=ascending,
                        rank_method=rank_method)
    elif not user_pw_db_f:
        scores = pa.all(expression_table=expression_df,
                        db=pathway_db_choice,
                        ascending=ascending,
                        rank_method=rank_method)
    else:
        user_pathways = user_pathways_dict(user_pw_db_f)
        scores = pa.all(expression_table=expression_df,
                        pathways=user_pathways,
                        ascending=ascending,
                        rank_method=rank_method)

    for score_type in scores:
        write_score_table(output_dir_path=output_dir, score_type=score_type, df=scores[score_type])

