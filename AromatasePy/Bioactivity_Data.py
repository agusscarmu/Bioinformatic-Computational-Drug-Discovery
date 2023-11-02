import pandas as pd
from chembl_webresource_client.new_client import new_client

target = new_client.target
target_query = target.search('aromatase')
targets = pd.DataFrame.from_dict(target_query)

selected_target = targets.target_chembl_id[0]

activity = new_client.activity
res = activity.filter(target_chembl_id=selected_target).filter(standard_type="IC50")

df = pd.DataFrame.from_dict(res)

df.standard_type.unique()

df.to_csv('aromatase_bioactivity_data.csv', index=False)

df2 = df[df.standard_value.notna()]


bioactivity_class = []
for i in df2.standard_value:
  if float(i) >= 10000:
    bioactivity_class.append("inactive")
  elif float(i) <= 1000:
    bioactivity_class.append("active")
  else:
    bioactivity_class.append("intermediate")


mol_cid = []
for i in df2.molecule_chembl_id:
  mol_cid.append(i)


canonical_smiles = []
for i in df2.canonical_smiles:
  canonical_smiles.append(i)


standard_value = []
for i in df2.standard_value:
  standard_value.append(i)


data_tuples = list(zip(mol_cid, canonical_smiles, bioactivity_class, standard_value))
df3 = pd.DataFrame( data_tuples,  columns=['molecule_chembl_id', 'canonical_smiles', 'bioactivity_class', 'standard_value'])


df3.to_csv('aromatase_bioactivity_preprocessed_data.csv', index=False)

