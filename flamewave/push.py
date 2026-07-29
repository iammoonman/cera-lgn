import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from stonewood import logger
import re

s3_client = None
try:
    # Create S3 client
    s3_client = boto3.client("s3", endpoint_url=os.environ["R2_ENDPOINT"], aws_access_key_id=os.environ["R2_ACCESS_KEY_ID"], aws_secret_access_key=os.environ["R2_SECRET_ACCESS_KEY"])
except:
    pass

def s3_has_object(file_name):
    try:
        s3_client.head_object(Bucket='wildheart', Key=file_name)
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == "404":
            # The key does not exist.
            return False
    except Exception as e:
        logger.info(e)
        return True

def upload_to_s3(file, file_name):
    try:
        # One month
        s3_client.upload_fileobj(file, "wildheart", file_name, ExtraArgs={"CacheControl": "public, immutable, max-age=31536000", "ContentType": "image/webp"})
        print(f"{file_name} uploaded to Wildheart.")
        return True
    except NoCredentialsError:
        print("Error: AWS credentials not available.")
    except ClientError as e:
        print(f"Error: {e}")
    return False

def to_grid(file_name):
    new_uri = re.sub(r"\.jpg\?\d+", ".webp", file_name)
    return new_uri.replace("normal", "grid")

def strip_uri(file_name):
    new_uri = re.sub(r"\.webp\?\d+", "", file_name)
    return new_uri.replace("https://cards.scryfall.io/grid/", "")