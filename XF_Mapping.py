from collections import deque

def mapping_step(H, S, b):
    Stack = deque()
    Queue = deque()
    T = [set() for _ in range(b)]  # 初始化哈希表 T

    # 填充哈希表
    for x in S:
        for index in range(len(H.instances)):
            h=H.get_instance(index)
            T[h.digest(x)].add(x)

    # 初始化队列
    for i in range(b):
        if len(T[i]) == 1:
            Queue.append(i)

    # 处理队列
    while Queue:
        i = Queue.popleft()
        try:
            x = T[i].pop()
        except KeyError:
            # print(f"桶 T[{i}] 为空，跳过处理")
            continue
        Stack.append((x, i))  # 压入栈
        for index in range(len(H.instances)):
            h=H.get_instance(index)
            bucket = h.digest(x)
            if x in T[bucket]:
                T[bucket].remove(x)
                if len(T[bucket]) == 1:
                    Queue.append(bucket)

    # 验证映射
    if len(Stack) != len(S):
        return False, None
    # print(Stack)
    return True, Stack