import shared

from codeinsight_sdk.client import CodeInsightClient

print("Example 1: List projects")

client = CodeInsightClient(shared.BASE_URL, shared.AUTH_TOKEN)


print(client.projects.all())
