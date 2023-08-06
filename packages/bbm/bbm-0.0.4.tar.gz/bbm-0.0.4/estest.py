from bbm.utils import get_data_from_es

if __name__ == "__main__":
    dql = "param.msg:start OR param.msg:complete"
    response = get_data_from_es(dql, num=10, es_index="batch-process-log-*", es_url="https://ps-log.saja.market")
    print(response)
