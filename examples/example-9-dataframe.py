import shared
import pandas as pd
from codeinsight_sdk.client import CodeInsightClient

print("Example 9: Working with Pandas DataFrames")
PROJECT_ID = 1 # Update this to your project ID

client = CodeInsightClient(shared.BASE_URL, shared.AUTH_TOKEN,experimental=True)

# Get all the project vulnerabilities.
# This will return a list of Vulnerability objects.
proj_vulns = client.experimental.get_project_vulnerabilities(PROJECT_ID)

# Convert the list of Vulnerability objects to a Pandas DataFrame.
df = pd.DataFrame([v.to_dict() for v in proj_vulns])

# Now "explode" list of vulnerabilities into separate rows.
# This will create a new row for each vulnerability.
df = df.explode('vulnerabilities', ignore_index=True)

# Next we convert the vulnerabilities column into another DataFrame
# and then merge it back into the original DataFrame so that we can
# access the vulnerability properties as columns.
df_vul = pd.json_normalize(df['vulnerabilities'])
df = df.merge(df_vul, left_index=True, right_index=True)

# Optionally we can drop the original vulnerabilities column
# since we no longer need it. You can also drop other columns
df.drop(columns=['vulnerabilities'],inplace=True)

# Finally we write the output to excel
df.to_excel('example-9-output.xlsx', index=False)
