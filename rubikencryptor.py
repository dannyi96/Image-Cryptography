from PIL import Image
from random import randint
import numpy
import sys
import json
import argparse

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
		for i in range(self.m):
			self.r.append([])
			self.g.append([])
			self.b.append([]) 
			for j in range(self.n):
				rgbPerPixel = self.pixels[i,j]
				self.r[i].append(rgbPerPixel[0])
				self.g[i].append(rgbPerPixel[1])
				self.b[i].append(rgbPerPixel[2])

	def create_vectors(self, alpha):
		self.Kr = [randint(0,pow(2,alpha)-1) for i in range(self.m)]
		Kr_file = open('Kr.txt','w+')
		Kr_file.write(str(self.Kr))		

		self.Kc = [randint(0,pow(2,alpha)-1) for i in range(self.n)]
		Kc_file = open('Kc.txt','w+')
		Kc_file.write(str(self.Kc))
   
	def load_vectors(self, Kr_filename, Kc_filename):
		Kr_file = open(Kr_filename,'r')
		self.Kr = json.loads(Kr_file.readline())

		Kc_file = open(Kc_filename,'r')
		self.Kc = json.loads(Kc_file.readline())

	def roll_row(self, encrypt_flag=True):
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
		if encrypt_flag:
			# For each row
			for i in range(self.m):
				for j in range(self.n):
					if(i%2==1):
						self.r[i][j] = self.r[i][j] ^ self.Kc[j]
						self.g[i][j] = self.g[i][j] ^ self.Kc[j]
						self.b[i][j] = self.b[i][j] ^ self.Kc[j]
					else:
						self.r[i][j] = self.r[i][j] ^ self.rotate180(self.Kc[j])
						self.g[i][j] = self.g[i][j] ^ self.rotate180(self.Kc[j])
						self.b[i][j] = self.b[i][j] ^ self.rotate180(self.Kc[j])
			# For each column
			for j in range(self.n):
				for i in range(self.m):
					if(j%2==0):
						self.r[i][j] = self.r[i][j] ^ self.Kr[i]
						self.g[i][j] = self.g[i][j] ^ self.Kr[i]
						self.b[i][j] = self.b[i][j] ^ self.Kr[i]
					else:
						self.r[i][j] = self.r[i][j] ^ self.rotate180(self.Kr[i])
						self.g[i][j] = self.g[i][j] ^ self.rotate180(self.Kr[i])
						self.b[i][j] = self.b[i][j] ^ self.rotate180(self.Kr[i])
		else:
			# For each column
			for j in range(self.n):
				for i in range(self.m):
					if(j%2==0):
						self.r[i][j] = self.r[i][j] ^ self.Kr[i]
						self.g[i][j] = self.g[i][j] ^ self.Kr[i]
						self.b[i][j] = self.b[i][j] ^ self.Kr[i]
					else:
						self.r[i][j] = self.r[i][j] ^ self.rotate180(self.Kr[i])
						self.g[i][j] = self.g[i][j] ^ self.rotate180(self.Kr[i])
						self.b[i][j] = self.b[i][j] ^ self.rotate180(self.Kr[i])
			# For each row
			for i in range(self.m):
				for j in range(self.n):
					if(i%2==1):
						self.r[i][j] = self.r[i][j] ^ self.Kc[j]
						self.g[i][j] = self.g[i][j] ^ self.Kc[j]
						self.b[i][j] = self.b[i][j] ^ self.Kc[j]
					else:
						self.r[i][j] = self.r[i][j] ^ self.rotate180(self.Kc[j])
						self.g[i][j] = self.g[i][j] ^ self.rotate180(self.Kc[j])
						self.b[i][j] = self.b[i][j] ^ self.rotate180(self.Kc[j])


	def upshift(self, a, index, n):
		col = []
		for j in range(len(a)):
			col.append(a[j][index])
		shiftCol = numpy.roll(col,-n)
		for i in range(len(a)):
			for j in range(len(a[0])):
				if(j==index):
					a[i][j] = shiftCol[i]

	def downshift(self, a, index, n):
		col = []
		for j in range(len(a)):
			col.append(a[j][index])
		shiftCol = numpy.roll(col,n)
		for i in range(len(a)):
			for j in range(len(a[0])):
				if(j==index):
					a[i][j] = shiftCol[i]

	def rotate180(self, n):
		bits = "{0:b}".format(n)
		return int(bits[::-1], 2)

	def encrypt(self, iter_max=10, alpha = 8):
		self.create_vectors(alpha)
		for iterations in range(iter_max):
			self.roll_row(encrypt_flag = True)
			self.shift_column(encrypt_flag = True)
			self.xor_pixels(encrypt_flag = True)
		for i in range(self.m):
			for j in range(self.n):
				self.pixels[i,j] = (self.r[i][j], self.g[i][j], self.b[i][j])

		self.image.save('encrypted_images/test.png')
  
	def decrypt(self, Kr_file, Kc_file, iter_max=10):
		self.load_vectors(Kr_file, Kc_file)
		for iterations in range(iter_max):
			self.xor_pixels(encrypt_flag = False)
			self.shift_column(encrypt_flag = False)
			self.roll_row(encrypt_flag = False)

		for i in range(self.m):
			for j in range(self.n):
				self.pixels[i,j] = (self.r[i][j], self.g[i][j], self.b[i][j])

		self.image.save('decrypted_images/test.png')

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("encrypt", help="indicate whether to encrypt or decrypt image")
	parser.add_argument("--image", help="indicate input image path")
	parser.add_argument("--output_image", help="indicate output image path")
	parser.add_argument("--Krfile", help="indicate kr file path(in case of decryption)")
	parser.add_argument("--Kcfile", help="indicate kc file path(in case of encryption)")
	

	args = parser.parse_args()
	input_image = args.image
	if args.encrypt == "true":		
		encryptor = RubikCubeEncryptor(input_image)
		encryptor.encrypt(iter_max=10)
	else:
		Krfile = args.Krfile
		Kcfile = args.Kcfile
		decryptor = RubikCubeEncryptor(input_image)
		decryptor.decrypt(Krfile,Kcfile,10)
  