import rubikencryptor
from rubikencryptor.rubikencryptor import RubikCubeEncryptor
import numpy as np

def test_rolling_rows():
     A = [[1, 2, 3],
          [4, 5, 6],
          [7, 8, 9]]
     encryptor = RubikCubeEncryptor('encrypted_images/pic1.png')
     encryptor.r = A.copy()
     encryptor.g = A.copy()
     encryptor.b = A.copy()
     encryptor.m = len(encryptor.r)
     encryptor.n = len(encryptor.r[0])
     encryptor.Kr = [605, 371, 646]
     encryptor.Kc = [910, 365, 887]
     encryptor.roll_row()
     encryptor.r = [list(x) for x in encryptor.r]
     assert (encryptor.r == [[2, 3, 1],
                         [6, 4, 5],
                         [9, 7, 8]] )

def test_shifting_columns():
     A = [[1, 2, 3],
          [4, 5, 6],
          [7, 8, 9]]
     encryptor = RubikCubeEncryptor('encrypted_images/pic1.png')
     encryptor.r = A.copy()
     encryptor.g = A.copy()
     encryptor.b = A.copy()
     encryptor.m = len(encryptor.r)
     encryptor.n = len(encryptor.r[0])
     encryptor.Kr = [605, 371, 646]
     encryptor.Kc = [910, 365, 887]
     encryptor.shift_column()
     encryptor.r = [list(x) for x in encryptor.r]
     print(encryptor.r)
     assert (encryptor.r == [[2, 3, 1],
                         [6, 4, 5],
                         [9, 7, 8]] )
