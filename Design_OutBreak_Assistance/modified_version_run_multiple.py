import database_test
import modified_Version_2new
from multiprocessing import Process

import subprocess

subprocess.run("python3 database_test.py & python3 modified_Version_2new.py", shell=True)
def fun1():
    database_test.function()
def fun2():
    modified_Version_2new.function()

