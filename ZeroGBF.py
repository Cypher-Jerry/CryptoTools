import numpy as np
import hashlib
import os
from ZGBF_config import GBF_size,Hash_num



# def ZGBF_Setup():
#     for i in range(Hash_num):

#     return Hashes

def ZGBF_Build(dataset):
    ZGBF_array = np.array([None] * GBF_size, dtype=object)
    for element in dataset:
        hashes = hash_functions(element)
        target = -1
        for loc in hashes:
            if ZGBF_array[loc] is None:
                ZGBF_array[loc] =  np.zeros(16, dtype=np.uint8).tobytes() 
                target = loc
        if (target == -1):
            print("Fail")
            return
        for loc in hashes:
            if loc == target:
                continue
            if ZGBF_array[loc] is None:
                ZGBF_array[loc] = os.urandom(16)
            ZGBF_array[target] = xor_bytes(ZGBF_array[target],ZGBF_array[loc])

    return ZGBF_array

def ZGBF_Test(ZGBF_array,element):
    hashes = hash_functions(element)
    # print(hashes)
    result = np.zeros(16, dtype=np.uint8).tobytes()
    zero_bytes = np.zeros(16, dtype=np.uint8).tobytes()
    for loc in hashes:
        result = xor_bytes(result,ZGBF_array[loc])
    if (result == zero_bytes):
        return True
    return False



def hash_functions(element):
    # 使用 SHA-256 生成一个长哈希值
    hash_value = hashlib.sha256(element.encode()).hexdigest()
    hash_int = int(hash_value, 16)  # 将哈希值转换为整数
    hashes = []
    for i in range(Hash_num):
        # 将哈希值分割成 k 部分
        offset = i * (hash_int.bit_length() // Hash_num)
        partial_hash = (hash_int >> offset) & ((1 << 32) - 1)  # 取 32 位
        hashes.append(partial_hash % GBF_size)  # 取模 m
    return hashes

def xor_bytes(b1: bytes, b2: bytes) -> bytes:
    """
    对两个 bytes 对象进行按位异或操作。
    要求 b1 和 b2 的长度相同。
    """
    if len(b1) != len(b2):
        raise ValueError("bytes 对象的长度必须相同")

    # 将 bytes 转换为 numpy 数组
    arr1 = np.frombuffer(b1, dtype=np.uint8)
    arr2 = np.frombuffer(b2, dtype=np.uint8)

    # 执行异或操作
    result_arr = np.bitwise_xor(arr1, arr2)
    # 将结果转换回 bytes
    return result_arr.tobytes()

if __name__ =="__main__":
    # 示例
    element = ("key","word","identifier","ggs","home","switch")
    ZGBF_array = ZGBF_Build(element)
    for e in element:
        if ZGBF_Test(ZGBF_array,e):
            print("Yes :",e)
        else:
            print("No :",e)