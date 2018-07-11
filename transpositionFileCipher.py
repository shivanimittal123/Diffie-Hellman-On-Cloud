import pyperclip
import transpositionCipher
import time, os, sys
import random
import base64
import hashlib
import sys
import math



def diffie_hellmanA(prime_num,privateA,alpha):
	A = power(alpha,privateA,prime_num)
	return A

	
def diffie_hellmanB(prime_num,privateB,alpha):
	B = power(alpha,privateB,prime_num)
	return B
	

def encryptMessage(key, message):
    # Each string in ciphertext represents a column in the grid.
    ciphertext = [''] * key

    # Loop through each column in ciphertext.
    for col in range(key):
        pointer = col

        # Keep looping until pointer goes past the length of the message.
        while pointer < len(message):
            # Place the character at pointer in message at the end of the
            # current column in the ciphertext list.
            ciphertext[col] += message[pointer]

            # move pointer over
            pointer += key

    # Convert the ciphertext list into a single string value and return it.
    return ''.join(ciphertext)


def enc(prime_num,privateA,privateB,alpha):

	inputFilename = 'input.txt'

	# BE CAREFUL! If a file with the outputFilename name already exists,
	# this program will overwrite that file.

	outputFilename = 'encrypted.txt'
#	A = diffie_hellmanA(prime_num,privateA,alpha)

	myKey = 120
	myMode = 'encrypt' # set to 'encrypt' or 'decrypt'

	# If the input file does not exist, then the program terminates early.

	if not os.path.exists(inputFilename):
		print('The file %s does not exist. Quitting...' % (inputFilename))
		sys.exit()

	# If the output file already exists, give the user a chance to quit.

	if os.path.exists(outputFilename):
		print('This will overwrite the file %s. (C)ontinue or (Q)uit?' % (outputFilename))
		response = input('> ')
		if not response.lower().startswith('c'):
			sys.exit()

	# Read in the message from the input file

	fileObj = open(inputFilename)
	content = fileObj.read()
	fileObj.close()

	print('%sing...' % (myMode.title()))

	# Measure how long the encryption/decryption takes.

	startTime = time.time()
	translated = encryptMessage(myKey, content)
	totalTime = round(time.time() - startTime, 2)
	print('%sion time: %s seconds' % (myMode.title(), totalTime))

	# Write out the translated message to the output file.

	outputFileObj = open(outputFilename, 'w')
	outputFileObj.write(translated)
	outputFileObj.close()

	print('Done %sing %s (%s characters).' % (myMode, inputFilename, len(content)))
	print('%sed file is %s.' % (myMode.title(), outputFilename))

	# If transpositionCipherFile.py is run (instead of imported as a module)
	# call the main() function.


def main():
	
	
	prime_num = 761
	print('number is prime and its primitive root is:  ')
	alpha = diffie_hellman.findPrimitive(prime_num)
	print(alpha)
	
	privateA = random.randint(5, 10)
	privateB = random.randint(10,20)
		
	enc(761,privateA,privateB,alpha)
	
	
if __name__ == '__main__':
	main()
