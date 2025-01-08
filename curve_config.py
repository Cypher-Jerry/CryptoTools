from ecdsa import SECP256k1

# Define the SECP256k1 curve globally in this module
SECP256k1_CURVE = SECP256k1.curve
base_point = SECP256k1.generator
p = SECP256k1_CURVE.p() #order of curve