import Image
from random import randint
import numpy

im = Image.open('encrypt.png')
pixels = list(im.getdata())
pix = im.load()


def upshift(a,index,n):
	col = []
	for j in range(len(a)):
		col.append(a[j][index])
	shiftCol = numpy.roll(col,-n)
	for i in range(len(a)):
		for j in range(len(a[0])):
			if(j==index):
				a[i][j] = shiftCol[i]

def downshift(a,index,n):
	col = []
	for j in range(len(a)):
		col.append(a[j][index])
	shiftCol = numpy.roll(col,n)
	for i in range(len(a)):
		for j in range(len(a[0])):
			if(j==index):
				a[i][j] = shiftCol[i]

def rotate180(n):
	bits = "{0:b}".format(n)
	return int(bits[::-1], 2)


#Obtaining the RGB matrices
r = []
g = []
b = []
for i in range(im.size[0]):
	r.append([])
	g.append([])
	b.append([]) 
	for j in range(im.size[1]):
		rgbPerPixel = pix[i,j]
		r[i].append(rgbPerPixel[0])
		g[i].append(rgbPerPixel[1])
		b[i].append(rgbPerPixel[2])

m = im.size[0]
n = im.size[1]

f = open('keys.txt','r')
l = []
for line in f:
	l.append(line)
# Vectors Kr and Kc


Kr = [1, 238, 95, 72, 15, 209, 184, 185, 111, 198, 142, 177, 116, 225, 50, 85, 179, 7, 71, 148, 102, 24, 60, 193, 204, 95, 137, 216, 158, 67, 67, 128, 115, 85, 84, 28, 91, 168, 32, 119, 150, 140, 204, 37, 8, 113, 157, 52, 250, 114, 3, 38, 112, 67, 129, 90, 41, 35, 165, 181, 204, 225, 52, 225, 230, 97, 132, 208, 209, 29, 16, 147, 99, 195, 38, 210, 90, 105, 12, 251, 2, 60, 218, 242, 4, 106, 143, 245, 143, 191, 78, 121, 35, 92, 93, 25, 106, 5, 60, 55, 233, 207, 54, 141, 76, 158, 91, 237, 161, 96, 218, 46, 179, 98, 54, 236, 115, 101, 250, 45, 28, 240, 239, 16, 31, 40, 90, 244, 57, 15, 214, 116, 51, 157, 159, 89, 232, 51, 227, 103, 51, 198, 215, 195, 57, 46, 94, 114, 233, 32, 207, 96, 154, 39, 12, 10, 105, 137, 195, 158, 40, 145, 168, 61, 59, 197, 67, 69, 169, 185, 78, 0, 239, 78, 4, 185, 188, 77, 248, 42, 74, 248, 22, 247, 228, 135, 253, 216, 94, 177, 71, 71, 228, 254, 124, 218, 19, 67, 108, 128, 11, 170, 23, 27, 109, 106, 75, 134, 41, 193, 113, 219, 143, 18, 218, 192, 242, 114, 150, 254, 229, 121, 51, 99, 224, 253, 237, 106, 0, 188, 218, 240, 119, 2, 16, 33, 152, 148, 137, 100, 253, 49, 217, 3, 101, 63, 176, 241, 110, 41, 103, 15, 99, 25, 86, 204, 132, 247, 19, 171, 155, 45, 94, 60, 138, 188, 171, 246, 254, 195, 255, 180, 69, 183, 124, 57, 89, 121, 96, 53, 253, 186, 183, 36, 103, 227, 11, 53, 58, 222, 218, 62, 31, 3, 25, 226, 59, 207, 78]
Kc = [8, 214, 92, 46, 59, 90, 171, 173, 196, 23, 148, 62, 220, 51, 110, 173, 232, 15, 35, 57, 218, 48, 18, 219, 132, 205, 95, 118, 31, 172, 74, 27, 14, 203, 137, 231, 155, 247, 59, 250, 186, 138, 108, 159, 134, 18, 99, 82, 109, 1, 229, 74, 13, 243, 158, 99, 242, 92, 224, 194, 187, 81, 205, 240, 188, 150, 71, 113, 119, 66, 17, 157, 86, 175, 213, 204, 208, 107, 54, 54, 120, 221, 75, 77, 7, 44, 2, 26, 205, 218, 98, 200, 48, 109, 202, 8, 60, 44, 35, 10, 126, 210, 4, 129, 171, 203, 147, 101, 14, 186, 119, 229, 4, 208, 106, 67, 251, 152, 110, 33, 240, 51, 50, 170, 78, 94, 252, 14, 37, 150, 13, 117, 226, 36, 236, 170, 134, 131, 211, 213, 204, 41, 235, 3, 215, 14, 153, 237, 160, 170, 140, 32, 43, 33, 217, 69, 2, 135, 184, 48, 193, 43, 170, 188, 40, 66, 190, 42]
ITER_MAX = 1
'''
Kr = input('Enter value of Kr')
Kc = input('Enter value of Kc')
ITER_MAX = input('Enter value of ITER_MAX')
'''

