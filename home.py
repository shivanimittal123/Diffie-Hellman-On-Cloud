from flask import Flask, render_template, request, redirect,url_for,session,send_from_directory,send_file
from werkzeug.utils import secure_filename
import os
import os.path 
import math
import pyperclip
import time, sys
import random
import base64
import hashlib
import sys



app = Flask(__name__)
userList = {}
publicKeys = {}
prime_num = 761

#-------------------------------------
''' Diffie Hellman Code'''

''' This function calcuates the a^(s/pi) '''

def power(num,y):
	res = 1
	num = num % prime_num
	
	while y>0:
		if y&1:
			res = (res*num) %prime_num
		y = y>>1
		num = (num*num)%prime_num
	return res


def findPrimeFactors(s,phi):
	while phi%2 == 0:
		if 2 not in s:
			s.append(2)
		phi = phi/2
	
	'''print(s[0])'''	
	ans = int(math.sqrt(phi))
	for i in range(3,ans+1):
		while phi%i == 0:
			if i not in s:
				s.append(int(i))
			phi = int(phi/i)
			
	
	if phi>2:
		s.append(phi)



'''
If the entered number p is prime then s = p-1. Then you need to determine 
all prime factors of p (p1,p2.....pk). Finally calculate a^(s/pi) mod p 
for all i= 1,2....k. and if you find 1 among residulas then it is NOT a 
primitive root, otherwise it is.

'''
def findPrimitive(n):
	phi = n-1
	s = []
	
	findPrimeFactors(s,phi)
	
	for i in range(2,phi+1):
		flag = False
		for it in s:
			p = power(i,int(phi/it))
			if p==1:
				flag = True
				break
		
		if flag ==False:
			return i

primitive = findPrimitive(prime_num)



#--------------------------------------

@app.route('/register-user/')
def redirectUser():
	return render_template('register.html')



''' SENDER - USER REGISTRATION '''
@app.route('/register-user/register',methods=['GET','POST'])
def registerNewUser():
	print('##############')
	username = request.form['username']
	password = request.form['password']
	
	print(username)
	print(password)
	print(type(password))
	#userList = {}
	userList[username] = int(password)
	password= int(password)%700
	publicA = power(primitive,password)
	publicKeys[username]= publicA 
	filepath = os.path.join('./uploads/Public-Keys',username+'.txt')
	fileobj = open(filepath,'w')
	print('=======================================')
	fileobj.write(str(publicA))
	fileobj.close()
	return render_template('successful.html')



@app.route('/verify/')
def redirectVerify():
	return render_template('verify.html')


''' verify username '''
@app.route('/verify/check-username',methods=['GET','POST'])
def verifyUser():
	username = request.form["username"]
	password = request.form["password"]
		
	if username in userList.keys():
		if int(password) == userList[username]:
			return render_template('recieverRegister.html')
		else:
			return render_template('incorrect.html')
	else:
		return render_template('incorrect.html')


@app.route('/verify/recieverRegistration',methods=['GET','POST'])
def reciever():
	print('##############')
	username = request.form['username']
	password = request.form['password']
	
	userList[username] = int(password)
	password= int(password)%700
	publicB = power(primitive,password)
	publicKeys[username] = publicB
	filepath = os.path.join('./uploads/Public-Keys',username+'.txt')
	fileobj = open(filepath,'w')
	fileobj.write(str(publicB))
	fileobj.close()
	return render_template('files.html')


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



@app.route('/verify/encrypt',methods=['GET','POST'])
def encrypt():
	inputFilename = 'input.txt'
	username1 = request.form['username1']
	username2 = request.form['username2']
	# BE CAREFUL! If a file with the outputFilename name already exists,
	# this program will overwrite that file.
	
	inputFilename = str(inputFilename)
	print(inputFilename)
	senderPrivateKey = userList[username1]
	recieverPublicKey = publicKeys[username2]
	
	outputFilename = 'encrypted.txt'
	#	A = diffie_hellmanA(prime_num,privateA,alpha)
	
	
	myKey = power(recieverPublicKey,senderPrivateKey)
	print(myKey)
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
	
	
	#Read in the message from the input file
	
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
	return render_template('esuccess.html')	


def decryptMessage(key, message):
    # The transposition decrypt function will simulate the "columns" and
    # "rows" of the grid that the plaintext is written on by using a list
    # of strings. First, we need to calculate a few values.

    # The number of "columns" in our transposition grid:
	numOfColumns = math.ceil(len(message) / key)
    # The number of "rows" in our grid will need:
	numOfRows = key
    # The number of "shaded boxes" in the last "column" of the grid:
	numOfShadedBoxes = (numOfColumns * numOfRows) - len(message)

    # Each string in plaintext represents a column in the grid.
	plaintext = [''] * numOfColumns

    # The col and row variables point to where in the grid the next
    # character in the encrypted message will go.
    
	col = 0
	row = 0
	
	for symbol in message:
		plaintext[col] += symbol
		col += 1 # point to next column

        # If there are no more columns OR we're at a shaded box, go back to
        # the first column and the next row.
		if (col == numOfColumns) or (col == numOfColumns - 1 and row >= numOfRows - numOfShadedBoxes):
			col = 0
			row += 1
	return ''.join(plaintext)



@app.route('/decrypt')
def decryptPage():
	return render_template('decrypt.html')
	

@app.route('/decryptMessage',methods=['GET','POST'])
def decrypt():
	print('##################3')
	inputFilename = 'encrypted.txt'
	
	username1 = request.form['username1']
	username2 = request.form['username2']
	
	senderPublicKey = publicKeys[username1]
	recieverPrivateKey = userList[username2]
	# BE CAREFUL! If a file with the outputFilename name already exists,
	# this program will overwrite that file.

	outputFilename = 'decrypted.txt'
	
	myKey = power(senderPublicKey, recieverPrivateKey)
	
	myMode = 'decrypt' # set to 'encrypt' or 'decrypt'

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
	translated = decryptMessage(myKey, content)
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
	return render_template('dsuccess.html')



''' FILE REDIRECTS '''
@app.route('/')
def home():
	return render_template('home.html')
		
	
'''@app.route('/files/')
def redirectFiles():
	return render_template('files.html')
'''



@app.route('/keys/')
def redirectKeys():
	return render_template('keys.html')

	
@app.route('/Public_key/')
def redirect():
	return render_template('PublicKey.html')

'''@app.route('/verify/check-username/recieverRegistration',methods=['GET','POST'])
def recieverRegister():
	return render_template('recieverRegister.html')
'''

#---------------------------------------------



	
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80)
