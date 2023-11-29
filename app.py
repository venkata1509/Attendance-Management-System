from flask import Flask,render_template,redirect,request 
import pymysql as mysql


#obj..
app=Flask(__name__)
mydb=mysql.connect(
    host='localhost',
    user='root',
    password='Ksb6419*',
    database='attendance'
)
cursor=mydb.cursor()


#handlers...


@app.route('/')
def start():
    return render_template('index.html')

@app.route('/admin-login')
def admin_login():
    return render_template('admin-login.html')
@app.route('/admin-home')
def admin_home():
    return render_template('admin-home.html')


@app.route('/faculty-login')
def faculty_login():
    return render_template('faculty-login.html')


@app.route('/student-login')
def student_login():
    return render_template('student-login.html')

@app.route('/student-signup')
def student_signup():
    return render_template('student-signup.html')

@app.route('/faculty-signup')
def faculty_signup():
    return render_template('faculty-signup.html')



#admin login handling...

@app.route('/adlogin',methods=['POST'])
def adlogin():
    name=request.form['username']
    password=request.form['password']
    
    sql='select * from admin'
    result=cursor.execute(sql)
    
    print(type(result))
    
    for i in result.fetchall():
        print(i)
    return render_template('admin-home.html')
    
    


if __name__=='__main__':
    app.run(debug=True)
    

