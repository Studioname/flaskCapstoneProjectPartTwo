from flask import Flask
from flask import url_for, render_template, request
import requests
import smtplib
import os

data_endpoint = "https://api.npoint.io/5deaf41b4f8078c817e6"

response = requests.get(data_endpoint)
response_data = response.json()

SMTP_ADDRESS = os.environ['SMTP_ADDRESS']
EMAIL_LOGIN = os.environ['EMAIL_LOGIN']
EMAIL_PASSWORD = os.environ['EMAIL_PASSWORD']
EMAIL_TO = os.environ['EMAIL_TO']

def send_email(sender, sender_email, sender_phone, message_body):
    connection = smtplib.SMTP(SMTP_ADDRESS)
    connection.starttls()
    connection.login(user=EMAIL_LOGIN, password=EMAIL_PASSWORD)
    message = f"Message from {sender}\\Name:{sender}\nEmail: {sender_email}\nTelephone: {sender_phone}\n{message_body}"
    connection.sendmail(from_addr=EMAIL_LOGIN, to_addrs=EMAIL_TO, msg=message)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html", blog_posts=response_data)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == "GET":
        return render_template("contact.html")
    elif request.method == "POST":
        send_email(request.form["name"], request.form["email"], request.form["phone"], request.form["message"])
        return render_template("contact.html")

@app.route('/post/<int:post_id>')
def get_blog_post(post_id):
    for post in response_data:
        if post['id'] == post_id:
            blog_post = post
    return render_template("post.html", blog_post=blog_post)

if __name__ == "__main__":
    app.run(debug=True)

