import os
import time

start_distributed = time.time()
os.system("mpiexec -np 4 python ford_fulkerson_distributed.py")
end_distributed = time.time()


start_regular = time.time()
os.system("python ford_fulkerson_regular.py")
end_regular = time.time()

time_distributed = (end_distributed - start_distributed) * 1000
time_regular = (end_regular - start_regular) * 1000
print(f"Vrijeme distribuiranog ford - fulkersonovog algoritma je: {time_distributed} ms", )
print(f"Vrijeme regularnog ford - fulkersonovog algoritma je: {time_regular} ms", )
