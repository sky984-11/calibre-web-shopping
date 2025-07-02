# # -*- coding: utf-8 -*-
# # flake8: noqa
# import requests
# from qiniu import Auth
# access_key = 'RegTtVZBKVbu2zp9ARaQ2N12Q8V5l8oaapm1vMwx'
# secret_key = 't6l2lBhrYqJUqv_sOXNFWWpzUtyQA7Jzo9oFCAgv'
# q = Auth(access_key, secret_key)
# base_url = 'http://syr2r6gly.hn-bkt.clouddn.com/metadata.db'
# private_url = q.private_download_url(base_url)

# r = requests.get(private_url)
# if r.status_code == 200:
#     with open('metadata.db', 'wb') as f:
#         f.write(r.content)
#     print("下载成功")
# else:
#     print("下载失败:", r.status_code)

# -*- coding: utf-8 -*-
import requests
from qiniu import Auth, put_file


class QiniuManager:
    def __init__(self, domain):
        self.access_key = 'RegTtVZBKVbu2zp9ARaQ2N12Q8V5l8oaapm1vMwx'
        self.secret_key = 't6l2lBhrYqJUqv_sOXNFWWpzUtyQA7Jzo9oFCAgv'
        self.bucket_name = 'techbooks'
        self.domain = domain if domain.startswith("http") else "http://" + domain
        self.auth = Auth(self.access_key, self.secret_key)

    def download_file(self, file_key, save_path, expires=3600):
        base_url = f'{self.domain}/{file_key}'
        private_url = self.auth.private_download_url(base_url, expires=expires)

        try:
            response = requests.get(private_url, stream=True)
            response.raise_for_status()
            with open(save_path, 'wb') as f:
                f.write(response.content)
            print("✅ 下载成功，保存到:", save_path)
        except requests.RequestException as e:
            print("❌ 下载失败:", e)

    def upload_file(self, local_file_path, file_key):
        token = self.auth.upload_token(self.bucket_name, file_key, 3600)
        ret, info = put_file(token, file_key, local_file_path)
        if info.status_code == 200:
            print(f"✅ 上传成功：{file_key}")
        else:
            print(f"❌ 上传失败：{info}")

# 示例使用
if __name__ == '__main__':
    DOMAIN = 'syr2r6gly.hn-bkt.clouddn.com'

    manager = QiniuManager(DOMAIN)

    mode = input("请选择操作（download/upload）：").strip().lower()

    if mode == 'download':
        file_key = input("请输入文件名（例如 metadata.db）: ").strip()
        save_path = f'./{file_key}'
        manager.download_file(file_key, save_path)

    elif mode == 'upload':
        file_key = input("请输入在七牛上的保存名（例如 images/test.jpg）: ").strip()
        local_path = f'./{file_key}'
        manager.upload_file(local_path, file_key)

    else:
        print("⚠️ 无效操作。请输入 download 或 upload。")