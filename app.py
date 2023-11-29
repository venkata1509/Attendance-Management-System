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


#server start..

if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000)
    

