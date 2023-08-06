import os
import sys
import cv2
import json
import boto3
import pickle
import asyncio
import requests
import numpy as np
# from PIL import Image
from typing import Any
from io import BytesIO
from threading import Thread, Lock
from boto3.s3.transfer import TransferConfig



class ProgressPercentage(object):
    def __init__(self, fileobj:Any=None, filename:str=None, fsize=None):
        self._fileobj = fileobj
        self._filename = filename
        if fsize is not None:
            self._size = fsize
        else:
            self._size = fileobj.getbuffer().nbytes if fileobj!=None else float(os.path.getsize(filename))
            

        self._seen_so_far = 0
        self._lock = Lock()

    def __call__(self, bytes_amount):
        # To simplify we'll assume this is hooked up
        # to a single filename.
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s %s %s %s / %s  (%.2f%%)"
                % (
                    "Uploading file ",
                    self._filename,
                    "to S3 =========>",
                    self._seen_so_far,
                    self._size,
                    percentage,
                )
            )
            sys.stdout.flush()


class S3Client:
    def __init__(self):
        presigned_cred = requests.post("http://prodbackend.alectio.com/experiments/getcredentials").json()
        # boto3 clients to read / write to S3 bucket
        self.client = boto3.client(
            "s3",
            aws_access_key_id=presigned_cred['KEY'],
            aws_secret_access_key=presigned_cred["SECRET"],
        )
        self.config = TransferConfig(
            multipart_threshold=1024 * 25,
            max_concurrency=10,
            multipart_chunksize=1024 * 25,
            use_threads=True,
        )

        # most probably we dont need to do these two steps
        os.environ["AWS_ACCESS_KEY_ID"] = presigned_cred['KEY']
        os.environ["AWS_SECRET_ACCESS_KEY"] = presigned_cred['SECRET']

    def upload_file(self, file_name:str, bucket:str, key:str):
        self.client.upload_file(file_name, bucket, key,
            # ExtraArgs={ 'ACL': 'public-read', 'ContentType': 'video/mp4'},
            Config = self.config,
            Callback=ProgressPercentage(filename=file_name)
            )
    def upload_object(self,obj:Any,bucket:str,key:str,format:str):
        if format == "pickle":
            bytestr = pickle.dumps(obj)
        elif format == "json":
            bytestr = bytes(json.dumps(obj).encode("UTF-8"))
        elif format == "txt":
            bytestr = b"{}".format(obj)
        elif format in ['.png','.jpg','.jpeg']:
            bytestr = cv2.imencode('.png', (obj * 255).astype(np.uint8))[1].tostring()
        fileobj = BytesIO(bytestr)
        self.client.upload_fileobj(
            Fileobj=fileobj,
            Bucket=bucket,
            Key=key,
            Callback=ProgressPercentage(fileobj=fileobj, filename=None),
            Config=self.config,
        )
        return

    def read(self, bucket:str,key:str,format:str):
        s3_object = self.client.get_object(Bucket=bucket, Key=key)
        body = s3_object["Body"]
        if format == "json":
            jstr = body.read().decode("utf-8")
            content = json.loads(jstr)
        elif format == "pickle":
            f = body.read()
            content = pickle.loads(f)
        elif format == "txt":
            content = body.read().decode(encoding="utf-8", errors="ignore")
        
        return content


if __name__=="__main__":
    client = S3Client()
    print(client.presigned_cred)
    client.upload_file("sql_client.py",)