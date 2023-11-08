from flask import Flask, render_template, request,jsonify
import pyodbc
import pymssql
import pypyodbc as odbc
import json

app = Flask(__name__)
# DB_HOST = 'mssql.esmsys.in,14251'
# DB_USER = 'DESKTOP-KFNVA5M\aryas'
# DB_PASSWORD = 'Interview@123'
# DB_NAME = 'interview'

# DB_HOST = 'DESKTOP-KFNVA5M'
# DB_USER = 'DESKTOP-KFNVA5M\aryas'
# # DB_PASSWORD = 'Interview@123'
# DB_NAME = 'interview'


# try:
#     conn = pymssql.connect(server=DB_HOST, user=DB_USER, database=DB_NAME)
#     # If the connection is successful, you can perform your operations here
#     # ...
#     # conn.close()  # Close the connection when done
# except pymssql.Error as e:
#     print(f"Connection failed: {e}")

# pymssql.connect(server=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)

DRIVER_NAME = 'SQL SERVER'
SERVER_NAME = 'DESKTOP-KFNVA5M'
DATABASE_NAME = 'interview'

connection_string = f"""
    DRIVER={{{DRIVER_NAME}}};
    SERVER={SERVER_NAME};
    DATABASE={DATABASE_NAME};
    Trust_Connection=yes;
"""

conn = odbc.connect(connectString = connection_string)
print(conn)

# write a query to show all data from my_State table
# cursor = conn.cursor()
# query = "SELECT * FROM [dbo].[my_state]"
# cursor.execute(query)
# rows = cursor.fetchall()
# for row in rows:
#     print (row)
#     # close the connection

# state_id = 5
# cursor = conn.cursor()
# sql_query = f"select CityName from [dbo].[my_city] where StateID = '{state_id}'"
# cursor.execute(sql_query)
# resultSet = cursor.fetchall()
# print(resultSet)
# cities = [row[0] for row in resultSet]
# print(cities)
# print(jsonify(cities))
    




@app.route('/')
def login():
    return render_template('index.html')


userDataBase = {
        "username": "arya",
        "password": "123"
    }

@app.route('/submit', methods=['POST', 'GET'])
def submit():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == userDataBase["username"] and password == userDataBase["password"]:
            print("Login Successful")
            return render_template('data.html')
        else:
            return "not received"
    elif request.method == 'GET':
        return render_template('data.html')



# /get_state api for loading all state
@app.route("/get_states", methods=['GET','POST'])
def getStates():
    try:
        cursor = conn.cursor()
        sqlQuery = "select * from [dbo].[my_state]"
        cursor.execute(sqlQuery)
        resultSet = cursor.fetchall()
        jsonResult = []
        dictRow = {}
        print(resultSet)
        # traverse resultSet and add each item in dictionary
        for row in resultSet:
            dictRow[str(row[0])] = str(row[1])
        
        print(dictRow)
        
        resp = app.response_class(
            response=json.dumps(dictRow),
            status=200,
            mimetype='application/json'
            )
        return resp
    except:
        traceback.print_exc()


@app.route('/get_cities/<state_id>')
def get_cities(state_id):
    
    try:
        cursor = conn.cursor()
        sqlQuery = f"SELECT * FROM [dbo].[my_city] WHERE StateID = {state_id}"
        cursor.execute(sqlQuery)
        resultSet = cursor.fetchall()
        cities = {}
        # traverse resultset 
        for city in resultSet:
            cities[city[0]] = city[1]
        resp = app.response_class(
            response=json.dumps(cities),
            status=200,
            mimetype='application/json'
            )
        return resp
    except:
        traceback.print_exc()

@app.route('/get_taluka/<city_id>')
def get_talukas(city_id):
    try:
        cursor = conn.cursor()
        sqlQuery = f"SELECT * FROM [dbo].[my_Taluka] WHERE CityID = {city_id}"
        cursor.execute(sqlQuery)
        resultSet = cursor.fetchall()
        talukas = {}
        # traverse resultset
        for taluka in resultSet:
            talukas[taluka[0]] = taluka[1]
        resp = app.response_class(
            response=json.dumps(talukas),
            status=200,
            mimetype='application/json'
        )
        return resp
    except:
        traceback.print_exc()

