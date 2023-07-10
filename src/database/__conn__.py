import boto3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
import redis

Base = declarative_base()

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
        self.USERNAME: str = "dev"
        self.PASSWORD: str = "localplayer0"
        self.ENDPOINT: str = "localhost"
        self.DBNAME: str = "develop"
        self.PORT: str = "3306"
        self.rds = create_engine(
                f"mysql+pymysql://{self.USERNAME}:{self.PASSWORD}@{self.ENDPOINT}:{self.PORT}/{self.DBNAME}?charset=utf8",
                echo=True
            )

        # redis settigns
        self.REDIS_HOSTNAME: str = "localhost"
        self.REDIS_PORT: str = "6379"
        self.REDIS_DBNAME: str = "dev"
    
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
        
    def engineData(self):
        return self.rds
    
        
    def engineData(self):
        return self.rds
    
    def rdsSession(self):
        try:
            rds = self.rds
            session = scoped_session(
                sessionmaker(
                    autocommit=False,
                    autoflush=False,
                    bind=rds
                )
            )

            return session
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
                db=self.DBNAME
            )

            return conn

        except Exception as e:
            return (str(e))


conn = CONNECT()
Base.query = conn.rdsSession().query_property()