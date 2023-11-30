from flask import Flask,render_template,redirect,request 


from pymongo import MongoClient

connection_string = 'mongodb+srv://kantashowribabu:showribabu@cluster1.es2isby.mongodb.net/'

# Create the MongoDB client
client = MongoClient(connection_string)

# Access the 'attendance' database and 'admin' collection
db = client['attendance']



#obj..
app=Flask(__name__)




#id generator..

def uid(desg,dept):
    icoll=db['increments']
    d=icoll.find()
    print(d)
    c=0
    if desg=='Student':
        c=d[0]['sinc']
        icoll.update_one({'sinc': c}, {'$set': {'sinc': str(int(c) + 1)}})    
    else:
        c=d[0]['finc']
        icoll.update_one({'finc': c}, {'$set': {'finc': str(int(c) + 1)}})    

    designation=desg
    department=dept
    s='23'+department[0:2]+designation[0:3]+c
    return s
    



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
def requestshandle():
    coll=db['signup']
    d=coll.find()
    d=list(d)
    k=[]
    for i in d:
        dummy=[]
        dummy.append(i['fname']+' '+i['lname'])
        dummy.append(uid(i['department'],i['designation']))
        dummy.append(i['designation'])
        dummy.append(i['department'])
        k.append(dummy)
    return render_template('requests.html',data=k)

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
    coll=db['signup']
    fname=request.form['fname']
    lname=request.form['lname']
    username=request.form['username']
    gender=request.form['gender']
    designation=request.form['designation']
    department=request.form['department']
    password=request.form['password']
    cpassword=request.form['cpassword']
    print(fname,lname,username,gender,designation,department,password,cpassword)
    
    if fname=='' or lname=='' or username=='' or gender=='' or designation=='' or password=='' or cpassword=='' or department=='':
        return render_template('faculty-signup.html',m='Please Fill all details')
    if(password != cpassword):
        return render_template('faculty-signup.html',r='Confirm password not matched')
    
    
    #check faculty already exists or not..
    d1=list(coll.find({'username':username}))
    
    if len(d1)>0:
        return render_template('faculty-signup.html',m='Username Already exists please use another username!!!')
    else:
        #now store data into signup
        d={'fname':fname,'lname':lname,'username':username,'gender':gender,'designation':designation,'department':department,'password':password,'cpassword':cpassword}
    
        res1=coll.insert_one(d)
        return render_template('faculty-login.html')
        

#faculty-login

@app.route('/faculty-login',methods=['POST'])
def facultylogin():
    coll=db['signup']
    username=request.form['username']
    password=request.form['password']
    
    if username=='' or  password=='':
        return render_template('faculty-login.html',m='Please fill all details')
    
    

        
    
    res=coll.find({'username':username, 'password':password})
   
    res= list(res)  # Convert the cursor to a list of documents
    print(res)

    if res:
        return render_template('faculty-login.html',m='Login Succeessfully')
    else:
        return render_template('faculty-login.html',m='No user Found!!!')
    
    

#student-signup

@app.route('/student-signup',methods=['POST'])
def studentsignup():
    coll=db['signup']
    fname=request.form['fname']
    lname=request.form['lname']
    username=request.form['username']
    gender=request.form['gender']
    designation=request.form['designation']
    department=request.form['department']
    password=request.form['password']
    cpassword=request.form['cpassword']
    
    print(fname,lname,username,gender,designation,department,password,cpassword)
    
    if fname=='' or lname=='' or username=='' or gender=='' or designation=='' or password=='' or cpassword=='' or department=='':
        return render_template('student-signup.html',m='Please Fill all details')
    
    if(password != cpassword):
        return render_template('student-signup.html',r='Confirm password not matched')
    
    
    #check faculty already exists or not..
    d1=list(coll.find({'username':username}))
    
    if len(d1)>0:
        return render_template('student-signup.html',m='Username Already exists please use another username!!!')
    else:
        #now store data into signup
        d={'fname':fname,'lname':lname,'username':username,'gender':gender,'designation':designation,'department':department,'password':password,'cpassword':cpassword}
    
        res1=coll.insert_one(d)
        return render_template('student-login.html')
        

#student-login

@app.route('/student-login',methods=['POST'])
def studentlogin():
    coll=db['signup']
    username=request.form['username']
    password=request.form['password']
    
    if username=='' or  password=='':
        return render_template('student-login.html',m='Please fill all details')

        
    
    res=coll.find({'username':username, 'password':password})
   
    res= list(res)  # Convert the cursor to a list of documents
    print(res)

    if res:
        return render_template('student-login.html',m='Login Succeessfully')
    else:
        return render_template('student-login.html',m='No user Found!!!')

        
     
    


if __name__=='__main__':
    
    app.run(host='0.0.0.0',port=5000)
    

