import os

TABLE = "Activities"
REGION = "us-east-1"
AWSENV = "AWS_SAM_LOCAL"
TABLE_NAME = os.environ.get("TABLE", "Activities")
REGION = os.environ.get("REGION", "us-east-1")
AWS_ENVIRONMENT = os.environ.get("AWSENV", "AWS_SAM_LOCAL")
