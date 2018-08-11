from multiprocessing import Process
import time


def A():
    while True:
        print('正在调用函数')
        time.sleep(1)  # 推迟执行的秒数


p = Process(target=A)  # 创建进程对象,并指定进程将来要执行的函数.
# p.start()  # 启动进程.
