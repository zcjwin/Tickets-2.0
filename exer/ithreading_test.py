from threading import Thread
import time,sys,os

def test(i):
    print("%s 开始执行" % i)
    while True:
        print("%s 循环执行" % i)
        time.sleep(1)
        if i > 18:
            os._exit(i)

def main():
    for i in range(10,20):
        Thread_name = Thread(target=test,args=(i,))
        # Thread_name.setDaemon(True)
        Thread_name.start()

def sys_test():
    try:
        sys.exit()
    except Exception as err:
        print(err)
    time.sleep(10)


if __name__ == '__main__':
    # main()
    sys_test()