import StringIO
import zipfile
import mimetypes
import boto3
from botocore.client import Config


s3 = boto3.resource('s3', config=Config(signature_version='s3v4'))

port_bucket = s3.Bucket('elwaz.net')
build_bucket = s3.Bucket('port.elwaz')

portfolio_zip = StringIO.StringIO()
build_bucket.download_fileobj('portfolio.zip', portfolio_zip)

with zipfile.ZipFile(portfolio_zip) as myzip:
    for nm in myzip.namelist():
        obj = myzip.open(nm)
        port_bucket.upload_fileobj(obj, nm,
            ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
        port_bucket.Object(nm).Acl().put(ACL='public-read')