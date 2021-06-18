from math import gcd
from hashlib import blake2b

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
		





Message=3192
#print("Message:",Message)
pAlice= 2000303
qAlice= 2000387

pBob= 2000423
qBob= 2000807

e= 65537

Alice_N = pAlice * qAlice
#print("Alice_Mod_N:",Alice_N)
Bob_N = pBob * qBob
#print("Bob_Mod_N:",Bob_N)

phi = (pAlice - 1) * (qAlice - 1)
#print("Phi:",phi)

lamda_Of_N = Check_lcm(pAlice-1,qAlice-1)
#print("LCM:",lamda_Of_N)

d=inverseMod(e,phi)
#print("D inverse:",d)

#print("E*D:",e*d)
#print("check invers1:",(e*d)%lamda_Of_N)

publicKey_Alice=[e,Alice_N]
publicKey_Bob = [e,Bob_N]

privateKey_Alice=[ inverseMod(e,(pAlice - 1) * (qAlice - 1)), pAlice, qAlice, Check_lcm(pAlice-1,qAlice-1)]
privateKey_Bob=[ inverseMod(e,(pBob - 1) * (qBob - 1)), pBob, qBob, Check_lcm(pBob-1,qBob-1)]

Dalice=inverseMod(e,(pAlice - 1) * (qAlice - 1))

#Alice --> Bob	
cipherM=Cipher_Message_ByRepitativeSQ(Message,e,Bob_N)
print("The Cipher Message:",cipherM)

#print("The Dcipher Message:",Dcipher_Message_ByRepitativeSQ(cipherM,privateKey_Bob[0],Bob_N))


MessageHash = int(blake2b(str(cipherM).encode(),digest_size=2).hexdigest(),base=16)
print("MessageHash:",MessageHash)

Message_afterHash_phi = (MessageHash**e)%Alice_N
print("Message_afterHas_phi:",Message_afterHash_phi)

#print("\nAlice SEND(After Hash) To Bob the (message,Encryption): " +'(' + str(Message) + ',' + str(Message_afterHash_phi) +')')


answer=DecMessage_AfterHash(cipherM,Message_afterHash_phi, Dalice, publicKey_Alice[1])

if(answer==True):
	DecrypteM = Dcipher_Message_ByRepitativeSQ(cipherM,privateKey_Bob[0],Bob_N)
	#print("\nBob recieve The message ", Message_afterHash_phi)
	#print("after Validation its really from Alice the message is:",DecrypteM)
	print("The Picture You Need to Open(Follow the Chipher Message) is:")
	print(DecrypteM)	
else:
	print("\nBob recieve Message and after Decryption -> doesnt match")
	print("How is trying to cheat?!!!")

