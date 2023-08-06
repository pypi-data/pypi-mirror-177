import boto3
from cookiecutter.utils import simple_filter


@simple_filter
def get_aws_account_id(*args, **kawrgs):
    sts = boto3.client("sts")
    return sts.get_caller_identity()["Account"]