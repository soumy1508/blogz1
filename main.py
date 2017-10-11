from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:launchcode@123@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(250))

    def __init__(self, title, body):
        self.title = title
        self.body = body
        


@app.route('/', methods=['GET'])
def index(): 
    # we have to write code to get the data from the database
    # get the list of blogs from the table
    # give the list of blogs to the blog html page

    listofblogs = Blog.query.all()
    return render_template('blog.html',blogs=listofblogs)


@app.route('/newpost', methods=['POST','GET'])
def newpost():   
    if request.method == 'POST':
        user_title = request.form['title']
        user_body = request.form['body']
        newBlog = Blog(user_title, user_body)
        db.session.add(newBlog)
        db.session.commit()
        return redirect('/') 
    else:
        return render_template('newpost.html')


if __name__ == '__main__':
     app.run()