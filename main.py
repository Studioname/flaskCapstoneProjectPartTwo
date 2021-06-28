from flask import Flask
from flask import url_for, render_template
import requests
from pprint import pprint

data_endpoint = "https://api.npoint.io/5deaf41b4f8078c817e6"

response = requests.get(data_endpoint)
response_data = response.json()

pprint(response_data)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html", blog_posts=response_data)

@app.route('/about.html')
def about():
    return render_template("about.html")

@app.route('/contact.html')
def contact():
    return render_template("contact.html")

@app.route('/post/<int:post_id>')
def get_blog_post(post_id):
    for post in response_data:
        if post['id'] == post_id:
            blog_post = post
    return render_template("post.html", blog_post=blog_post)


if __name__ == "__main__":
    app.run(debug=True)

