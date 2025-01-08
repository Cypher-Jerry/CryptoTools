import math

def calculate_bloom_filter_parameters(n, epsilon):
    """
    计算 Garbled Bloom Filter 的位数组大小 (m) 和哈希函数数量 (k)。

    参数:
        n (int): 集合中元素的数量。
        epsilon (float): 目标误报率（例如 0.01 表示 1%）。

    返回:
        m (int): 位数组大小（比特数）。
        k (int): 哈希函数数量。
    """
    # 计算位数组大小 m
    m = - (n * math.log(epsilon)) / (math.log(2) ** 2)
    m = int(math.ceil(m))  # 向上取整，确保 m 是整数

    # 计算哈希函数数量 k
    k = (m / n) * math.log(2)
    k = int(math.ceil(k))  # 向上取整，确保 k 是整数

    return m, k

# 示例用法
n = 6  # 集合中元素数量
epsilon = 0.001  # 目标误报率 1%

GBF_size, Hash_num = calculate_bloom_filter_parameters(n, epsilon)
print(f"位数组大小 : {GBF_size} 比特")
print(f"哈希函数数量 : {Hash_num}")