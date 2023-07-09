import boto3
import pymysql
import redis
from datetime import datetime, timedelta


class CONNECT:
    """
    Returns:
        각 연결 세션
    """

    def __init__(self):
        self.REGION: str = "ap-northeast-2"
        self.CLIENTKEY: str = ""
        self.SECRETKEY: str = ""

        # s3 settings
        self.BUCKET: str = ""

        # rds settings
        self.RDSNAME: str = ""
        self.USERNAME: str = "dev"
        self.PASSWORD: str = ""
        self.ENDPOINT: str = ""
        self.DBNAME: str = "unicorn-dev"
        self.PORT: str = "3306"

        # redis settigns
        self.REDIS_HOSTNAME: str = "localhost"
        self.REDIS_PORT: str = "6379"
        self.REDIS_DBNAME: str = ""

    def s3Session(self, filePath: str, fileName: str):
        """
        Args:
            filePath (str): 파일경로
            fileName (str): 저장될 파일명
        """
        try:
            s3 = boto3.client(
                's3',
                region_name=self.REGION,
                aws_access_key_id=self.CLIENTKEY,
                aws_secret_access_key=self.SECRETKEY
            )
            response = s3.upload_file(filePath, self.BUCKET, fileName)
            return response

        except Exception as e:
            return (str(e))

    def rdsSession(self):
        try:
            rds = pymysql.connect(
                host=self.ENDPOINT,
                user=self.USERNAME,
                password=self.PASSWORD,
                db=self.DBNAME,
                port=self.PORT,
                charset="utf8"
            )

            return rds
        except Exception as e:
            return (str(e))

    def redisConnect(self, dbname: str):
        """
        Args:
            dbname (str): 사용할 db명
        """
        try:
            conn = redis.StrictRedis(
                host=self.REDIS_HOSTNAME,
                port=self.REDIS_PORT,
                db=self.DBNAME
            )

            return conn

        except Exception as e:
            return (str(e))


conn = CONNECT()
