from PIL import Image
from random import randint
import numpy as np
import json
import base64

class RubikCubeCrypto:

	def __init__(self, image: Image) -> None:
		self.image = image.convert('RGB')
		self.rgb_array = np.array(self.image)

		self.r_array, self.g_array, self.b_array = self.rgb_array[:,:,0], self.rgb_array[:,:,1], self.rgb_array[:,:,2]
		self.m, self.n = self.rgb_array.shape[0], self.rgb_array.shape[1]

		self.new_r_array, self.new_g_array, self.new_b_array = np.copy(self.r_array), np.copy(self.g_array), np.copy(self.b_array)  


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
			Filename to store the encryption key ( contains the two geneated vectors Kr, Kc & the iter_max )
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


	def roll_row(self, encrypt_flag: bool = True) -> np.array:
		"""
		Peform the Rolling Rows stage of Rubik Encryption/Decryption

		Parameters
		----------
		encrypt_flag : boolean
			flag indicating whether to perform encryption or decryption
		"""
		direction_multiplier = 1 if encrypt_flag else -1
  
		# For each row of the transpose matrices
		for i in range(self.m):
			rModulus = sum(self.r_array[i]) % 2
			gModulus = sum(self.g_array[i]) % 2
			bModulus = sum(self.b_array[i]) % 2
			
			self.new_r_array[i] = np.roll(self.new_r_array[i],direction_multiplier * -self.Kc[i]) if(rModulus==0) else np.roll(self.new_r_array[i], direction_multiplier * self.Kc[i])
			self.new_g_array[i] = np.roll(self.new_g_array[i],direction_multiplier * -self.Kc[i]) if(gModulus==0) else np.roll(self.new_g_array[i], direction_multiplier * self.Kc[i])
			self.new_b_array[i] = np.roll(self.new_b_array[i],direction_multiplier * -self.Kc[i]) if(bModulus==0) else np.roll(self.new_b_array[i], direction_multiplier * self.Kc[i])

		# if np.sum(self.rgb_array[:,:,0]) == 0:
		# 	self.rgb_array[:,:,0] = np.roll(self.rgb_array[:,:,0], direction_multiplier * self.Kr[i])
		# else:
		# 	self.rgb_array[:,:,0] = np.roll(self.rgb_array[:,:,0], direction_multiplier * self.Kr[i])
			

	def roll_column(self, encrypt_flag: bool = True) -> np.array:
		"""
		Peform the Shifting Columns stage of Rubik Encryption/Decryption

		Parameters
		----------
		encrypt_flag : boolean
			flag indicating whether to perform encryption or decryption
		"""
		direction_multiplier = 1 if encrypt_flag else -1

		for i in range(self.n):
			rModulus = sum(self.new_r_array[:,i]) % 2
			gModulus = sum(self.new_g_array[:,i]) % 2
			bModulus = sum(self.new_b_array[:,i]) % 2
			
			self.new_r_array[:,i] = np.roll(self.new_r_array[:,i],direction_multiplier * -self.Kc[i]) if(rModulus==0) else np.roll(self.new_r_array[:,i], direction_multiplier * self.Kc[i])
			self.new_g_array[:,i] = np.roll(self.new_g_array[:,i],direction_multiplier * -self.Kc[i]) if(gModulus==0) else np.roll(self.new_g_array[:,i], direction_multiplier * self.Kc[i])
			self.new_b_array[:,i] = np.roll(self.new_b_array[:,i],direction_multiplier * -self.Kc[i]) if(bModulus==0) else np.roll(self.new_b_array[:,i], direction_multiplier * self.Kc[i])
  

	def xor_pixels(self, encrypt_flag: bool = True) -> None:
		"""
		Peform the XOR Cells stage of Rubik Encryption/Decryption

		Parameters
		----------
		encrypt_flag : boolean
			flag indicating whether to perform encryption or decryption
		"""
		# For each pixel
		for i in range(self.m):
			for j in range(self.n):
				xor_operand_1 = self.Kc[j] if i%2==1 else self.rotate180(self.Kc[j])
				xor_operand_2 = self.Kr[i] if j%2==0 else self.rotate180(self.Kr[i])
				self.new_r_array[i][j] = self.new_r_array[i][j] ^ xor_operand_1 ^ xor_operand_2
				self.new_g_array[i][j] = self.new_g_array[i][j] ^ xor_operand_1 ^ xor_operand_2
				self.new_b_array[i][j] = self.new_b_array[i][j] ^ xor_operand_1 ^ xor_operand_2


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


	def encrypt(self, output_image: str = 'encrypted_output.png', iter_max: int = 10, alpha: int = 8) -> Image:
		"""
		Peform encryption of the input image

		Parameters
		----------
		iter_max: int
			Maximum number of iterations to perform
		alpha: int
			Hyperparameter needed for vector generation
		"""
		self.create_key(alpha, iter_max)
		for _ in range(iter_max):
			self.roll_row(encrypt_flag = True)
			self.roll_column(encrypt_flag = True)
			self.xor_pixels(encrypt_flag = True)
		for i in range(self.m):
			for j in range(self.n):
				self.pixels[i,j] = (self.r[i][j], self.g[i][j], self.b[i][j])
		new_rgb_array = 
		return Image.fromarray(new_rgb_array)

  
	def decrypt(self, key_filename: str, output_image: str = 'decrypted_output.png') -> Image:
		"""
		Peform decryption of the input image

		Parameters
		----------
		Kr_filename : str
			File storing the vector Kr
		Kc_filename : str
			File storing the vector Kc
		iter_max: int
			Maximum number of iterations to perform
		"""
		new_rgb_array = np.array([])
		self.load_key(key_filename)
		for _ in range(self.iter_max):
			self.xor_pixels(encrypt_flag = False)
			self.roll_column(encrypt_flag = False)
			self.roll_row(encrypt_flag = False)

		for i in range(self.m):
			for j in range(self.n):
				self.pixels[i,j] = (self.r[i][j], self.g[i][j], self.b[i][j])

		self.image.save(output_image)
		return Image.fromarray(new_rgb_array)
		# Image.fromarray(ndarray)

if __name__ == '__main__':
    encryptor = RubikCubeCrypto(Image.open('input/pic1.png'))
    print(encryptor.rgb_array.shape)
    print(encryptor.rgb_array)
    print(encryptor.rgb_array[0].shape)