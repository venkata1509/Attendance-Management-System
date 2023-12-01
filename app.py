from flask import Flask,render_template,redirect,request 
import datetime

import json

from pymongo import MongoClient

import ast

connection_string = 'mongodb+srv://kantashowribabu:showribabu@cluster1.es2isby.mongodb.net/'

# Create the MongoDB client
client = MongoClient(connection_string)

# Access the 'attendance' database and 'admin' collection
db = client['attendance']



#obj..
app=Flask(__name__)




#id generator..

def uid(dept,desg):
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
    

#day from date..


def is_leap_year(year):
    # Function to check if a year is a leap year
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def count_odd_days(year):
    # Function to count the odd days for a given year
    # Each non-leap year has 1 odd day, and each leap year has 2 odd days
    odd_days = 1 if not is_leap_year(year) else 2
    return odd_days

def get_days_in_month(month, year):
    # Function to get the number of days in a given month
    days_in_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if month == 2 and is_leap_year(year):
        return 29
    return days_in_month[month]

def count_days_since_1st_Jan_1AD(day, month, year):
    # Function to count the total number of days from 1st January 1 AD to the input date
    total_days = 0

    # Years from 1 AD to the input year (excluding the input year)
    for y in range(1, year):
        total_days += count_odd_days(y)

    # Months from January to the input month (excluding the input month)
    for m in range(1, month):
        total_days += get_days_in_month(m, year)

    total_days += day  # Days from 1st of the input month to the input day (we don't subtract 1 here)

    return total_days

def find_day_of_week(day, month, year):
    # Calculate the day of the week using 1st January 1 AD as the reference date
    days_of_week = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    total_days = count_days_since_1st_Jan_1AD(day, month, year) % 7
    return days_of_week[total_days]

# Example usage:
def day_from_date(d):
    year, month, day = map(int, d.split('-'))
    day_of_week = find_day_of_week(day, month, year)
    return day_of_week

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
        if i['flag'] =='0':
            dummy=[]
            dummy.append(i['fname']+' '+i['lname'])
            dummy.append(i['username'])
            dummy.append(uid(i['department'],i['designation']))
            dummy.append(i['designation'])
            dummy.append(i['department'])
            dummy.append(i['password'])
            k.append(dummy)
    print(k)
    return render_template('requests.html',data=k)


#faculty view..
@app.route('/facultyview')
def facultyview():    
    coll=db['faculty']
    d=coll.find()
    d=list(d)
    k=[]
    for i in d:
            dummy=[]
            dummy.append(i['Id'])
            dummy.append(i['name'])
            dummy.append(i['Department'])
            k.append(dummy)
    return render_template('faculty-view.html',data=k)

#student view 

@app.route('/studentview')
def studentview():    
    coll=db['student']
    d=coll.find()
    d=list(d)
    k=[]
    for i in d:
            dummy=[]
            dummy.append(i['Id'])
            dummy.append(i['name'])
            dummy.append(i['Department'])
            k.append(dummy)
    return render_template('student-view.html',data=k)
#attendance view by admin

@app.route('/faculty-attendance')
def facultyattendance():
    return redirect('/facultyview')

    

def attendance(Id):
    acoll=db['attend']
    d=acoll.find({'Id':Id})
    d=list(d)
    c=0
    p=0
    if len(d)==0:
        print(Id,'--->',0)
        return 0
    else:
        c=len(d)
        p=acoll.find({'Id':Id,'status':'Present'})
        p=list(p)
        print(Id,'--->',int((len(p)/c)*100))
        return int((len(p)/c)*100)
        

@app.route('/student-attendance')
def studentattendance():
    coll=db['student']
    d=coll.find()
    d=list(d)
    k=[]
    for i in d:
            dummy=[]
            dummy.append(i['Id'])
            dummy.append(i['name'])
            dummy.append(i['Department'])
            dummy.append(attendance(i['Id']))
            k.append(dummy)
    return render_template('student-view-admin.html',data=k)



#add or remove by admin

@app.route('/faculty-remove')
def facultyremove():
    return render_template('faculty-removefaculty.html')
    
@app.route('/faculty-remove-1',methods=['post'])
def facultyremove1():
    username=request.form['username']
    coll=db['faculty']
    coll.delete_one({'username':username})
    return render_template('faculty-removefaculty.html',result="Removed Successfully")


@app.route('/student-remove')
def studentremove():
    return render_template('student-removestudent.html')

@app.route('/student-remove-1',methods=['post'])
def studentremove1():
    username=request.form['username']
    coll=db['student']
    coll.delete_one({'username':username})
    return render_template('student-removestudent.html',result="Removed Successfully")


@app.route('/faculty-add')
def facultyadd():
    return render_template('faculty-addfaculty.html')
