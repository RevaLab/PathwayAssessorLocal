import pandas as pd
import pathway_assessor as pa

expression_table = "C:\\Users\\Boris\\Desktop\\PW_A_Local\\ucec.normal.txt"

expression_df = pd.read_csv(expression_table, sep='\t', index_col=0)


scores = pa.all(
	expression_table=expression_df,
	db='hallmark',
	ascending=True,
	rank_method='max'
)

print(scores)