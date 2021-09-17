from flask import Flask, render_template, request, redirect, make_response
from flask.json import jsonify
from flask_restful import Api, Resource, reqparse
from flask_mysqldb import MySQL
from functools import wraps
from json import JSONDecodeError
import yaml, json, jsonpickle

app = Flask(__name__)
api = Api(app)
req_par = reqparse.RequestParser()

db = yaml.safe_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
# app.config['MYSQL_PORT'] = db['mysql_port']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == 'username' and auth.password == 'password':
            return f(*args, **kwargs)

        return make_response('Could not verify your login!', 401)

    return decorated


@app.route('/')
@auth_required
def welcome():
    res = {
        "Message":"Welcome to basic flask and mysql app."
    }
    return res, 200


class Userservice(Resource):
    @auth_required
    def get(self):
        userDetails = request.get_json()
        email = userDetails['email']
        try:
            cur = mysql.connection.cursor()
            result = cur.execute("SELECT name,email FROM users")
            if result>0:
                users = cur.fetchall()
            res = {
                "Users":users
            }
            res_code = 200
        except Exception as e:
            res = {
                "Error":e
            }
            res_code = 404
        return res, res_code
    
    @auth_required
    def post(self):
        userDetails = request.get_json()
        email = userDetails['email']
        name = userDetails['name']
        password = userDetails['password']
        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO users(name, email, password) VALUES(%s, %s, %s)",(name, email, password))
            mysql.connection.commit()
            cur.close()
            res = {
                "Message":"New user added.",
                "User Details":{
                    "Name":name,
                    "email":email
                }
            }
            res_code = 201
        except Exception as e:
            res = {
                "Error":e
            }
            res_code = 403
        return res, res_code

api.add_resource(Userservice,"/user")

# @app.route('/user', methods=['GET', 'POST'])
# def user_service():
#     userDetails = json.loads(request.get_data())
#     print(userDetails)
#     print(type(str(userDetails['email'])))
#     email = userDetails['email']
#     if request.method == 'POST':
#         name = userDetails['name']
#         password = userDetails['password']
#         try:
#             cur = mysql.connection.cursor()
#             cur.execute("INSERT INTO users(name, email, password) VALUES(%s, %s, %s)",(name, email, password))
#             mysql.connection.commit()
#             cur.close()
#             res = {
#                 "Message":"New user added.",
#                 "User Details":{
#                     "Name":name,
#                     "email":email
#                 }
#             }
#             res_code = 201
#         except Exception as e:
#             res = {
#                 "Error":e
#             }
#             res_code = 403
#     if request.method == 'GET':
#         try:
#             cur = mysql.connection.cursor()
#             result = cur.execute("SELECT name,email FROM users")
#             # res = {
#             #     "User Details":{
#             #         "Name":name,
#             #         "email":email
#             #     }
#             # }
#             res = {
#                 "Details":result
#             }
#             res_code = 200
#         except Exception as e:
#             res = {
#                 "Error":e
#             }
#             res_code = 404
#     return res, res_code

@app.route('/users')
def users():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM users")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('users.html',userDetails=userDetails)

if __name__ == '__main__':
    app.run(debug=True)