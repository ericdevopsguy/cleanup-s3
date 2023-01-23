import sys
import boto3

# Grab parameter that represents to number of deployments to keep,
# and exit with USAGE message if none are passed.
try:
    to_keep = int(sys.argv[1])
except Exception:
    print("USAGE: python3 s3-cleanup.py <number of deployments to keep>")
    exit()

to_keep = to_keep + 1

bucket_name = 'sure-infra-test'
s3 = boto3.client('s3')
response = s3.list_objects(Bucket=bucket_name)

# Determine which objects are "folders"
deployments = []
for obj in response.get("Contents", []):
    key = obj['Key']
    if '/' in key:
        deployment_name = key.split('/')[0]
        last_modified = obj['LastModified']
        deployments.append((deployment_name, last_modified))

deployments = list(set(deployments))  # Removes duplicates if any
deployments.sort(key=lambda x: x[1], reverse=True)

most_recent_deployments = [f[0] for f in deployments[:to_keep]]
deployments_to_delete = [f[0] for f in deployments[to_keep:]]

for deployment_name in deployments_to_delete:
    objects_to_delete = s3.list_objects(Bucket=bucket_name, Prefix=deployment_name)
    delete_keys = {"Objects": [{"Key": k} for k in [obj['Key'] for obj in objects_to_delete.get("Contents", [])]]}

    ## Silencing an invalid "malformed xml" exception
    try:
        s3.delete_objects(Bucket=bucket_name, Delete=delete_keys)
    except Exception:
        pass

    s3.delete_object(Bucket=bucket_name, Key=deployment_name + '/')
