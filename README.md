# locust-for-NIFCLOUD

## Usage

* task_setクラスにパフォーマンスをテストしたいニフクラAPIの定義を追加してから以下を実施

```
$ export AWS_ACCESS_KEY_ID=<Your NIFCLOUD Access Key ID>
$ export AWS_SECRET_ACCESS_KEY=<Your NIFCLOUD Secret Access Key>
$ export AWS_DEFAULT_REGION=jp-east-1
$ locust -H https://jp-east-1.computing.api.nifcloud.com
```

