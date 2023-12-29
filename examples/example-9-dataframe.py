import shared
import pandas as pd
from codeinsight_sdk.client import CodeInsightClient

print("Example 9: Working with Pandas DataFrames")

client = CodeInsightClient(shared.BASE_URL, shared.AUTH_TOKEN)


inventory = client.project_inventory.get(1)
df = pd.DataFrame(inventory.__dict__['inventoryItems'])