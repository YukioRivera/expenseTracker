import pandas as pd
import re

df_boa = pd.read_csv("BOA_2024_April_1371.csv")

df1_chase = pd.read_csv("../processed/2022_Chase1664_Activity20221126_20221231_20241127.CSV")
df2_chase = pd.read_csv("../processed/2022_Chase9197_Activity20221126_20221231_20241127.CSV")
df3_chase = pd.read_csv("../processed/2023_Chase1664_Activity20230101_20231231_20241127.CSV")
df4_chase = pd.read_csv("../processed/2023_Chase9197_Activity20230101_20231231_20241127.CSV")
df5_chase = pd.read_csv("../processed/2024_Chase1664_Activity20240101_20241126_20241127.CSV")
df6_chase = pd.read_csv("../processed/2024_Chase9197_Activity20240101_20241126_20241127.CSV")


boa1 = pd.read_csv("../BOA/BOA_2024_February_1371.csv")
boa2 = pd.read_csv("../BOA/BOA_2024_March_1371.csv")
boa3 = pd.read_csv("../BOA/BOA_2024_April_1371.csv")
boa4 = pd.read_csv("../BOA/BOA_2024_May_1371.csv")
boa5 = pd.read_csv("../BOA/BOA_2024_June_1371.csv")
boa6 = pd.read_csv("../BOA/BOA_2024_July_1371.csv")
boa7 = pd.read_csv("../BOA/BOA_2024_August_1371.csv")
boa8 = pd.read_csv("../BOA/BOA_2024_September_1371.csv")
boa9 = pd.read_csv("../BOA/BOA_2024_October_1371.csv")
boa10 = pd.read_csv("../BOA/BOA_2024_November_1371.csv")

# print(boa1)
# print(boa2)
# print(boa3)
# print(boa4)
# print(boa5)
# print(boa6)
# print(boa7)
# print(boa8)
# print(boa9)
# print(boa10)

# creating the list to concatenate
dfs_chase = [df1_chase, df2_chase, df3_chase, df4_chase, df5_chase, df6_chase]
dfs_boa = [boa1, boa2, boa3, boa4, boa5, boa6, boa7, boa8, boa9, boa10]

# creating the combined df for boa and chase
df_Chase = pd.concat(dfs_chase)
df_BOA = pd.concat(dfs_boa)

# Making the transationDate into a datetime object
df_Chase["TransactionDate"] = pd.to_datetime(df_Chase["TransactionDate"])
df_BOA["TransactionDate"] = pd.to_datetime(df_BOA["TransactionDate"])

# sorting the dfs but chronological order, most recent purchases on top then resettinng index from 0 to len(df)
df_Chase = df_Chase.sort_values(by='TransactionDate', ascending=False).reset_index()
df_BOA = df_BOA.sort_values(by='TransactionDate', ascending=False).reset_index()

# removing the unordered index
del df_Chase['index']
del df_BOA['index']


df_Chase = df_Chase[df_Chase["Type"] == 'Sale'] # remove returns, refunds, and anything other than sales 
df_BOA = df_BOA[df_BOA["Type"] == 'Sale'] # remove returns, refunds, and anything other than sales 

# creating labled and unllabeled columns for chase and boa 
df_BOA['Label'] = 'Unlabeled'
df_Chase['Label'] = 'Labeled'

# combine the dataframes 
df_combined = pd.concat([df_Chase, df_BOA], ignore_index=True)
df_combined = df_combined.sort_values(by='TransactionDate', ascending=False).reset_index()

# print(df_Chase.to_string())
print(df_combined.to_string())