#handle..
@app.route('/faculty-add-1', methods=['post'])
def facultyadd1():
    coll=db['faculty']
    fname=request.form['fname']
    lname=request.form['lname']
    name=fname+' '+lname
    username=request.form['username']
    gender=request.form['gender']
    designation=request.form['designation']
    department=request.form['department']
    password=request.form['password']
    cpassword=request.form['cpassword']
    userid=uid(department,designation)
    
    d = {'name': name, 'username': username, 'Id': userid, 'Designation': designation, 'Department': department,'password': password,'flag':'0'}
    
    print(fname,lname,username,gender,designation,department,password,cpassword)
    if fname=='' or lname=='' or username=='' or gender=='' or designation=='' or password=='' or cpassword=='' or department=='':
        return render_template('faculty-addfaculty.html',m='Please Fill all details')
    if(password != cpassword):
        return render_template('faculty-addfaculty.html',r='Confirm password not matched')
    
    
    #check faculty already exists or not..
    d1=list(coll.find({'username':username}))
    
    if len(d1)>0:
        return render_template('faculty-addfaculty.html',m='Username Already exists please use another username!!!')
    else:
        res1=coll.insert_one(d)
        return redirect('/facultyview')
    

@app.route('/student-add')
def studentadd():
    return render_template('student-addstudent.html')
#handler..
@app.route('/student-add-1', methods=['post'])
def studentadd1():
    coll=db['student']
    fname=request.form['fname']
    lname=request.form['lname']
    name=fname+' '+lname
    username=request.form['username']
    gender=request.form['gender']
    designation=request.form['designation']
    department=request.form['department']
    password=request.form['password']
    cpassword=request.form['cpassword']
    userid=uid(department,designation)
    
    d = {'name': name, 'username': username, 'Id': userid, 'Designation': designation, 'Department': department,'password': password,'flag':'0'}
    
    print(fname,lname,username,gender,designation,department,password,cpassword)
    if fname=='' or lname=='' or username=='' or gender=='' or designation=='' or password=='' or cpassword=='' or department=='':
        return render_template('student-addstudent.html',m='Please Fill all details')
    if(password != cpassword):
        return render_template('student-addstudent.html',r='Confirm password not matched')
    
    
    #check faculty already exists or not..
    d1=list(coll.find({'username':username}))
    
    if len(d1)>0:
        return render_template('student-addstudent.html',m='Username Already exists please use another username!!!')
    else:
        res1=coll.insert_one(d)
        return redirect('/studentview')

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
        d={'fname':fname,'lname':lname,'username':username,'gender':gender,'designation':designation,'department':department,'password':password,'cpassword':cpassword,'flag':'0'}
    
        res1=coll.insert_one(d)
        return render_template('faculty-login.html')
        

#faculty-login
@app.route('/faculty-login',methods=['POST'])
def facultylogin():
    coll=db['faculty']
    username=request.form['username']
    password=request.form['password']
    
    if username=='' or  password=='':
        return render_template('faculty-login.html',m='Please fill all details')
    
    res=coll.find({'username':username, 'password':password})
   
    res= list(res)  # Convert the cursor to a list of documents
    print(res)
    
    #student-details...
    
    # coll=db['student']
    # d=coll.find()
    # d=list(d)
    # k=[]
    # for i in d:
    #         dummy=[]
    #         dummy.append(i['Id'])
    #         dummy.append(i['name'])
    #         coll.update_one({'Id':i['Id']},{'$set':{'flag':'0'}})
    #         k.append(dummy)
    if res:
        # coll.update_many({'flag':'0'})
        # return render_template('fill-attendance.html',data=k,dd=str(datetime.datetime.now().date()))
        return render_template('faculty-details-view.html',Id=res[0]['Id'],name=res[0]['name'],d=res[0]['Department'])
    else:
        return render_template('faculty-login.html',m='Admin Review Pending [OR] Enter correct details ')
    
    
#fill-atttendance
@app.route('/fillattendance')
def fillattendance():
    #student-details...
    coll=db['student']
    d=coll.find()
    d=list(d)
    k=[]
    for i in d:
            dummy=[]
            dummy.append(i['Id'])
            dummy.append(i['name'])
            coll.update_one({'Id':i['Id']},{'$set':{'flag':'0'}})
            k.append(dummy)
    return render_template('fill-attendance.html',data=k,dd=str(datetime.datetime.now().date()))
    

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
        d={'fname':fname,'lname':lname,'username':username,'gender':gender,'designation':designation,'department':department,'password':password,'cpassword':cpassword,'flag':'0'}
    
        res1=coll.insert_one(d)
        return render_template('student-login.html')
        

#student-login

