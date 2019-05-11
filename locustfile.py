import time
import os
from locust import Locust, TaskSet, events, task
from nifcloud import session

class NifcloudClient(object):
    def __init__(self):
        self.client = session.get_session().create_client(
                        "computing",
                        region_name=os.environ['AWS_DEFAULT_REGION'],
                        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])

    def __getattr__(self, action_name):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                # nifcloud.sessionのAction別のメソッドを作成すると
                # API追加のたびにエンハンスが必要になるためメタプログラミングしている
                execute_method = 'self.client.' + action_name
                response_code = eval(execute_method ,{'self':self})() \
                                    ['ResponseMetadata']['HTTPStatusCode']
                if response_code == 200:
                    total_time = int((time.time() - start_time) * 1000)
                    events.request_success.fire(request_type="Nifcloud",
                                                name=action_name,
                                                response_time=total_time,
                                                response_length=0)
                else:
                    total_time = int((time.time() - start_time) * 1000)
                    events.request_failure.fire(request_type="Nifcloud",
                                                name=action_name,
                                                response_time=total_time,
                                                response_length=0)
            except Exception as e:
                total_time = int((time.time() - start_time) * 1000)
                events.request_failure.fire(request_type="Nifcloud", name=action_name, response_time=total_time, exception=e)
        return wrapper

class NifcloudLocust(Locust):
    def __init__(self, *args, **kwargs):
        super(NifcloudLocust, self).__init__(*args, **kwargs)
        self.client = NifcloudClient()

class NifcloudUser(NifcloudLocust):
    min_wait = 1000
    max_wait = 1000

    class task_set(TaskSet):
        @task
        def describe_instances(self):
            self.client.describe_instances()

        @task
        def describe_volumes(self):
            self.client.describe_volumes()