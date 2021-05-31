import os
email_os = os.getenv("email")
hash_os = os.getenv("hash")

from flask import Flask,render_template,send_file,request
from email.message import EmailMessage
from string import Template
import csv
import smtplib

app = Flask(__name__)

@app.route('/')
def home_page():
	return render_template("index.html")

@app.route('/<string:page>')
def html_page(page):
	try:
		return render_template(f'{page}.html')
	except:
		return render_template('404.html')


@app.route('/submit',methods=["POST","GET"])
def submit_form():
	try:
		if request.method == "POST":
			data = request.form.to_dict()
			email = EmailMessage()
			email["from"] = data["email"]
			email["to"] = email_os
			email['subject'] = "Message from My Portfolio"

			email.set_content(f'Hello it\'s <b>{data["name"]}</b> <br/><u>{data["email"]}</u> <hr/><br/><br/> {data["message"]}',"html")

			with smtplib.SMTP(host="smtp.gmail.com",port=587) as smtp:
				smtp.ehlo()
				smtp.starttls()
				smtp.login(email_os,hash_os)
				smtp.send_message(email)
				print("Message Sent Successfully")
				write_to_csv(data)
				return render_template("success.html")
		else:
			return render_template("error.html")
	except:
		return render_template("error.html")

@app.route('/resume')
def get_resume():
	return send_file('static/assets/NOUBISSIE DIEPE ANGE ODILON CV v2.pdf')

def write_to_csv(data):
  with open('./database.csv', newline='', mode='a') as database2:
    email = data["email"]
    name = data["name"]
    message = data["message"]
    csv_writer = csv.writer(database2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow([email,name,message])


@app.errorhandler(404)
def not_found(e):

  return render_template("404.html")


if __name__ == '__main__':
    app.run(debug=True)
