```
pip3 install --trusted-host 3.83.66.248 --index-url http://3.83.66.248:8080 censiuslogs
```
You can then start using the Python package as 


```
from censiuslogs.client import Client

c = Client(api_key='lczhlzobdvwrrwechlzsvbzselirtsxk')

data = {
    "model_id": 2,
    "user_defined_model_id": "11a2cb",
    "feature_event": {"smoething": 1},
    "event_type": "something",
    "feature_prediction": {"somePrediction": 1},
    "actuals": {"someActuals": "wo"},
    "proc_feature_event": [1, 2],
    "model_version": "v1",
    "feature_actuals": {"actual": 1}
}

c.add_logs(data=data)
```


```
from censiuslogs.client import Client

c = Client(api_key='lczhlzobdvwrrwechlzsvbzselirtsxk')

data = [{
    "model_id": 2,
    "user_defined_model_id": "11a2cb",
    "feature_event": "{\"smoething\": 1}",
    "event_type": "something",
    "feature_prediction": "{\"somePrediction\": 1}",
    "actuals": "{\"someActuals\": \"wo\"}"
},{
    "model_id": 2,
    "user_defined_model_id": "11a2cb",
    "feature_event": "{\"smoething\": 1}",
    "event_type": "something",
    "feature_prediction": "{\"somePrediction\": 1}",
    "actuals": "{\"someActuals\": \"wo\"}"
}]

c.add_batch_logs(all_events=data)
```


```
from censiuslogs.client import Client

c = Client(api_key='lczhlzobdvwrrwechlzsvbzselirtsxk')

data={
    "log_id": "061cd5bb-a8c8-4343-bedb-7ebe5f15d499",
    "actuals": "{\"someActuals\": \"wo\"}"
}

c.update_actuals(data=data)
```