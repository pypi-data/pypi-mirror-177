from bbm import Interval, logging, setup


# 이런식으로 이름 변경 가능
@logging(process_name="custom_name_of_process", interval=Interval.A_DAY)
def temp_func():
    return "Hello World"


if __name__ == "__main__":
    setup(es_url="https://ps-log.saja.market", index_prefix="batch-process-log")
    temp_func()