for iterations in range(ITER_MAX):
	# For each column
	for j in range(n):
		for i in range(m):
			if(j%2==0):
				r[i][j] = r[i][j] ^ Kr[i]
				g[i][j] = g[i][j] ^ Kr[i]
				b[i][j] = b[i][j] ^ Kr[i]
			else:
				r[i][j] = r[i][j] ^ rotate180(Kr[i])
				g[i][j] = g[i][j] ^ rotate180(Kr[i])
				b[i][j] = b[i][j] ^ rotate180(Kr[i])
	# For each row
	for i in range(m):
		for j in range(n):
			if(i%2==1):
				r[i][j] = r[i][j] ^ Kc[j]
				g[i][j] = g[i][j] ^ Kc[j]
				b[i][j] = b[i][j] ^ Kc[j]
			else:
				r[i][j] = r[i][j] ^ rotate180(Kc[j])
				g[i][j] = g[i][j] ^ rotate180(Kc[j])
				b[i][j] = b[i][j] ^ rotate180(Kc[j])
	# For each column
	for i in range(n):
		rTotalSum = 0
		gTotalSum = 0
		bTotalSum = 0
		for j in range(m):
			rTotalSum += r[j][i]
			gTotalSum += g[j][i]
			bTotalSum += b[j][i]
		rModulus = rTotalSum % 2
		gModulus = gTotalSum % 2
		bModulus = bTotalSum % 2
		if(rModulus==0):
			downshift(r,i,Kc[i])
		else:
			upshift(r,i,Kc[i])
		if(gModulus==0):
			downshift(g,i,Kc[i])
		else:
			upshift(g,i,Kc[i])
		if(bModulus==0):
			downshift(b,i,Kc[i])
		else:
			upshift(b,i,Kc[i])

	# For each row
	for i in range(m):
		rTotalSum = sum(r[i])
		gTotalSum = sum(g[i])
		bTotalSum = sum(b[i])
		rModulus = rTotalSum % 2
		gModulus = gTotalSum % 2
		bModulus = bTotalSum % 2
		if(rModulus==0):
			r[i] = numpy.roll(r[i],-Kr[i])
		else:
			r[i] = numpy.roll(r[i],Kr[i])
		if(gModulus==0):
			g[i] = numpy.roll(g[i],-Kr[i])
		else:
			g[i] = numpy.roll(g[i],Kr[i])
		if(bModulus==0):
			b[i] = numpy.roll(b[i],-Kr[i])
		else:
			b[i] = numpy.roll(b[i],Kr[i])

for i in range(m):
	for j in range(n):
		pix[i,j] = (r[i][j],g[i][j],b[i][j])

im.save('decryptedImage.png')