@app.route('/get_village/<taluka_id>')
def get_villages(taluka_id):
    try:
        cursor = conn.cursor()
        sqlQuery = f"SELECT * FROM [dbo].[my_Village] WHERE TalukaID = {taluka_id}"
        cursor.execute(sqlQuery)
        resultSet = cursor.fetchall()
        villages = {}
        # traverse resultset
        for village in resultSet:
            villages[village[0]] = village[1]
        
        resp = app.response_class(
            response=json.dumps(villages),
            status=200,
            mimetype='application/json'
        )
        return resp
    except:
        traceback.print_exc()

@app.route('/edit_village', methods=['GET', 'POST'])
def edit_village():
    if request.method == 'GET':
        village_id = request.args.get('villageID')
        village_name = request.args.get('villageName')
        # Perform actions with the received talukaID
        print("Name: ", village_name)
        print("id:", village_id)
        return render_template('edit_village.html',village_id=village_id, village_name=village_name )
    elif request.method == "POST":
        data = json.loads(request.data)
        print(data)
        village_id = data["villageID"]
        newVillageName = data["newVillageName"]
        print(village_id, newVillageName)
        cursor = conn.cursor()
        sqlQuery = f"UPDATE [dbo].[my_Village] SET VillageName = '{newVillageName}' WHERE VillageID='{village_id}'"
        cursor.execute(sqlQuery)
        conn.commit()
        return render_template('success.html')

@app.route('/edit_taluka', methods=['GET', 'POST'])
def edit_taluka():
    if request.method == 'GET':
        taluka_id = request.args.get('talukaID')
        taluka_name = request.args.get('talukaName')
        # Perform actions with the received talukaID
        print("Name:", taluka_name)
        print("ID:", taluka_id)
        return render_template('edit_taluka.html', taluka_id=taluka_id, taluka_name=taluka_name)
    elif request.method == "POST":
        data = json.loads(request.data)
        print(data)
        taluka_id = data["talukaID"]
        newTalukaName = data["newTalukaName"]
        print(taluka_id, newTalukaName)
        cursor = conn.cursor()
        sqlQuery = f"UPDATE [dbo].[my_Taluka] SET TalukaName = '{newTalukaName}' WHERE TalukaID='{taluka_id}'"
        cursor.execute(sqlQuery)
        conn.commit()
        return render_template('success.html')


@app.route("/add_state", methods = ['POST', 'GET'])
def add_state():
    if request.method == 'POST':
        data = json.loads(request.data)
        print(data)
        cursor = conn.cursor()
        # write sql query to count total states 
        stateCount = 0
        cursor.execute("SELECT COUNT(*) FROM my_State")
        resultSet = cursor.fetchone()
        for row in resultSet:
            stateCount += row
        stateId = stateCount + 1

        # add data and stateID to my_State table
        
        insertSQL = f"INSERT INTO my_State (stateID, stateName) VALUES ({stateId}, '{data}')"
        cursor.execute(insertSQL)
        conn.commit()
        return render_template('success.html')
    elif request.method == 'GET':
        return render_template('add_data.html')

@app.route("/change_taluka", methods=['GET', 'POST'])
def change_taluka():
    if request.method == 'GET':
        village_id = request.args.get('villageID')
        village_name = request.args.get('villageName')
        city_id = request.args.get('cityID')
        print(village_id, village_name, city_id)
        # write a query to get city name based on city_id
        cursor = conn.cursor()
        selectCitySQL = f'SELECT * FROM my_City WHERE cityID={city_id}'
        cursor.execute(selectCitySQL)
        resultSet = cursor.fetchall()
        city_name = list(resultSet)[0][1]
        print(list(resultSet)[0][1])
        return render_template('change_village_taluka.html', village_id=village_id, village_name=village_name, city_id=city_id, city_name=city_name)
    elif request.method == "POST":
        data = json.loads(request.data)
        print(data)
        selectedTaluka = data["selectedTaluka"]
        village_id = data["villgeID"]
        village_name = data["villageName"]
        # write a query to add village id and village name and selectedTaluke to my_Village table
        cursor = conn.cursor()
        insertSQL = f"UPDATE my_Village SET TalukaID='{selectedTaluka}' WHERE VillageID={village_id}"
        cursor.execute(insertSQL)
        conn.commit()
        return render_template('success.html')

@app.route("/successUpdate")
def successUpdate():
    return render_template('success.html')


if __name__ == '__main__':
    app.run(debug=True)
