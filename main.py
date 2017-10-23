from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz1:launchcode@123@localhost:8889/blogz1'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)
app.secret_key = 'dgdgdfgdfgdfgdgdghdgghgh'

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(250))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(250))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password
        
        
@app.route('/', methods=['GET'])
def userindex():    
        listofusers = User.query.all()        
        return render_template('index.html',users=listofusers)




@app.route('/login', methods=['POST','GET'])
def userlogin():
    if request.method == 'POST':         
        username = request.form['username']
        password = request.form['password']
        
        _usernameerror = ""
        _passworderror = ""

        if (not username) or (username.strip() == ""):
            _usernameerror = "Please enter username"

        if (not password) or (password.strip() == ""):
            _passworderror = "Please enter passwd"

        if _usernameerror or _passworderror:
            return render_template('login.html', usernameerror=_usernameerror, passworderror=_passworderror)
        else:        
            user = User.query.filter_by(username=username).first()
            if user and user.password == password:
                session['username'] = username
                flash("Logged in")
                return render_template('newpost.html', titleerror="", bodyerror="")
            else:
                flash('User password incorrect, or user does not exist', 'error')


    return render_template('login.html')

@app.route('/logout')
def logout():
    del session['username']
    print(session)
    return redirect('/blog')

@app.route('/signup', methods=['POST', 'GET'])
def usersignup():
    if request.method == 'POST':
        
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']     

        _usernameerror = ""
        _passworderror = ""
        _verifyerror = ""

        if (not username) or (username.strip() == ""):
            _usernameerror = "Please enter username"

        if (not password) or (password.strip() == ""):
            _passworderror = "Please enter passwd"

        if (not verify) or (verify.strip() == ""):
            _verifyerror = "Please verify passwd"

        if (len(username) < 3):
            _usernameerror = "Invalid username"
        
        if (len(password) < 3):
            _passworderror = "Invalid password"


        if _usernameerror or _passworderror or _verifyerror:
                return render_template('signup.html',
                                usernameerror=_usernameerror and cgi.escape(_usernameerror, quote=True),
                                passworderror=_passworderror and cgi.escape(_passworderror, quote=True),
                                verifyerror=_verifyerror and cgi.escape(_verifyerror, quote=True))
        else:
            existing_user = User.query.filter_by(username=username).first()
            if not existing_user:
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()  

                session['username'] = username
                flash("Logged in")    
                print(session)      
                return render_template('newpost.html', titleerror="", bodyerror="")
            else:            
                return "<h1>Duplicate user</h1>"

    elif request.method == 'GET':
        return render_template('signup.html')



@app.route('/singluser', methods=['GET'])
def singleuserdata(): 
    clickuserid = request.args.get("id")
    clickeduserobject = User.query.filter_by(id=int(clickuserid)).first()
    singleuserblogs = Blog.query.filter_by(owner=clickeduserobject).all()
    return render_template('singleUser.html', userblogs=singleuserblogs)


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
            return render_template('newpost.html',
                                titleerror=titleerrormessage and cgi.escape(titleerrormessage, quote=True),
                                bodyerror=bodyerrormessage and cgi.escape(bodyerrormessage, quote=True))
        else:

            owner = User.query.filter_by(username=session['username']).first()

            newBlog = Blog(user_title, user_body, owner)
            db.session.add(newBlog)
            db.session.commit()
            return redirect("/blog?id=" + str(newBlog.id))            
            #return redirect('/blog')
    else:        
        if 'username' not in session:
            return redirect('/login')
        else:
            return render_template('newpost.html')


if __name__ == '__main__':
     app.run()