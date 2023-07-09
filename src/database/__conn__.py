import boto3


class AWSCONNECT:
    def __init__(self):
        self.REGION: str = ""
        self.BUCKET: str = ""
        self.CLIENTKEY: str = ""
        self.SECRETKEY: str = ""

    def s3_session(self, filePath: str, fileName: str):
        """
        Args:
            filePath: 파일경로
            fileName: 저장될 파일명
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
