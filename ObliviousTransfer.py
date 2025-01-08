from ecdsa import ellipticcurve
from ecdsa.ellipticcurve import Point
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from curve_config import SECP256k1_CURVE,base_point,p
import secrets
import random
import hashlib

def Aes_Encrypt(key,message):
    cipher = AES.new(key,AES.MODE_CBC)
    iv = cipher.iv
    padded_message = pad(message, AES.block_size)
    encrypted_value =  cipher.encrypt(padded_message)
    return encrypted_value,iv

def Aes_Decrypt(key,iv,ciphertext):
    cipher = AES.new(key,AES.MODE_CBC,iv)
    padded_message = cipher.decrypt(ciphertext)
    message = unpad(padded_message,AES.block_size)
    return message


#OT
def KeyGen():                 #Sender choose SK:c/PK:cG and send to Receiver
    private_c = secrets.randbelow(p - 1) + 1  # Ensure the range is from 1 to n-1
    public_c = private_c * base_point
    return public_c

def QueryGen(public_c,choice,temp_key):        #Receiver choose random k, choice b
    private_k = temp_key
    public_k = private_k * base_point

    # Compute the point to negate using the choice and the public key
    temp_point = (choice-1) * public_c
    x_p = temp_point.x()
    y_p = temp_point.y()

    # Compute the negative of the point (x, -y mod p)
    y_neg_p = (-y_p) % p
    
    # Create the negative point (-P)
    neg_P = ellipticcurve.Point(SECP256k1_CURVE, x_p, y_neg_p)

    PK_0 = public_k + neg_P
    return PK_0,private_k

def Response(public_c,query,data:list):
    length = len(data)
    PK = {}
    response = {}
    PK[0] = query

    for i in range(1,length):
        PK[i] = PK[i-1]+public_c
    for i in range(length):
        random_value = random.randint(0,1000)
        hash_value = hash_point(random_value * PK[i])
        public_random = random_value * base_point
        encrypted_value,iv = Aes_Encrypt(hash_value,data[i])
        response[i] = [public_random,encrypted_value,iv]
    return response 

def Extract(response,private_k,choice):
    public_random,encrypted_value,iv = response[choice-1]
    hash_value = hash_point(public_random * private_k)
    result = Aes_Decrypt(hash_value,iv,encrypted_value)
    print (result)
    return result

def hash_point(P: Point) -> bytes:
    """
    Hash an elliptic curve point to a fixed-length byte string (using SHA-256).
    
    Args:
    - P: The elliptic curve point to be hashed.
    
    Returns:
    - A 32-byte hash of the elliptic curve point.
    """
    # Check for point at infinity (optional)
    if P.x() is None or P.y() is None:
        return hashlib.sha256(b"point_at_infinity").digest()
    
    # Serialize the coordinates of the point (x and y as bytes)
    x_bytes = P.x().to_bytes(32, byteorder='big')
    y_bytes = P.y().to_bytes(32, byteorder='big')
    
    # Concatenate the coordinates
    point_bytes = x_bytes + y_bytes
    
    # Hash the concatenated bytes using SHA-256
    return hashlib.sha256(point_bytes).digest()



if __name__=="__main__":
    # Sender Setup
    public_c = KeyGen()
    data =  (b"key",b"word",b"identifier",b"ggs",b"home",b"switch")

    # Receiver Choose and Generate Query
    choice = 2
    PK_0,private_k = QueryGen(public_c,choice,7)

    # Sender compute responses
    response = Response(public_c,PK_0,data)

    # Receiver locally decrypt
    result = Extract(response,private_k,choice)