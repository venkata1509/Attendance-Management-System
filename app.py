from flask import Flask,render_template,redirect,request 
import pymysql as mysql


#obj..
app=Flask(__name__)
# mydb=mysql.connect(
#     host='localhost',
#     user='root',
#     password='Ksb6419*',
#     database='attendance'
# )
# cursor=mydb.cursor()


#handlers...


@app.route('/')
def start():
    return render_template('index.html')

@app.route('/admin-login')
def admin_login():
    return render_template('admin-login.html')

@app.route('/faculty-login')
def faculty_login():
    return render_template('faculty-login.html')
#server start..

@app.route('/student-login')
def student_login():
    return render_template('student-login.html')


if __name__=='__main__':
    app.run(debug=True)
    

