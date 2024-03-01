 
from config import Config
import oss2
import os

class OSSClient:
    
    def __init__(self):
        self.config = Config()
        self.static_type = self.config.get("static_type")
        if self.static_type != "oss":
            return
    
        self.ossConfig = self.config.get("oss")
        # 初始化身份验证
        self.auth = oss2.Auth(self.ossConfig["ID"], self.ossConfig["Secret"])
        # 初始化Bucket
        self.bucket = oss2.Bucket(self.auth, self.ossConfig["Endpoint"], self.ossConfig["Bucket"])

        if not self.test_bucket():
            print("OSS Bucket上传测试失败，请检查配置是否正确")

    def test_bucket(self) -> bool:
        try:
            self.bucket.put_object("BUCKET_TEST_FILE", b"Test File")
            test_object = self.bucket.get_object("BUCKET_TEST_FILE")
            self.bucket.delete_object("BUCKET_TEST_FILE")
        except oss2.exceptions.ServerError:
            return False
        return test_object.read() == b"Test File"


    def upload_file(self, local_file: str) -> str:
        """OSS上传文件

        :param local_file: 本地文件的路径
        :return: 上传对象的OSS链接
        """
        file_name = os.path.basename(local_file)
        self.bucket.put_object_from_file(os.path.join(self.ossConfig["Directory"], file_name), local_file,
                                    headers={"Content-Type": f"image/{self.config['oss']['Image_Format']}"})
        return self.ossConfig["Link"] + "/" + self.ossConfig["Directory"] + file_name

