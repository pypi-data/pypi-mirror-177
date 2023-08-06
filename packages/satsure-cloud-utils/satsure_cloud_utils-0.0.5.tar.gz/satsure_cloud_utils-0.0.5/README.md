## satsure_cloud_utils

The **satsure_cloud_utils** is a python package that contains all the functionality to browse and navigate aws infrastrucure used in SatSure.

### Documentation

[satsure_cloud_utils Docs](https://docs-satsure-cloud-utils.netlify.app/)

###  Install

```
$ pip install satsure_cloud_utils  
```

### Usage

```
>> from satsure_cloud_utils import Get_s3_handler
>> s3_handler = Get_s3_handler(
    access_key_id = "",
    secret_access_key="",
    session_token=""
)
>> output = s3_handler.get_all_s3_buckets()
>> print(output)
```
