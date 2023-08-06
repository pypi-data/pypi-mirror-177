import random
from time import sleep

n = 20
for i in range(n):
    if i == 15:
        raise ValueError("i == 15")
    print(random.random(),flush=True) # Notice: flush=True here is important.
    sleep(1)