import hmac
import hashlib
import os

class updatable_PRF:
    def __init__(self):
        self.key = os.urandom(32)
        self.hashtype = 'sha256'
    def digest(self,message:bytes)-> bytes: 
        assert(type(message)==bytes)
        h=hmac.new(self.key,message,self.hashtype)
        return h.digest()[:16]


class keyed_hash:
#根据输入的类型判断是普通的hash或者keyed hash，相当于把两类哈希合为一类了，如此甚至只需要两个对象就能实现四个哈希的功能
#再补了个切割的功能，输入128就能得到16字节的结果（分片
    def __init__(self,partition:list,par=128):
        self.salt = os.urandom(32)
        self.hashtype = 'sha256'
        self.interval = partition
        assert (par==128 or par ==256)
        self.parameter = par 

    def digest(self, message:bytes , key = 'default'):

        if (key == 'default'):
            assert(type(message) == bytes)
            h = hmac.new(self.salt, message, self.hashtype)
            if self.parameter == 256:
                return self.hash_to_interval(h.digest())
            else:
                return self.hash_to_interval(h.digest()[:self.parameter//8])
        else:

            assert(len(key) == 32 and type(message) == bytes)
            h = hmac.new(key, message, self.hashtype)
            if self.parameter == 256:
                return self.hash_to_interval(h.digest())
            else:
                return self.hash_to_interval(h.digest()[:self.parameter//8])

    def hash_to_interval(self,value:bytes):
        piece = self.interval[1]-self.interval[0]
        result = int.from_bytes(value, byteorder='big')%piece
        result = result + self.interval[0]
        return result

class InstanceManager:
    def __init__(self, cls=keyed_hash):
        """
        初始化一个管理类，用于动态管理指定类的实例。
        
        参数:
            cls (type): 要管理的类。
        """
        self.cls = cls
        self.instances = []

    def create_instances(self, count:int,s:int):
        """
        批量创建实例并存储。
        
        参数:
            count (int): 要创建的实例数量。
        """
        if count <= 0:
            raise ValueError("实例数量必须是正整数")
        assert(s%count==0)
        section = s//count
        lower_bound = 0
        upper_bound = 0+section
        for i in range(count):
            bound = [lower_bound,upper_bound]
            instance = self.cls(bound)
            self.instances.append(instance)
            lower_bound =lower_bound+section
            upper_bound = upper_bound+section
            

    def get_instance(self, index):
        """
        根据索引获取实例。
        
        参数:
            index (int): 实例索引（从 0 开始）。
        
        返回:
            object: 索引对应的实例。
        """
        if 0 <= index < len(self.instances):
            return self.instances[index]
        else:
            raise IndexError("索引超出范围")

    def list_instances(self):
        """
        列出所有已创建的实例。
        
        返回:
            list: 所有实例的字符串表示。
        """
        return [f"Instance {i}: {repr(instance)}" for i, instance in enumerate(self.instances)]


# 示例用法
if __name__ == "__main__":
    manager = InstanceManager()

    # 创建 5 个实例
    manager.create_instances(3,9)

    # 列出所有实例
    print("所有实例：")
    for item in manager.list_instances():
        print(item)

    # 获取并使用某个实例
    test_message = b"Hello World!"
    print("\n选择的实例：")
    instance = manager.get_instance(0)
    print(instance.digest(test_message))
    instance = manager.get_instance(1)
    print(instance.digest(test_message))
    instance = manager.get_instance(2)
    print(instance.digest(test_message))



