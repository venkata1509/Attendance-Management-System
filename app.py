from flask import Flask,render_template,redirect,request 
import pymysql as mysql


from pymongo import MongoClient

connection_string = 'mongodb+srv://kantashowribabu:showribabu@cluster1.es2isby.mongodb.net/'

# Create the MongoDB client
client = MongoClient(connection_string)

# Access the 'attendance' database and 'admin' collection
db = client['attendance']



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


#requests handling by admin....
@app.route('/requestshandle')
def  requestshandle():
    return render_template('requests.html')

#attendance view by admin

@app.route('/faculty-attendance')
def facultyattendance():
    return render_template('faculty-view.html')
    

@app.route('/student-attendance')
def studentattendance():
    return render_template('student-view.html')



#add or remove by admin

@app.route('/faculty-remove')
def facultyremove():
    return render_template('faculty-addremove.html')
    

@app.route('/student-remove')
def studentremove():
    return render_template('student-addremove.html')


@app.route('/faculty-add')
def facultyadd():
    return render_template('faculty-addremove.html')
    

@app.route('/student-add')
def studentadd():
    return render_template('student-addremove.html')



#admin login handling...

@app.route('/adlogin',methods=['POST'])
def adlogin():
    adcoll=db['admin']
    
    name=request.form['username']
    password=request.form['password']
    if(name=='' and password==''):
        return render_template('admin-login.html',m='Please fill all details!!')
    
    
    print(name,password)
    
    # sql= 'SELECT * FROM admin'
    # cursor.execute(sql)
    # result = cursor.fetchall()
    # print(type(result))
    
    # for i in result:
    #     print(i)
    #     if i[0]==name and i[1]==password:
    #         return render_template('admin-home.html')
    #     else:
    #         return render_template('admin-login.html',m='Please enter valid details')
    
    d=adcoll.find()
    

    if (d[0]['username'] == name and d[0]['password'] == password):
        return render_template('admin-home.html')
    else:
        return render_template('admin-login.html',m='Please enter valid details')
        


#faculty-signup

@app.route('/faculty-signup',methods=['POST'])
def facultysignup():
'''
fname
lname
username
gender
designation
department
password
cpassword
'''
    pass    
                     
    
    
    
    


if __name__=='__main__':
    
    app.run(debug=True)
    

