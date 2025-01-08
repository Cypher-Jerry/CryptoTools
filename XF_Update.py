from XF_Mapping import mapping_step
import numpy as np
import os

def update_step(H,F,S,array_length:int):
    Mark,Stack = mapping_step(H,S,array_length)
    if Mark == False:
        print("False")
        return
    #得到插入顺序
    xor_array = np.array([None] * array_length, dtype=object)
    # print("Initialized Size")
    # print(len(xor_array[1]))
    #初始化array D
    while Stack:
        x,i = Stack.pop()
        # 按顺序将值进行插入操作
        xor_array[i] = F.digest(x)

        # print(len(F.digest(x)))
        for index in range(len(H.instances)):
            h = H.get_instance(index)
            other_bucket = h.digest(x)
            if other_bucket != i:
                if xor_array[other_bucket] is None:
                    # 随机生成一个符合参数长度的随机值
                    xor_array[other_bucket] = os.urandom(16)
                # 异或操作
                xor_array[i] = xor_bytes(xor_array[i],xor_array[other_bucket])

    # Step 3: 处理未初始化的 B[j]
    for j in range(array_length):
        if xor_array[j] is None:
            xor_array[j] = os.urandom(16)

    # Step 4: 返回更新后的 B
    return xor_array


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

# # 示例
# b1 = b'\x01\x02\x03'
# b2 = b'\x03\x02\x01'
# result = xor_bytes(b1, b2)
# print(result)  # 输出: b'\x02\x00\x02'
if __name__=="__main__":
    b1 = os.urandom(16)
    b2 = os.urandom(16)
    print(len(xor_bytes(b1,b2)))