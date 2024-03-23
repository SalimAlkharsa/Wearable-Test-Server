from flask import Flask, request, jsonify
from psycopg2 import sql
import psycopg2
from dotenv import load_dotenv
import os

app = Flask(__name__)

class DataStore:
    def __init__(self):
        self.data = []
        self.max_size = 1000*10 # Maximum number of entries the data store can hold

    def insert(self, data):
        '''
        Insert data into the data store
        '''
        if len(self.data) >= self.max_size:
            raise Exception("Data store is full")
        if data in self.data:
            raise Exception("Data already exists in data store")
        self.data.append(data)

    def reset(self):
        '''
        Reset the data store
        '''
        self.data = []

class Database:
    def __init__(self):
        load_dotenv()
        self.connection = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        self.cursor = self.connection.cursor()

    def insert(self, data):
        '''
        Insert data into the database from the data store
        '''
        try:
            # Iterate through the data and insert each entry
            for item in data:
                print(item[0])
                print(item[-1])
                timestamp = item.get('my_timestamp')[0] if item.get('my_timestamp') else None
                a_x = item.get('a_x')[0] if item.get('a_x') else None
                a_y = item.get('a_y')[0] if item.get('a_y') else None
                a_z = item.get('a_z')[0] if item.get('a_z') else None
                r_x = item.get('r_x')[0] if item.get('r_x') else None
                r_y = item.get('r_y')[0] if item.get('r_y') else None
                r_z = item.get('r_z')[0] if item.get('r_z') else None
                temperature = item.get('temperature')[0] if item.get('temperature') else None
                pressure = item.get('pressure')[0] if item.get('pressure') else None
                heart_rate = item.get('hr')[0] if item.get('hr') else None
                user_id = item.get('user_id')[0] if item.get('user_id') else None

                # Check if the exact data already exists in the database
                self.cursor.execute("""
                    SELECT * FROM sensors
                    WHERE timestamp = %s AND a_x = %s AND a_y = %s AND a_z = %s
                    AND r_x = %s AND r_y = %s AND r_z = %s AND temperature = %s AND pressure = %s
                    AND hr = %s AND user_id = %s
                """, (timestamp, a_x, a_y, a_z, r_x, r_y, r_z, temperature, pressure, heart_rate, user_id))

                existing_data = self.cursor.fetchone()

                # If the exact data doesn't exist, insert it into the database
                if not existing_data:
                    self.cursor.execute("""
                        INSERT INTO sensors (timestamp, a_x, a_y, a_z, r_x, r_y, r_z, temperature, pressure, hr, user_id)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (timestamp, a_x, a_y, a_z, r_x, r_y, r_z, temperature, pressure, heart_rate, user_id))

            # Commit the changes
            self.connection.commit()

        except Exception as e:
            print(f"Database Error: {e}")
            self.connection.rollback()  # Rollback the transaction in case of an error

    def close(self):
        self.connection.close()


data_store = DataStore()  # Create a data store to store the data 

# Define a route that only accepts POST requests
@app.route('/post_endpoint', methods=['POST'])
def post_request_handler():
    # curl -X POST -H "Content-Type: application/json" -d '{"name":"John Doe"}' https://i-want-to-pass-capstone-96abfc16411c.herokuapp.com/post_endpoint
    # curl -X POST -H "Content-Type: application/json" -d '{"name":"John Doe"}' http://127.0.0.1:5000/post_endpoint
    # Check if the request contains JSON data
    if request.is_json:
        data = request.get_json()

        #data_store.insert(data)  # Store the posted data
        # Now insert the data into the database
        db = Database()
        db.insert(data)
        return jsonify({"message": "Received POST and inserted request", "data": data}), 200
    # TO DO ADD MORE ERROR HANDLING CODE
    else:
        return jsonify({"error": "Request data must be in JSON format"}), 400

# Define a route that only accepts GET requests
@app.route('/get_endpoint', methods=['GET'])
def get_request_handler():
    # curl -X GET https://i-want-to-pass-capstone-96abfc16411c.herokuapp.com/get_endpoint
    # This is simply a route that returns the data_store for testing purposes
    return jsonify(data_store.data)

# Define a route that resets the data_store
@app.route('/reset_endpoint', methods=['POST'])
def reset_request_handler():
    # curl -X POST https://i-want-to-pass-capstone-96abfc16411c.herokuapp.com/reset_endpoint
    # This is simply a route that resets the data_store for testing purposes
    global data_store
    data_store = data_store.reset()  # Clear the data store
    return jsonify({"message": "Data store reset successfully"}), 200

# Define a route that shows hello world
@app.route('/')
def index():
    return jsonify({"message": "Hello World!"})

if __name__ == '__main__':
    app.run(debug=False)


'''
[
  {
    "name": "John Doe"
  },
  {
    "name": "John Doey"
  }
]
'''