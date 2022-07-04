from multiprocessing import Process
import time



def job1():
    while True:
        print("#######################################")
        time.sleep(1)

def job2():
    while True:
        print("My name is josss")
        time.sleep(2)




if __name__=='__main__':
    J1=Process(target=job1)
    J2 = Process(target=job2)

    J1.start()
    J2.start()