from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import cgi

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
        


@app.route('/blog', methods=['GET'])
def index(): 
    # we have to write code to get the data from the database
    # get the list of blogs from the table
    # give the list of blogs to the blog html page
    blogid = request.args.get("id")
    if blogid:
        singleblog = Blog.query.filter_by(id=int(blogid)).first()
        return render_template('oneblog.html', blog=singleblog)
    else:
        listofblogs = Blog.query.all()
        return render_template('blog.html',blogs=listofblogs)

    
@app.route('/newpost', methods=['POST','GET'])
def newpost():   
    if request.method == 'POST':
        user_title = request.form['title']
        user_body = request.form['body']

        # do validations here
        # if validation Pass then store data in Db
        # else redirect to newpost page with error messages
                
        titleerrormessage = ""
        bodyerrormessage = ""
        
        if (not user_title) or (user_title.strip() == ""):
            titleerrormessage = "Please enter title"

        if (not user_body) or (user_body.strip() == ""):
            bodyerrormessage = "Please enter body"
        
        if titleerrormessage or bodyerrormessage:
            # go to page and display the error message
            return redirect("/newpost?titleerror=" + titleerrormessage + "&bodyerror=" + bodyerrormessage)
        else:
            newBlog = Blog(user_title, user_body)
            db.session.add(newBlog)
            db.session.commit()
            return redirect("/blog?id=" + str(newBlog.id))            
            #return redirect('/blog')
    else:
        titleerror = request.args.get("titleerror")
        bodyerror = request.args.get("bodyerror")
        return render_template('newpost.html',
                                titleerror=titleerror and cgi.escape(titleerror, quote=True),
                                bodyerror=bodyerror and cgi.escape(bodyerror, quote=True) )


if __name__ == '__main__':
     app.run()