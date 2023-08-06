import boto3

def transform_sqlstring_to_vector(ls):
    return '( '+ ','.join(list(map(lambda x: "'"+x+"'",ls))) + ')'

def redshift_copy_query(account_id = '973153193407', 
                        role = 'TESTEBI', 
                        schema_dot_table = 'dw_tri.dim_tempo', 
                        s3_path = 's3://bi-remote-write/teste0/dataframe.csv/04.part'):
    return f"""copy {schema_dot_table}
from '{s3_path}'
iam_role 'arn:aws:iam::{account_id}:role/{role}'
delimiter ','
IGNOREHEADER 1"""


def list_files_in_bucket(bucket_name = "bi-remote-write", dir = "teste0"):
    s3 = boto3.resource("s3")
    s3_bucket = s3.Bucket(bucket_name)
    files_in_s3 = [f.key.split(dir + "/")[1] for f in s3_bucket.objects.filter(Prefix=dir).all()]
    return files_in_s3