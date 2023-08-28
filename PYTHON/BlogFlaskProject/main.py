from flask import Flask, render_template
import requests

app = Flask(__name__)
all_post = {item['id']: {"title":item['title'], "subtitle":item['subtitle'],"body":item['body']} for item in requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()}
@app.route('/')
def home():
    return render_template("index.html",posts = all_post)

@app.route('/post/<blog_id>')
def show_post(blog_id):
    return render_template("post.html", post = all_post[int(blog_id)])

if __name__ == "__main__":
    app.run(debug=True)
