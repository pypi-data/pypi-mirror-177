from bbm import Interval, logging, setup


# 아무것도 설정하지 않았을 시에는 실행하는 python filename이 process_name이 된다.
# 기본 Interval은 1시간
@logging()
def temp_func():
    return "Hello World"


@logging(process_name="custom_name_of_process", interval=Interval.A_DAY)
def temp_func2():
    return "Hello World"


if __name__ == "__main__":
    setup(es_url="https://ps-log.saja.market", index_prefix="batch-process-log")
    temp_func()
    temp_func2()