@app.route('/student-login',methods=['POST'])
def studentlogin():
    coll=db['student']
    
    username=request.form['username']
    password=request.form['password']
    
    if username=='' or  password=='':
        return render_template('student-login.html',m='Please fill all details')

    res=coll.find({'username':username, 'password':password})
   
    res= list(res)  # Convert the cursor to a list of documents
    print(res)
 
    
    if res:
        #detatils of the student ....
       
        Id=res[0]['Id']
        name=res[0]['name']
        
        
        acoll=db['attend']
        
        d=acoll.find({'Id':Id})
        d=list(d)
        print('Data:------>',d)
        k=[]
        c=0
        p=0
        
        if len(d)==0:
            print('No attendence found')
            return render_template('student-details-view.html',Id=Id,name=name,att=int(0))

        else:
            for i in d:
                if i['Id']==Id:
                    c=c+1
                    dummy=[]
                    dummy.append(i['date'])
                    dummy.append(day_from_date(i['date']))
                    dummy.append(i['status'])
                    if(i['status']=='Present'):
                        p+=1
                    k.append(dummy)
            return render_template('student-details-view.html',Id=Id,name=name,data=k,att=int((p/c)*100))

    else :
        return render_template('student-login.html',m='Admin Review Pending [OR] Enter correct details ')




#admin request handling..

@app.route('/add_user/<i>',methods=['GET','POST'])
def add_user(i):
    i=ast.literal_eval(i)
    print(type(i))
    print(i)
  
    fcoll = db['faculty']
    scoll = db['student']
    
    sigcoll = db['signup']
        
    
    
    name=i[0]
    username = i[1]
    userid = i[2]
    designation = i[3]
    department = i[4]
    password=i[5]
    print(password)
    d = {'name': name, 'username': username, 'Id': userid, 'Designation': designation, 'Department': department,'password': password,'flag':'0'}
    
    if designation == 'Student':
        scoll.insert_one(d)
        sigcoll.update_one({'username': username}, {'$set': {'flag': '1'}})
        return redirect('/studentview')
    
    else:
        fcoll.insert_one(d)
        sigcoll.update_one({'username': username}, {'$set': {'flag': '1'}})
        return redirect('/facultyview')

        
        

@app.route('/remove_user/<i>',methods=['GET','POST'])
def removeuser(i):
    print(i)
    i=ast.literal_eval(i)
    sigcoll = db['signup']
        
    username = i[1]
    designation = i[3]
    
    if designation == 'Student':
        sigcoll.update_one({'username': username}, {'$set': {'flag': '1'}})
    else:
        sigcoll.update_one({'username': username}, {'$set': {'flag': '1'}})    

    return render_template('requests.html')


#faculty attendance handling..


@app.route('/present/<i>',methods=['GET','POST'])
def presentuser(i):
    print(i)
    i=ast.literal_eval(i)
    sigcoll = db['attend']
    scoll=db['student']
    Id= i[0]
    name= i[1]
    sigcoll.insert_one({'Id': Id ,'name':name,'date':str(datetime.datetime.now().date()),'status':'Present'})
    scoll.update_one({'Id': Id}, {'$set': {'flag': '1'}})
    
    d=scoll.find()
    d=list(d)
    k=[]
    
    for i in d:
        if i['flag'] =='0':
            dummy=[]
            dummy.append(i['Id'])
            dummy.append(i['name'])
            k.append(dummy)
    print(k)
    return render_template('fill-attendance.html',data=k,dd=str(datetime.datetime.now().date()))


@app.route('/absent/<i>',methods=['GET','POST'])
def absentuser(i):
    print(i)
    i=ast.literal_eval(i)
    sigcoll = db['attend']
    scoll=db['student']
    Id= i[0]
    name= i[1]
    scoll.update_one({'Id': Id}, {'$set': {'flag': '1'}})

    sigcoll.insert_one({'Id': Id ,'name':name,'date':str(datetime.datetime.now().date()),'status':'Absent'})
    
    d=scoll.find()
    d=list(d)
    k=[]
    for i in d:
        if i['flag']=='0':
            dummy=[]
            dummy.append(i['Id'])
            dummy.append(i['name'])
            k.append(dummy)
    return render_template('fill-attendance.html',data=k,dd=str(datetime.datetime.now().date()))




if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000)
'''

#add or remove by admin

@app.route('/faculty-remove')
def facultyremove():
    return render_template('faculty-removefaculty.html')

@app.route('/faculty-remove-1',methods=['post'])
def facultyremove1():
    id=request.form['username']
    doc=client['attendance']['admin']
    doc.delete_one(id)
    return render_template('faculty-addfaculty.html',result="Removed Successfully")
    

@app.route('/student-remove')
def studentremove():
    return render_template('student-removestudent.html')


@app.route('/student-remove-1',methods=['post'])
def studentremove1():
    id=request.form['username']
    doc=client['attendance']['admin']
    doc.delete_one(id)
    return render_template('student-removestudent.html',result="Removed Successfully")






'''