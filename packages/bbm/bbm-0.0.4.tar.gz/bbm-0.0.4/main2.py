from bbm import Interval, logging, setup


@logging()
def temp_func():
    return "Hello World"


if __name__ == "__main__":
    setup(es_url="https://ps-log.saja.market", index_prefix="batch-process-log")
    temp_func()
