import numpy as np
from XF_Update import xor_bytes

def query_step(H,B,x):
    zero_bytes = np.zeros(16, dtype=np.uint8).tobytes() 
    for index in range(len(H.instances)):
        loc = H.get_instance(index).digest(x)
        value = B[loc]
        zero_bytes = xor_bytes(zero_bytes,value)
    return zero_bytes