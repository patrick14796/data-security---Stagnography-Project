from datetime import date
from PIL import Image
from math import gcd
from hashlib import blake2b
import random

#RSA Functions:
def Check_Prime(num):
	if num > 1:
		for i in range(2, num):
			if (num % i) == 0:
				# if factor is found, set flag to True
				return True
		return False

def Check_lcm(x, y):
   return x * y // gcd(x, y)

def inverseMod(a, m):
    m0 = m
    y = 0
    x = 1
 
    if (m == 1):
        return 0
 
    while (a > 1):
 
        # q is quotient
        q = a // m
 
        t = m
 
        # m is remainder now, process
        # same as Euclid's algo
        m = a % m
        a = t
        t = y
 
        # Update x and y
        y = x - q * y
        x = t
 
    # Make x positive
    if (x < 0):
        x = x + m0
 
    return x

def Cipher_Message_ByRepitativeSQ(bas,exp,ModN): 
    cipher = 1; 
    while(exp > 0):  
  
        # for cases where exponent 
        # is not an even value 
        if (exp % 2 != 0): 
            cipher = (cipher * bas) % ModN; 
  
        bas = (bas * bas) % ModN; 
        exp = int(exp / 2); 
    return cipher % ModN; 

def Dcipher_Message_ByRepitativeSQ(bas,exp,ModN): 
    Dcipher = 1; 
    while(exp > 0):  
  
        # for cases where exponent 
        # is not an even value 
        if (exp % 2 != 0): 
            Dcipher = (Dcipher * bas) % ModN; 
  
        bas = (bas * bas) % ModN; 
        exp = int(exp / 2); 
    return Dcipher % ModN ; 

def DecMessage_AfterHash(Message,Message_afterHash_phi,Esend,ModSend):
	hash_the_Original_message=int(blake2b(str(Message).encode(),digest_size=2).hexdigest(),base=16)
	#print("hash_the_Original_message in func:",hash_the_Original_message)
	check_phi = Dcipher_Message_ByRepitativeSQ(Message_afterHash_phi,Esend,ModSend)
	#print("phi of Message in func:",check_phi)

	if(hash_the_Original_message == check_phi):
		return True
	return False


#Encode Picture & Text Functions:
def EncodePicture(rgb_img_path, bin_img_path, new_img_name):
	imC = Image.open(rgb_img_path).convert('RGB')
	imB = Image.open(bin_img_path).convert('1')
	# Split into 3 channels
	r, g, b = imC.split()

	#bpixel
	pixels = list(b.getdata())
	width, height = b.size
	#binary blue channel
	b_arr = [bin(col)[2:].zfill(8) for col in pixels]

	#rpixel
	pixels = list(r.getdata())
	width, height = r.size
	#binary red channel
	r_arr = [bin(col)[2:].zfill(8) for col in pixels ]



	#gpixel
	pixels = list(g.getdata())
	width, height = g.size
	#binary green channel
	g_arr = [bin(col)[2:].zfill(8) for col in pixels ]



	#binarypixel
	pixels = list(imB.getdata())
	width, height = imB.size
	#binary channel
	binary_arr = [bin(col)[2:].zfill(8) for col in pixels ]

	#XOR
	for i in range(len(binary_arr)):
			x=(int(binary_arr[i][7]) ^ int(r_arr[i][7]))
			if(not(x)):
				y=1 ^ int(g_arr[i][7])
				if(not(y)):
					pixel = list(b_arr[i])
					pixel[7] = '1'
					pixel = ''.join(pixel)
					b_arr[i]=pixel
				else:
					pixel = list(b_arr[i])
					pixel[7] = '0'
					pixel = ''.join(pixel)
					b_arr[i]=pixel
			else:
				y=0 ^ int(g_arr[i][7])
				if(y):
					pixel = list(b_arr[i])
					pixel[7] = '0'
					pixel = ''.join(pixel)
					b_arr[i]=pixel
				else:
					pixel = list(b_arr[i])
					pixel[7] = '1'
					pixel = ''.join(pixel)
					b_arr[i]=pixel





	new_b = [int(col,2) for col in b_arr ]
	b.putdata(new_b)
	# Recombine back to RGB image
	result = Image.merge('RGB', (r,g,b))
	result.save(new_img_name + '.png')

