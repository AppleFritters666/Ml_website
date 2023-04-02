from flask import Blueprint,render_template,request,flash,redirect,url_for,session
import mysql.connector

db = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='pranav',
    database='website'
)

mycursor = db.cursor()

mycursor.execute("select * from details")
x = mycursor.fetchall()
usernames = [i[0] for i in x]
names = [i[1] for i in x]
passwords = [i[2] for i in x]
users = {usernames[i]: [passwords[i],names[i]] for i in range(len(usernames))}
print(users)

auth = Blueprint('auth',__name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username in usernames:
            if users[username][0] == password:
                session['logged_in'] = True
                return render_template('home.html',user=users[username][1]) 
            else:
                flash('Incorrect Password!',category='error')
    else:
        flash('Username Does Not Exist!',category='error')
    return render_template("login.html")

@auth.route('/logout', methods=['GET','POST'])

def logout():
    session['logged_in'] = False
    return redirect(url_for('views.home')) 

@auth.route('/sign_up', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if password1 != password2:
            flash('Passwords dont match!',category='error')
        else:
            if username in usernames:
                flash('Username exists!',category='error')
            else:
                mycursor.execute("INSERT INTO details VALUES (%s,%s,%s)",[username,name,password1])
                db.commit()
                flash('account created',category='success')
                session['logged_in'] = True
                return render_template('home.html',user=users[username][1]) 

    return render_template('sign_up.html')