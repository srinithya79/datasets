import jsonpickle as jsonpickle
from flask import Flask, Response, json, request
import pyodbc as db
from flask_cors import CORS

appu = Flask(__name__)
CORS(appu)

class User:
    def __init__(self, username, emailaddress, rolename):
        self.username = username
        self.emailaddress = emailaddress
        self.rolename = rolename

con = db.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER=BG164\\SQLEXPRESS;uid=sa;pwd=Thylak@123;DATABASE=status')
cursor = con.cursor()


@appu.route('/getuserroles')
def getuserroles():
    UserList = []
    cursor.execute('select * from userroles')
    for row in cursor:
        print(row)
        UserList.append(User(row[0], row[1], row[2]))
    return Response(jsonpickle.encode(UserList), 200)


@appu.route('/getuserrolesbyId/<id>')
def getuserrolesbyId(id):
    UserList = []
    print("received id is "+id)
    cursor.execute('select * from userroles where userrolesid=' + id)
    for row in cursor:
        print(row)
        UserList.append(User(row[0], row[1], row[2]))
    return Response(jsonpickle.encode(UserList), 200)

@appu.route('/Createuserroles', methods=['POST'])
def Createuserroles():
    username = request.json['username']
    emailaddress = request.json['emailaddress']
    rolename = request.json['rolename']
    insertstatement = "insert into userroles (username, emailaddress, rolename) "\
    "values ('{username}','{emailaddress}','{rolename}')".format(username=username,emailaddress=emailaddress,rolename=rolename)
    print(insertstatement)
    cursor.execute(insertstatement)
    con.commit()
    return Response(jsonpickle.encode(User(username, emailaddress,rolename )), 200)


@appu.route('/Updateuserroles', methods=['POST'])
def Updateuserroles():
    id = request.json['id']
    username = request.json['username']
    emailaddress = request.json['emailaddress']
    rolename = request.json['rolename']
    updatestatement = "update userroles set username='{usernameParam}',emailaddress='{emailaddressParam}', rolename='{rolenameParam}'where userroleid={id}".\
        format(usernameParam=username,emailaddressParam=emailaddress,rolenameParam=rolename, id=id)
    cursor.execute(updatestatement)
    con.commit()
    return Response(True, 200)

@appu.route('/Deleteuserroles', methods=['GET','POST'])
def Deleteuserroles():
    id = request.json['id']
    print('received id for delete'+id)
    deletestatement = "delete from userroles where userroleid={id}".format(id=id)
    cursor.execute(deletestatement)
    con.commit()
    return Response(jsonpickle.encode(deletestatement), 200)

if __name__=='__main__':
    appu.run(debug=True)