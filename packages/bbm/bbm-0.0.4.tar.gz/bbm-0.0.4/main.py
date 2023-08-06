import socket
from datetime import datetime
from uuid import uuid4

import pytz
import requests

KST = pytz.timezone("Asia/Seoul")

my_ip = requests.get("http://ipgrab.io").text
hostname = socket.gethostname()


if __name__ == "__main__":
    _LOG_ES_URL = "https://ps-log.saja.market"
    now_kst = datetime.now(tz=KST)
    get_date_to_index = now_kst.strftime("%Y.%m.%d")
    index = f"batch-process-log-{get_date_to_index}"
    datetime_to_write_at_es = now_kst.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
    write_dict = {
        "process": "damon_test.py",
        "func": "main",
        "level": "info",
        "param": {"msg": "check", "cate": "test", "interval": 3600, "uuid": str(uuid4())},
        "ip": my_ip,
        "host": hostname,
        "@timestamp": datetime_to_write_at_es,
    }
    print(write_dict)
    try:
        requests.post(f"{_LOG_ES_URL}/{index}/_doc", json=write_dict)
    except Exception as e:
        print(e)