def DecodePicture(img_path):
	imCombined = Image.open(img_path)

	rc, gc, bc = imCombined.split()


	#bpixel
	pixelsC = list(bc.getdata())
	widthC, heightC = bc.size
	#binary blue channel
	b_arrC = [bin(col)[2:].zfill(8) for col in pixelsC]



	#rpixel
	pixelsC = list(rc.getdata())
	widthC, heightC = rc.size
	#binary red channel
	r_arrC = [bin(col)[2:].zfill(8) for col in pixelsC]


	#gpixel
	pixelsC = list(gc.getdata())
	widthC, heightC = gc.size
	#binary green channel
	g_arrC = [bin(col)[2:].zfill(8) for col in pixelsC]




	binary_image_arr = []
	#XOR

	for i in range(len(b_arrC)):
			x=(int(b_arrC[i][7]) ^ int(g_arrC[i][7]))
			if(not(x)):
				y=1 ^ int(r_arrC[i][7])
				if(not(y)):
					binary_image_arr.append(1)
				else:
					binary_image_arr.append(0)
			else:
				y=0 ^ int(r_arrC[i][7])
				if(y):
					binary_image_arr.append(0)
				else:
					binary_image_arr.append(1)



	binary_image_arr=binary_image_arr[:128*128]
	nimg=Image.new('1',(128,128))
	nimg.putdata(binary_image_arr)
	nimg.show()

def EncodeText(rgb_img_path, new_img_name):
	imC = Image.open(rgb_img_path).convert('RGB')
	secret = input("Please Enter Your Secret Message: ")
	secretMessage= secret+str("//")
	secret=secretMessage
	# Split into 3 channels
	r, g, b = imC.split()


	#bpixel
	pixels = list(b.getdata())
	width, height = b.size
	#binary blue channel
	b_arr = [bin(col)[2:].zfill(8) for col in pixels]

	#rpixel
	pixels = list(r.getdata())
	width, height = r.size
	#binary red channel
	r_arr = [bin(col)[2:].zfill(8) for col in pixels ]



	#gpixel
	pixels = list(g.getdata())
	width, height = g.size
	#binary green channel
	g_arr = [bin(col)[2:].zfill(8) for col in pixels ]



	#binarypixel
	#pixels = list(secret.encode())
	pixels = secret.encode()

	#binary channel
	binary_arr = [bin(col)[2:].zfill(8) for col in pixels ]


	binary_arr = ''.join(binary_arr)
	#XOR
	for i in range(len(binary_arr)):
			x=(int(binary_arr[i]) ^ int(r_arr[i][7]))
			if(not(x)):
				y=1 ^ int(g_arr[i][7])
				if(not(y)):
					pixel = list(b_arr[i])
					pixel[7] = '1'
					pixel = ''.join(pixel)
					b_arr[i]=pixel
				else:
					pixel = list(b_arr[i])
					pixel[7] = '0'
					pixel = ''.join(pixel)
					b_arr[i]=pixel
			else:
				y=0 ^ int(g_arr[i][7])
				if(y):
					pixel = list(b_arr[i])
					pixel[7] = '0'
					pixel = ''.join(pixel)
					b_arr[i]=pixel
				else:
					pixel = list(b_arr[i])
					pixel[7] = '1'
					pixel = ''.join(pixel)
					b_arr[i]=pixel


	new_b = [int(col,2) for col in b_arr ]
	b.putdata(new_b)
	# Recombine back to RGB image
	result = Image.merge('RGB', (r,g,b))
	result.save(new_img_name + '.png')

