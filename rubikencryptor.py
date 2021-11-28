from PIL import Image
from random import randint
import numpy
import json

class RubikCubeEncryptor:

	def __init__(self, image_name):
		self.image = Image.open(image_name)
		self.pixels = self.image.load()
		self.m = self.image.size[0]
		self.n = self.image.size[1]
		self.r = []
		self.g = []
		self.b = []
		self.load_rgb_matrix()

	def load_rgb_matrix(self):
		"""
		Loads the Red(R), Green(G) & Blue(B) Matrices of the input image
		"""
		for i in range(self.m):
			self.r.append([])
			self.g.append([])
			self.b.append([]) 
			for j in range(self.n):
				rgbPerPixel = self.pixels[i,j]
				self.r[i].append(rgbPerPixel[0])
				self.g[i].append(rgbPerPixel[1])
				self.b[i].append(rgbPerPixel[2])

	def create_vectors(self, alpha, Kr_filename='Kr.txt', Kc_filename='Kc.txt'):
		"""
		Create the two vectors using the value alpha
			- Vector Kr - M elements randomnly picked b/w 0 and 2^alpha - 1
			- Vector Kc - N elements randomnly picked b/w 0 and 2^alpha - 1

		Parameters
		----------
		alpha : integer
			hyperparameter alpha which is used in generarting the two vectors
		Kr_filename : string
			Filename to store the vector Kr
		Kc_filename : string
			Filename to store the vector Kc
		"""
		self.Kr = [randint(0,pow(2,alpha)-1) for i in range(self.m)]
		Kr_file = open(Kr_filename,'w+')
		Kr_file.write(str(self.Kr))		

		self.Kc = [randint(0,pow(2,alpha)-1) for i in range(self.n)]
		Kc_file = open(Kc_filename,'w+')
		Kc_file.write(str(self.Kc))
   
	def load_vectors(self, Kr_filename, Kc_filename):
		"""
		Load the two vectors Kr and Kc from the input files provided

		Parameters
		----------
		Kr_filename : string
			File storing the vector Kr
		Kc_filename : string
			File storing the vector Kc
		"""
		Kr_file = open(Kr_filename,'r')
		self.Kr = json.loads(Kr_file.readline())

		Kc_file = open(Kc_filename,'r')
		self.Kc = json.loads(Kc_file.readline())

	def roll_row(self, encrypt_flag=True):
		"""
		Peform the Rolling Rows stage of Rubik Encryption/Decryption

		Parameters
		----------
		encrypt_flag : boolean
			flag indicating whether to perform encryption or decryption
		"""
		direction_multiplier = 1 if encrypt_flag else -1
  		# For each row
		for i in range(self.m):
			rModulus = sum(self.r[i]) % 2
			gModulus = sum(self.g[i]) % 2
			bModulus = sum(self.b[i]) % 2
			
			self.r[i] = numpy.roll(self.r[i],direction_multiplier * self.Kr[i]) if(rModulus==0) else numpy.roll(self.r[i], direction_multiplier * -self.Kr[i])
			self.g[i] = numpy.roll(self.g[i],direction_multiplier * self.Kr[i]) if(gModulus==0) else numpy.roll(self.g[i], direction_multiplier * -self.Kr[i])
			self.b[i] = numpy.roll(self.b[i],direction_multiplier * self.Kr[i]) if(bModulus==0) else numpy.roll(self.b[i], direction_multiplier * -self.Kr[i])


	def shift_column(self, encrypt_flag=True):
		"""
		Peform the Shifting Columns stage of Rubik Encryption/Decryption

		Parameters
		----------
		encrypt_flag : boolean
			flag indicating whether to perform encryption or decryption
		"""
		for i in range(self.n):
			rTotalSum = 0
			gTotalSum = 0
			bTotalSum = 0
			for j in range(self.m):
				rTotalSum += self.r[j][i]
				gTotalSum += self.g[j][i]
				bTotalSum += self.b[j][i]
			rModulus = rTotalSum % 2
			gModulus = gTotalSum % 2
			bModulus = bTotalSum % 2
			if(encrypt_flag):
				if(rModulus==0):
					self.upshift(self.r,i,self.Kc[i])
				else:
					self.downshift(self.r,i,self.Kc[i])
				if(gModulus==0):
					self.upshift(self.g,i,self.Kc[i])
				else:
					self.downshift(self.g,i,self.Kc[i])
				if(bModulus==0):
					self.upshift(self.b,i,self.Kc[i])
				else:
					self.downshift(self.b,i,self.Kc[i])
			else:
				if(rModulus==0):
					self.downshift(self.r,i,self.Kc[i])
				else:
					self.upshift(self.r,i,self.Kc[i])
				if(gModulus==0):
					self.downshift(self.g,i,self.Kc[i])
				else:
					self.upshift(self.g,i,self.Kc[i])
				if(bModulus==0):
					self.downshift(self.b,i,self.Kc[i])
				else:
					self.upshift(self.b,i,self.Kc[i])


	def xor_pixels(self, encrypt_flag=True):
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
				self.r[i][j] = self.r[i][j] ^ xor_operand_1 ^ xor_operand_2
				self.g[i][j] = self.g[i][j] ^ xor_operand_1 ^ xor_operand_2
				self.b[i][j] = self.b[i][j] ^ xor_operand_1 ^ xor_operand_2


	def upshift(self, a, index, n):
		"""
		Peform Matrix Upshift operation

		Parameters
		----------
		a : List
			matrix to perform upshift operation on
		index: integer
			column on which to perform the upshift
		n: integer
			number of times to perform the shift
		"""
		col = []
		for j in range(len(a)):
			col.append(a[j][index])
		shiftCol = numpy.roll(col,-n)
		for i in range(len(a)):
			for j in range(len(a[0])):
				if(j==index):
					a[i][j] = shiftCol[i]

	def downshift(self, a, index, n):
		"""
		Peform Matrix Downshift operation

		Parameters
		----------
		a : List
			matrix to perform downshift operation on
		index: integer
			column on which to perform the downshift
		n: integer
			number of times to perform the shift
		"""
		col = []
		for j in range(len(a)):
			col.append(a[j][index])
		shiftCol = numpy.roll(col,n)
		for i in range(len(a)):
			for j in range(len(a[0])):
				if(j==index):
					a[i][j] = shiftCol[i]

	def rotate180(self, n):
		"""
		Peform complete 180 Bit Rotation of number
		( eg - decimal 11 (1011 in binary) becomes decimal 13(1101 in binary) )

		Parameters
		----------
		n: integer
			number on which to perform 180 bit rotation
		Returns
		-------
		Integer
			number obtained on performing 180 bit rotation of given number
		"""
		bits = "{0:b}".format(n)
		return int(bits[::-1], 2)

	def encrypt(self, output_image='encrypted_output.png', iter_max=10, alpha = 8):
		"""
		Peform encryption of the input image

		Parameters
		----------
		iter_max: integer
			Maximum number of iterations to perform
		alpha: integer
			Hyperparameter needed for vector generation
		"""
		self.create_vectors(alpha)
		for iterations in range(iter_max):
			self.roll_row(encrypt_flag = True)
			self.shift_column(encrypt_flag = True)
			self.xor_pixels(encrypt_flag = True)
		for i in range(self.m):
			for j in range(self.n):
				self.pixels[i,j] = (self.r[i][j], self.g[i][j], self.b[i][j])

		self.image.save(output_image)
  
	def decrypt(self, Kr_filename, Kc_filename, output_image='decrypted_output.png', iter_max=10):
		"""
		Peform decryption of the input image

		Parameters
		----------
		Kr_filename : string
			File storing the vector Kr
		Kc_filename : string
			File storing the vector Kc
		iter_max: integer
			Maximum number of iterations to perform
		"""
		self.load_vectors(Kr_filename, Kc_filename)
		for iterations in range(iter_max):
			self.xor_pixels(encrypt_flag = False)
			self.shift_column(encrypt_flag = False)
			self.roll_row(encrypt_flag = False)

		for i in range(self.m):
			for j in range(self.n):
				self.pixels[i,j] = (self.r[i][j], self.g[i][j], self.b[i][j])

		self.image.save(output_image)
