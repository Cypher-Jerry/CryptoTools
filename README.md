# CryptoTools
During my time as a postgraduate student, i faced lots of problems searching for crypto tools, thus solving them myself with the help of A.I.

## XOR Filter
using **numpy** as helping hands, main functions and logic are in XORFilter.py.
1. First setup parameters like hashes, these hashes are not the same as BF, since their mapping should share no intersection, in other words, fall into different boundary.
2. With chosen data set, XF_Update will first execute XF_mapping to retrieve the sequence used for inserting into array B.
3. Finally, after update insertion, the array is the output value.

   `Notice, as the parameters are changed, the failure probability to update may vary. The feature of XOR Filter is to move the failure possibility from testing to generating, different from BF`

## OT
using curve_config and OT files, need to install **numpy** and **ecdsa** library before running
1. Sender generate a pair of public/private key using points on Elliptive Curve
2. Receiver receive such $pk:=c\cdot P$, and choose its own secret key k and its choice location
3. A series of value will be sent to Sender, and Sender will use them to combine with his data
4. the combined data are sent back to Receiver for decryption

## ZGBF
a variant from GBF, the existing elements' location will compute zero instead of the true value of element
