from yzcore.extensions.storage.base import StorageManagerBase


class MinioManager(StorageManagerBase):
    def create_bucket(self, bucket_name):
        pass

    def get_bucket_cors(self):
        pass

    def list_buckets(self):
        pass

    def is_exist_bucket(self, bucket_name=None):
        pass

    def delete_bucket(self, bucket_name=None):
        pass

    def get_sign_url(self, key, expire=0):
        pass

    def post_sign_url(self, key):
        pass

    def put_sign_url(self, key):
        pass

    def iter_objects(self, prefix='', marker=None, delimiter=None, max_keys=100):
        pass

    def get_object_meta(self, key: str):
        pass

    def update_file_headers(self, key, headers: dict):
        pass

    def download(self, key, local_name=None, is_stream=False, **kwargs):
        pass

    def upload(self, *args, **kwargs):
        pass

    def get_policy(self, filepath: str, callback_url: str, callback_data: dict = None,
                   callback_content_type: str = "application/json"):
        pass