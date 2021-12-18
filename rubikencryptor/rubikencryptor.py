from PIL import Image
from random import randint
import numpy as np
import json
import base64

class RubikCubeCrypto:

	def __init__(self, image: Image) -> None:
		self.image = image.convert('RGB')
		self.rgb_array = np.array(self.image)
		self.new_rgb_array = np.copy(self.rgb_array)
		self.m, self.n = self.rgb_array.shape[0], self.rgb_array.shape[1]


	def create_key(self, alpha: float, iter_max: int, key_filename: str ='key.txt') -> None:
		"""
		Create the two vectors using the value alpha
			- Vector Kr - M elements randomnly picked b/w 0 and 2^alpha - 1
			- Vector Kc - N elements randomnly picked b/w 0 and 2^alpha - 1

		Parameters
		----------
		alpha : 
			hyperparameter alpha which is used in generarting the two vectors
		iter_max : int
			Maximum number of iterations to perform
		key_filename : str
			Filename to store the encryption key ( contains the two generated vectors Kr, Kc & the iter_max )
		"""
		self.Kr = [randint(0,pow(2,alpha)-1) for i in range(self.m)]
		self.Kc = [randint(0,pow(2,alpha)-1) for i in range(self.n)]
		self.iter_max = iter_max

		key_dict = {
					"Kr": self.Kr, 
					"Kc": self.Kc, 
					"iter_max": iter_max
					}

		serialized_key_dict = json.dumps(key_dict)
		encoded_key = base64.b64encode(serialized_key_dict.encode())
		with open(key_filename, "wb") as binary_file:
			binary_file.write(encoded_key)
		

	def load_key(self, key_filename: str) -> None:
		"""
		Load the two vectors Kr, Kc and the iter_max from the key file provided

		Parameters
		----------
		key_filename : str
			Key File generated from encryption
		"""
		with open(key_filename, 'r') as keyfile:
			data = keyfile.read()
			decoded_key = base64.b64decode(data).decode()
			decoded_dict = json.loads(decoded_key)
			self.Kr = decoded_dict["Kr"]
			self.Kc = decoded_dict["Kc"]
			self.iter_max = decoded_dict["iter_max"]


	def roll_row(self, encrypt_flag: bool = True) -> None:
		"""
		Peform the Rolling Rows stage of Rubik Encryption/Decryption

		Parameters
		----------
		encrypt_flag : boolean
			flag indicating whether to perform encryption or decryption
		"""
		direction_multiplier = 1 if encrypt_flag else -1
  
		# For each row of the matrices
		for i in range(self.m):
			rModulus = np.sum(self.new_rgb_array[i,:,0]) % 2
			gModulus = np.sum(self.new_rgb_array[i,:,1]) % 2
			bModulus = np.sum(self.new_rgb_array[i,:,2]) % 2
			   
			self.new_rgb_array[i,:,0] = np.roll(self.new_rgb_array[i,:,0], direction_multiplier * -self.Kc[i]) if(rModulus==0) \
											else np.roll(self.new_rgb_array[i,:,0], direction_multiplier * self.Kc[i])
			self.new_rgb_array[i,:,1] = np.roll(self.new_rgb_array[i,:,1], direction_multiplier * -self.Kc[i]) if(gModulus==0) \
											else np.roll(self.new_rgb_array[i,:,1], direction_multiplier * self.Kc[i])
			self.new_rgb_array[i,:,2] = np.roll(self.new_rgb_array[i,:,2], direction_multiplier * -self.Kc[i]) if(bModulus==0) \
											else np.roll(self.new_rgb_array[i,:,2], direction_multiplier * self.Kc[i])


	def roll_column(self, encrypt_flag: bool = True) -> None:
		"""
		Peform the Shifting Columns stage of Rubik Encryption/Decryption

		Parameters
		----------
		encrypt_flag : boolean
			flag indicating whether to perform encryption or decryption
		"""
		direction_multiplier = 1 if encrypt_flag else -1

		for i in range(self.n):
			rModulus = np.sum(self.new_rgb_array[:,i,0]) % 2
			gModulus = np.sum(self.new_rgb_array[:,i,1]) % 2
			bModulus = np.sum(self.new_rgb_array[:,i,2]) % 2

			self.new_rgb_array[:,i,0] = np.roll(self.new_rgb_array[:,i,0], direction_multiplier * -self.Kc[i]) if(rModulus==0) \
											else np.roll(self.new_rgb_array[:,i,0], direction_multiplier * self.Kc[i])
			self.new_rgb_array[:,i,1] = np.roll(self.new_rgb_array[:,i,1], direction_multiplier * -self.Kc[i]) if(gModulus==0) \
											else np.roll(self.new_rgb_array[:,i,1], direction_multiplier * self.Kc[i])
			self.new_rgb_array[:,i,2] = np.roll(self.new_rgb_array[:,i,2], direction_multiplier * -self.Kc[i]) if(bModulus==0) \
											else np.roll(self.new_rgb_array[:,i,2], direction_multiplier * self.Kc[i])


	def xor_pixels(self) -> None:
		"""
		Peform the XOR Cells stage of Rubik Encryption/Decryption
		"""
		# For each pixel
		for i in range(self.m):
			for j in range(self.n):
				xor_operand_1 = self.Kc[j] if i%2==1 else self.rotate180(self.Kc[j])
				xor_operand_2 = self.Kr[i] if j%2==0 else self.rotate180(self.Kr[i])
				self.new_rgb_array[i,j,0] = self.new_rgb_array[i,j,0] ^ xor_operand_1 ^ xor_operand_2
				self.new_rgb_array[i,j,1] = self.new_rgb_array[i,j,1] ^ xor_operand_1 ^ xor_operand_2
				self.new_rgb_array[i,j,2] = self.new_rgb_array[i,j,2] ^ xor_operand_1 ^ xor_operand_2


	def rotate180(self, n: int) -> int:
		"""
		Peform complete 180 Bit Rotation of number
		( eg - decimal 11 (1011 in binary) becomes decimal 13(1101 in binary) )

		Parameters
		----------
		n: int
			number on which to perform 180 bit rotation
		Returns
		-------
		int
			number obtained on performing 180 bit rotation of given number
		"""
		bits = "{0:b}".format(n)
		return int(bits[::-1], 2)


	def encrypt(self, alpha: int = 8, iter_max: int = 10, key_filename: str = 'key.txt') -> Image:
		"""
		Peform encryption of the input image

		Parameters
		----------
		iter_max: int
			Maximum number of iterations to perform
		alpha: int
			Hyperparameter needed for vector generation
   		key_filename : str
			Filename to store the encryption key ( contains the two generated vectors Kr, Kc & the iter_max )
		"""
		self.create_key(alpha, iter_max, key_filename)
		for _ in range(iter_max):
			self.roll_row(encrypt_flag = True)
			self.roll_column(encrypt_flag = True)
			self.xor_pixels()

		new_image = Image.fromarray(self.new_rgb_array.astype(np.uint8))
		return new_image

  
	def decrypt(self, key_filename: str) -> Image:
		"""
		Peform decryption of the input image

		Parameters
		----------
		key_filename : str
			Key file generated from encryption ( contains the two generated vectors Kr, Kc & the iter_max )
		iter_max: int
			Maximum number of iterations to perform
		"""
		self.load_key(key_filename)
		for _ in range(self.iter_max):
			self.xor_pixels()
			self.roll_column(encrypt_flag = False)
			self.roll_row(encrypt_flag = False)

		new_image = Image.fromarray(self.new_rgb_array.astype(np.uint8))
		return new_image

