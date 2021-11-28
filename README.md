# Image Cryptography Based on Rubix's Cube Principle

Implementation of image encryption and decryption using Rubix's Cube Principle. This algorithm is based on the paper ["A Secure Image Encryption Algorithm Based on Rubik's Cube Principle"](https://www.hindawi.com/journals/jece/2012/173931/) by Khaled Loukhaoukha, Jean-Yves Chouinard and Abdellah Berdai.

---

## Algorithm Overview

Given an input image having the three R,G,B matrices of size `M X N`
Hyperparameters include 
`α` - used for vector creation
`ITER_MAX` - maximum number of times to carry out operations

#### A. Encyption
1. Create two vectors `Kr` and `Kc` with `|Kr|=M` & `|Kc|=N`. The values of these vectors are randomly picked from 0 to 2<sup>α </sup>-1
2.  Repeat steps 3 to 5 `ITER_MAX` number of times
3. **Rolling Rows:** 
The sum of all pixel values of every row of the image RGB matrices are calculated one by one
if the sum of a given row `rowNumber` is even,
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;we roll the row to the right `Kr[rowNumber]` times
and if the sum is odd
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;we roll the row to the left `Kr[rowNumber]` times
4. **Shifting Columns:** 
The sum of all pixel values of every column of the image RGB matrices are calculated one by one
if the sum of a given row `columnNumber` is even,
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;we shift the column to the up `Kc[columnNumber]` times
and if the sum is odd
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;we roll the column to the left `Kc[columnNumber]` times
5. **XORing Pixels:**
For every pixel(i,j), XOR the pixel with the below two values
I. `Kc[columnNumber]` if `i` is odd else 180 rotated bit version of `Kc[columnNumber]`
II. `Kr[rowNumber]` if `j` is even else 180 rotated bit version of `Kr[rowNumber]`


#### B. Decryption
Decryption just follows the reverse procedure of encryption. 
Given an encrypted image, vectors `Kr` and `Kc` & `ITER_MAX` , 
decryption can be done by XORing pixels(in reverse sequence) → Shifting Columns → Rolling Rows `ITER_MAX` number of times

---

## Encryption Example 
Input image has matrices `R`, `G` and `B` of size 3 X 3
`α` is chosen as 10
`ITER_MAX` is chosen as 1 (for purpose of this example)

Let the matrix R be 

R = $\left[\begin{array}{ccc}
1 & 2 & 3\\
4 & 5 & 6\\
7 & 8 & 9\\
\end{array}\right]$

**Step 1: Vector creation**
Vectors are created by randomly picking between 0 &  2<sup>10</sup>-1
Vr = $\left[\begin{array}{ccc}
605 & 371 & 646\\
\end{array}\right]$

Vc = $\left[\begin{array}{ccc}
910 & 365 & 887\\
\end{array}\right]$

**Step 2: Rolling Rows**

sum(row0) = 1+2+3 = 6 = even → shift row to the right 605(ie- Vr[0]) times
sum(row1) = 4+5+6 = 15 = odd → shift row to the left 371(ie- Vr[1]) times
sum(row2) = 7+8+9 = 24 = even → shift row to the right 646(ie- Vr[2]) times

Hence the matrix now becomes
R` = $\left[\begin{array}{ccc}
2 & 3 & 1\\
5 & 6 & 4\\
9 & 7 & 8\\
\end{array}\right]$

**Step 3: Shifting Columns**

sum(col0) = 2+5+9 = 16 = even → shift column upwards 910(ie- Vc[0]) times
sum(col1) = 3+6+7 = 16 = even → shift to the left 365(ie- Vc[1]) times
sum(col2) = 1+4+8 = 13 = odd → shift to the right 887(ie- Vc[2]) times

Hence the matrix now becomes
R`` = $\left[\begin{array}{ccc}
5 & 7 & 4\\
9 & 3 & 8\\
2 & 6 & 1\\
\end{array}\right]$

**Step 4: XORing Pixels**
Every Row element is XORed as per the rule
pixel(0,0) → pixel(0,0) ⊕ Vr[0] ⊕ rotate180(Vc[0]) = 5 ⊕ 605 ⊕ 455 = 927
pixel(0,1) → pixel(0,1) ⊕ rotate180(Vr[0]) ⊕ Vc[1] = 7 ⊕ 745 ⊕ 365 = 899
...

Hence the matrix now becomes
R``` = $\left[\begin{array}{ccc}
927 & 899 & 482\\
756 & 243 & 524\\
835 & 238 & 316\\
\end{array}\right]$

Same steps are followed for the `G` and `B` matrices as well. The resultant RGB matrices create the encrypted image.

---

## Running 

### Prerequisites

- Python3 ( https://www.python.org/downloads/ )

- Python3 package dependencies ( can be installed using pip3 `pip3 install -r requirements.txt` )


Run the crypto_client script supplying neccessary parameters
```
# python crypto_client.py --help
usage: crypto_client.py [-h] [--type TYPE] [--image IMAGE] [--output_image OUTPUT_IMAGE] [--Krfile KRFILE]
                        [--Kcfile KCFILE]

optional arguments:
  -h, --help            show this help message and exit
  --type TYPE           indicate whether to encrypt or decrypt image
  --image IMAGE         indicate input image path
  --output_image OUTPUT_IMAGE
                        indicate output image path
  --Krfile KRFILE       indicate kr file path(in case of decryption)
  --Kcfile KCFILE       indicate kc file path(in case of encryption)
```

Using python package
```
import rubikencryptor
input_image = 'test.png'

# Encrypt image
encryptor = rubikencryptor.RubikCubeEncryptor(input_image)
encryptor.encrypt(iter_max=10)

# Decrypt image
decryptor = rubikencryptor.RubikCubeEncryptor(input_image)
decryptor.decrypt(Krfile,Kcfile,10)
```
    
