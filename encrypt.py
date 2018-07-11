from flask import Flask, render_template, request


app = Flask(__name__)


@app.route("/encrypt/", methods=['GET', 'POST'])
def index():
	print(request.method)
	if request.method == 'POST':
		if request.form.get('encrypt') == 'encrypt':
			# pass
			print("Encrypted")
		elif  request.form.get('decrypt') == 'decrypt':
			# pass # do something else
			print("Decrypted")
		else:
			# pass # unknown
			return render_template("index.html")
	elif request.method == 'GET':
		# return render_template("index.html")
		print("No Post Back Call")
	return render_template("index.html")

if __name__ == '__main__':
	app.run()