def DecodeText(img_path):
	imCombined = Image.open(img_path)

	rc, gc, bc = imCombined.split()


	#bpixel
	pixelsC = list(bc.getdata())
	widthC, heightC = bc.size
	#binary blue channel
	b_arrC = [bin(col)[2:].zfill(8) for col in pixelsC]



	#rpixel
	pixelsC = list(rc.getdata())
	widthC, heightC = rc.size
	#binary red channel
	r_arrC = [bin(col)[2:].zfill(8) for col in pixelsC]


	#gpixel
	pixelsC = list(gc.getdata())
	widthC, heightC = gc.size
	#binary green channel
	g_arrC = [bin(col)[2:].zfill(8) for col in pixelsC]




	binary_image_arr = []
	#XOR

	for i in range(len(b_arrC)):
			x=(int(b_arrC[i][7]) ^ int(g_arrC[i][7]))
			if(not(x)):
				y=1 ^ int(r_arrC[i][7])
				if(not(y)):
					binary_image_arr.append(1)
				else:
					binary_image_arr.append(0)
			else:
				y=0 ^ int(r_arrC[i][7])
				if(y):
					binary_image_arr.append(0)
				else:
					binary_image_arr.append(1)

	
	binary_image_arr = list(map(str, binary_image_arr))
	binary_image_arr = ["".join(binary_image_arr[i:i + 8]) for i in range(0, len(binary_image_arr), 8)]
	binary_image_arr = list(map(lambda x: chr(int(x, 2)), binary_image_arr))
	binary_image_arr = ''.join(binary_image_arr)
	msg = (binary_image_arr.split("//"))[0]
	print("Decoded Message:",msg)
	
def EncodePicture_Rsa(rgb_img_path, bin_img_path):
	secrect_img_num = random.randint(0, 4)
	EncodePicture(rgb_img_path, bin_img_path, 'result' + str(secrect_img_num))

	j = 0
	# duplicate image
	for i in range(5):
		if i != secrect_img_num:
			namePath='result' + str(i)
			bin_img_name = 'bin'+ str(j) +  '.jpeg'
			EncodePicture(rgb_img_path, bin_img_name, namePath)
			j = j +1
		

	return secrect_img_num


#improvment2
def improv2():
	Message = EncodePicture_Rsa('1.jpeg', '2.jpeg')
	print("Secret:",Message)
	


	pAlice= 2000303
	qAlice= 2000387

	pBob= 2000423
	qBob= 2000807
	e= 65537

	Alice_N = pAlice * qAlice
	Bob_N = pBob * qBob

	phi = (pAlice - 1) * (qAlice - 1)

	lamda_Of_N = Check_lcm(pAlice-1,qAlice-1)

	d=inverseMod(e,phi)

	publicKey_Alice=[e,Alice_N]
	publicKey_Bob = [e,Bob_N]

	privateKey_Alice=[ inverseMod(e,(pAlice - 1) * (qAlice - 1)), pAlice, qAlice, Check_lcm(pAlice-1,qAlice-1)]
	privateKey_Bob=[ inverseMod(e,(pBob - 1) * (qBob - 1)), pBob, qBob, Check_lcm(pBob-1,qBob-1)]

	Dalice=inverseMod(e,(pAlice - 1) * (qAlice - 1))

	#Alice --> Bob	
	cipherM=Cipher_Message_ByRepitativeSQ(Message,e,Bob_N)
	print("The Cipher Message:",cipherM)


	MessageHash = int(blake2b(str(cipherM).encode(),digest_size=2).hexdigest(),base=16)
	print("MessageHash:",MessageHash)

	Message_afterHash_phi = (MessageHash**e)%Alice_N
	print("Message_afterHas_phi:",Message_afterHash_phi)

	answer=DecMessage_AfterHash(cipherM,Message_afterHash_phi, Dalice, publicKey_Alice[1])

	if(answer==True):
		DecrypteM = Dcipher_Message_ByRepitativeSQ(cipherM,privateKey_Bob[0],Bob_N)
		print("The Picture You Need to Open(Follow the Chipher Message) is:")
		print("result"+str(DecrypteM)+'.png')	
	else:
		print("\nMessage Problem!!!!\n")

#improv2()
#DecodePicture('result0.png')
#DecodePicture('result1.png')	
#DecodePicture('result2.png')
#DecodePicture('result3.png')
#DecodePicture('result4.png')



#Main
EncodePicture('1.jpeg', '2.jpeg', 'result')
#EncodeText('1.jpeg', 'resultText')
#DecodeText('resultText.png')
#DecodePicture('result.png')
