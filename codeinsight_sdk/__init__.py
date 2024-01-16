#  _  _   _   _ ___       __ ___  __    ___    __  _
# /  / \ | \ |_  |  |\ | (_   |  /__ |_| | __ (_  | \ |/
# \_ \_/ |_/ |_ _|_ | \| __) _|_ \_| | | |    __) |_/ |\
#
"""
Code Insight SDK package for Python.

Copyright (C) 2024 Zachary Karpinski. All Rights Reserved.

Basic usage:

   >>> import codeinsight_sdk
   >>> client = codeinsight_sdk.CodeInsightClient(<base_url>, <api_token>)
   >>> print(client.projects.all())
   ...
"""

from .client import CodeInsightClient
