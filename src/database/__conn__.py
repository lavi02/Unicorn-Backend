import boto3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from fastapi import UploadFile
import redis

Base = declarative_base()

class CONNECT:
    """
    Returns:
        각 연결 세션
    """

    def __init__(self):
        self.REGION: str = "ap-northeast-2"
        self.CLIENTKEY: str = "AKIASMEYUNS7LEQKLXBY"
        self.SECRETKEY: str = "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"

        # s3 settings
        self.BUCKET: str = "image-deploy-d"

        # rds settings
        self.USERNAME: str = "dev"
        self.PASSWORD: str = "localplayer0"
        self.ENDPOINT: str = "localhost"
        self.DBNAME: str = "develop"
        self.PORT: str = "3306"
        self.rds = create_engine(
                f"mysql+pymysql://{self.USERNAME}:{self.PASSWORD}@{self.ENDPOINT}:{self.PORT}/{self.DBNAME}?charset=utf8",
                echo=True
            )
        
        self.session = sessionmaker(
                    autocommit=False,
                    autoflush=False,
                    bind=self.rds
                )

        # redis settigns
        self.REDIS_HOSTNAME: str = "localhost"
        self.REDIS_PORT: str = "6379"
        self.REDIS_DBNAME: int = 0
    
    def s3Session(self, file: UploadFile, fileName: str):
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
            s3.upload_fileobj(file.file, self.BUCKET, fileName)
            return "success"

        except Exception as e:
            return (str(e))
        
    def engineData(self):
        return self.rds
    
        
    def engineData(self):
        return self.rds
    
    def rdsSession(self):
        try:
            return self.session
        except Exception as e:
            return str(e)

    def redisConnect(self, dbname: str):
        """
        Args:
            dbname (str): 사용할 db명
        """
        try:
            conn = redis.StrictRedis(
                host=self.REDIS_HOSTNAME,
                port=self.REDIS_PORT,
                db=self.REDIS_DBNAME
            )

            return conn

        except Exception as e:
            return (str(e))


conn = CONNECT()
Uploader = conn.s3Session
Session = conn.rdsSession()
