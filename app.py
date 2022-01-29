import MySQLdb
from flask import Flask, render_template,flash,redirect, request, url_for, session, logging
from data import Articles
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

app = Flask(__name__)

# Config MySQL DB
app.config ['MYSQL_HOST'] = 'localhost'
app.config ["MYSQL_USER"] = 'root'
app.config ["MYSQL_PASSWORD"] = 'Sandra2000$'
app.config ["MYSQL_DB"] = 'MyFlaskBlogDB'
app.config ["MYSQL_CURSORCLASS"] = 'DictCursor'

# init MYSQL 
mysql = MySQL(app)


Articles = Articles()

@app.route('/')
def index():
    return render_template('home.html')
    
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/articles')
def articles():
    return render_template('articles.html', articles = Articles)

@app.route('/article/<string:id>/')
def display_article(id):
    return render_template('article.html', id=id)

class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=5, max=40)])
    username = StringField('Username', [validators.Length(min=7, max=30)])
    email = StringField('Email', [validators.Length(min=7, max=35)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Password does not match')
    ])
    confirm = PasswordField('Confirm Password')
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data 
        email = form.email.data
        username = form.username.data 
        password = sha256_crypt.hash(str(form.password.data))  
        
        # Creates cursor
        cur = mysql.connection.cursor() 
        
        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password)) 
        
        # commit to db 
        mysql.connection.commit()
        
        
        #Close db
        cur.close()
        
        flash('You are now registered and may login. Welcome to BlogIt!', 'success')
        
        redirect(url_for('index'))

    return render_template('register.html', form=form)

if __name__ == '__main__':
    app.secret_key = 'Secret145'
    app.run(debug=True)