from locust import HttpUser, task, between
from utils.test_records import post_user

jwt_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhZG1pbiIsInJvbGUiOiJhZG1pbiIsImlhdCI6MTYyMjQ3NzE0NSwi' \
            'ZXhwIjoxNjIyOTA5MTQ1fQ.zxPKQWFYDp4kNUgsjEqz_GMovBy15mTvWKkncd8d85Q'
auth_header = {"Authorization": f"Bearer {jwt_token}"}


class QuickstartUser(HttpUser):
    host = "http://localhost:8000"

    # @task
    # def get_token(self):
    #     self.client.post("/token", dict(username="admin", password="admin"))

    @task
    def post_user(self):
        self.client.post("/user/test", json=post_user, headers=auth_header)