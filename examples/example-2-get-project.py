import shared

from codeinsight_sdk.client import CodeInsightClient

print("Example 1: List projects")

client = CodeInsightClient(shared.BASE_URL, shared.AUTH_TOKEN)

id = client.projects.get_id("Example Project")
project = client.projects.get(id)
