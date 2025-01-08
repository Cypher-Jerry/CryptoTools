#首先，将哈希个数与Array长度确定下来，并生成那么多的哈希
#接着，在Update的时候，将F作为输入，而不再是确定的值
from XF_Setup import InstanceManager,updatable_PRF
from XF_Update import update_step,xor_bytes
from XF_Query import query_step

if __name__=="__main__":
    hash_num = 3
    array_length = 12
    Input_Element_Set = (b"key",b"word",b"identifier",b"ggs",b"home",b"switch")
    Manager = InstanceManager()
    Manager.create_instances(hash_num,array_length)
    F = updatable_PRF()
    B = update_step(Manager,F,Input_Element_Set,array_length)
    for e in Input_Element_Set:
        print(f"Key {e}:")
        print(F.digest(e))
        print(query_step(Manager,B,e))
